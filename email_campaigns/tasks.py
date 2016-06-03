__author__ = 'mpetyx'

from celery import shared_task
from celery.utils.log import get_task_logger
from celery.schedules import crontab
import celery
logger = get_task_logger(__name__)
import datetime
from questionnaire.models import RunInfoHistory, Subject, RunInfo
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from datetime import date
import os
from datetime import timedelta
from .models import Campaign
from questionnaire.views import *
from django.contrib.sites.models import Site
from django.template import loader
from django.core.mail import send_mail


current_site = Site.objects.all()[0].name



def generate_campaign_run( questionnaire_id, subject_id=None):

    qu = get_object_or_404(Questionnaire, id=questionnaire_id)
    qs = qu.questionsets()[0]

    if subject_id is not None:
        # su = get_object_or_404(Subject, email=subject_id)
        su = Subject.objects.get_or_create(email=subject_id)
        su = su[0]
        su.save()
    else:
        su = Subject.objects.filter(givenname='Anonymous', surname='User')[0:1]
        if su:
            su = su[0]
        else:
            su = Subject(givenname='Anonymous', surname='User')
            su.save()

    str_to_hash = "".join(map(lambda i: chr(random.randint(0, 255)), range(16)))
    str_to_hash += settings.SECRET_KEY
    key = md5(str_to_hash).hexdigest()

    run = RunInfo(subject=su, random=key, runid=key, questionset=qs)
    run.save()

    questionnaire_start.send(sender=None, runinfo=run, questionnaire=qu)

    return str(current_site)+"/q/%s/"%key

def retrieve_campaign_run( questionnaire_id, subject):



    qu = get_object_or_404(Questionnaire, id=questionnaire_id)
    qs = qu.questionsets()[0]

    if RunInfo.objects.filter(subject__email=subject, questionset=qs):
        run_key = RunInfo.objects.get(subject__email=subject, questionset=qs).runid

        return str(current_site)+"/q/%s/"%run_key
    else:
        return generate_campaign_run(questionnaire_id, subject)




@shared_task(ignore_result=True)
def send_email_alert(email, questionnaire):
    subject = "You should Complete your Questionaire!"
    to = [email]
    from_email = 'forgot_questionaires@apis.technology'



    ctx = {
        # 'user': str(user.first_name+ " "+user.last_name),
        # 'invoice_id': invoice_id,
        # 'amount' : amount,
        # 'overall_balance':balance,
        # 'billing_date':str(date.today())
        'questionnaire':str(questionnaire)
    }

    message = get_template('mails/questionaire.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    # msg.content_subtype = "html"
    # msg.send()


    html_message = loader.render_to_string(
        'mails/questionaire.html',
        {
            'questionnaire':str(questionnaire)
    }
    )

    send_mail(subject, message, from_email, to, fail_silently=True, html_message=html_message)

    return True

@shared_task(ignore_result=True)
def send_email_campagin(email, qu):
    subject = "You should Complete your Questionaire!"
    to = [email]
    from_email = 'welcome_questionaires@apis.technology'



    ctx = {
        # 'user': str(user.first_name+ " "+user.last_name),
        # 'invoice_id': invoice_id,
        # 'amount' : amount,
        # 'overall_balance':balance,
        'qu':str(qu)
    }

    message = get_template('mails/welcome_questionaire.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

    return True

@shared_task(ignore_result=True)
def start_campaign(emails):

    for email in emails:
        send_email_campagin.delay(email)




# @celery.decorators.periodic_task(run_every=crontab(day_of_month=[1,15]),ignore_result=True,name="task_check_who_filled_the_questionaire",)
@celery.decorators.periodic_task(run_every=timedelta(seconds=30),ignore_result=True,name="task_check_who_filled_the_questionaire",)
def check_who_filled_the_questionaire():
    for campaign in Campaign.objects.all():
        questionnaires = campaign.questionnaires.all()
        for questionnaire in questionnaires:
            emails = campaign.emails
            for email in emails:
                if not RunInfoHistory.objects.filter(subject__email=email,questionnaire=questionnaire):

                    send_email_alert.delay(email,retrieve_campaign_run(questionnaire.id,email))

# from email_campaigns.tasks import send_email
# send_email("mpetyx@me.com")
