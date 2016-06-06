__author__ = 'mpetyx'

from django import http
from django.shortcuts import render_to_response
from django.template import RequestContext
from questionnaire.models import *

from questionnaire.page.models import Page


def complete(request, page_to_render):
    try:
        p = Page.objects.get(slug=page_to_render, public=True)
    except Page.DoesNotExist:
        raise http.Http404('%s page requested but not found' % page_to_render)

    return render_to_response("page.html",
                              {"request": request, "page": p,},
                              context_instance=RequestContext(request)
                              )


def clone_questionnaire(request, questionnaire_id):


    q_original = Questionnaire.objects.get(id=questionnaire_id)
    q = q_original
    q.pk = None
    q.save()
    q.name = q.name + " -"+ str(q.id)
    q.save()

    q_original = Questionnaire.objects.get(id=questionnaire_id)



    for qs in q_original.questionsets():
        qs_original_id = qs.id
        qs.pk = None
        # qs.save()
        qs.questionnaire = q
        qs.save()
        qs_original = QuestionSet.objects.get(id=qs_original_id)

        for question in qs_original.questions():
            question.pk = None
            question.save()
            question.questionset = qs
            question.save()

    return render_to_response("page.html",
                              {"request": request, "page": 1,},
                              context_instance=RequestContext(request)
                              )
