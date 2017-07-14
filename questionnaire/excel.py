from rexec import FileWrapper

import xlsxwriter
from django.core.files.temp import NamedTemporaryFile

from questionnaire.models import Answer
from questionnaire.views import big_question_dict
from django.http import HttpResponse
import os


def workers_sentiment_detailed_results(request):
    workers_sentiment_qs = Answer.objects.filter(
        question__questionset__questionnaire__type="WORKERS_SENTIMENT"
    )

    campaign = request.GET.get('campaign', None)
    if campaign:
        workers_sentiment_qs = workers_sentiment_qs.filter(campaign_id=campaign)

    filename = 'workers_sentiment_detailed_results.xlsx'
    excel = NamedTemporaryFile(suffix='.xlsx')
    wordbook = xlsxwriter.Workbook(excel.name)
    bold = wordbook.add_format({'bold': True})
    runids = workers_sentiment_qs.values_list('runid', flat=True).distinct()

    for i in range(1,6):
        worksheet = wordbook.add_worksheet(name='Questionnaire part %s' % str(i))
        worksheet.set_default_row(20)
        answers_for_part = workers_sentiment_qs.filter(question__questionset__sortid=i).order_by('question_id')
        num_of_questions = answers_for_part.order_by('question__text_en').distinct('question__text_en').count()
        question_texts = answers_for_part.values_list('question__text_en', flat=True).order_by('question_id').distinct()[:num_of_questions]

        worksheet.write(0, 0, '#', bold)
        worksheet.write(0, 1, 'TYPE', bold)
        worksheet.write(0, 2, 'DATE', bold)
        worksheet.write(0, 3, 'CAMPAIGN', bold)
        for idx, question_text in enumerate(question_texts):
            clean_question_text = question_text.strip().replace('\r\n', '')
            worksheet.write(0, (idx + 4), question_text.upper() if clean_question_text not in big_question_dict else big_question_dict[clean_question_text], bold)

        for idx2, runid in enumerate(runids):
            answers_for_part_for_user = answers_for_part.filter(runid=runid).order_by('question_id')
            sample_answer = answers_for_part_for_user[0]

            worksheet.write((idx2 + 1), 0, (idx2 + 1))
            worksheet.write((idx2 + 1), 1, sample_answer.subject.type.capitalize())
            worksheet.write((idx2 + 1), 2, sample_answer.answered_at.strftime('%d/%m/%Y'))
            worksheet.write((idx2 + 1), 3, sample_answer.campaign.name.capitalize())

            for idx3, user_answer in enumerate(answers_for_part_for_user):
                worksheet.write((idx2 + 1), (idx3 + 4), user_answer.get_answer_text())

        for code in range(ord('a'), ord('c') + 1):
            worksheet.set_column('%s:%s' % (chr(code).upper(), chr(code).upper()), 15)

        for code in range(ord('d'), ord('j') + 1):
            worksheet.set_column('%s:%s' % (chr(code).upper(), chr(code).upper()), 30)

    wordbook.close()

    response = HttpResponse(FileWrapper(file(excel.name, 'rb')), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    response['Content-Length'] = os.path.getsize(excel.name)

    return response


def brand_values_detailed_results(request):
    brand_value_qs = Answer.objects.filter(
        question__questionset__questionnaire__type="BRAND_VALUE"
    )

    campaign = request.GET.get('campaign', None)
    if campaign:
        brand_value_qs = brand_value_qs.filter(campaign_id=campaign)

    filename = 'brand_value_detailed_results.xlsx'
    excel = NamedTemporaryFile(suffix='.xlsx')
    wordbook = xlsxwriter.Workbook(excel.name)
    bold = wordbook.add_format({'bold': True})
    runids = brand_value_qs.values_list('runid', flat=True).distinct()

    worksheet = wordbook.add_worksheet(name='Questionnaire detailed answers')
    worksheet.set_default_row(20)
    answers = brand_value_qs.order_by('question_id')
    num_of_questions = answers.order_by('question__text_en').distinct('question__text_en').count()
    question_texts = answers.values_list('question__text_en', flat=True).order_by('question_id').distinct()[:num_of_questions]

    worksheet.write(0, 0, '#', bold)
    worksheet.write(0, 1, 'TYPE', bold)
    worksheet.write(0, 2, 'DATE', bold)
    worksheet.write(0, 3, 'CAMPAIGN', bold)
    for idx, question_text in enumerate(question_texts):
        worksheet.write(0, (idx + 4), question_text.upper(), bold)

    for idx2, runid in enumerate(runids):
        answers_for_part_for_user = answers.filter(runid=runid).order_by('question_id')
        sample_answer = answers_for_part_for_user[0]

        worksheet.write((idx2 + 1), 0, (idx2 + 1))
        worksheet.write((idx2 + 1), 1, sample_answer.subject.type.capitalize())
        worksheet.write((idx2 + 1), 2, sample_answer.answered_at.strftime('%d/%m/%Y'))
        worksheet.write((idx2 + 1), 3, sample_answer.campaign.name.capitalize())

        for idx3, user_answer in enumerate(answers_for_part_for_user):
            worksheet.write((idx2 + 1), (idx3 + 4), user_answer.get_likert_answer())

    for code in range(ord('a'), ord('c') + 1):
        worksheet.set_column('%s:%s' % (chr(code).upper(), chr(code).upper()), 15)

    for code in range(ord('d'), ord('s') + 1):
        worksheet.set_column('%s:%s' % (chr(code).upper(), chr(code).upper()), 30)

    wordbook.close()

    response = HttpResponse(FileWrapper(file(excel.name, 'rb')), content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    response['Content-Length'] = os.path.getsize(excel.name)

    return response
