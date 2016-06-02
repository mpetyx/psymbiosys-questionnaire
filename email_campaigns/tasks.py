__author__ = 'mpetyx'

from celery import shared_task
from celery.utils.log import get_task_logger
from celery.schedules import crontab
import celery
logger = get_task_logger(__name__)
import datetime
from questionnaire.models import RunInfoHistory, Subject
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from datetime import date
import os
from .models import Campaign


@shared_task(ignore_result=True)
def send_email_alert(email):
    subject = "You should Complete your Questionaire!"
    to = [email]
    from_email = 'forgot_questionaires@apis.technology'



    ctx = {
        # 'user': str(user.first_name+ " "+user.last_name),
        # 'invoice_id': invoice_id,
        # 'amount' : amount,
        # 'overall_balance':balance,
        # 'billing_date':str(date.today())
    }

    message = get_template('mails/questionaire.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.content_subtype = 'html'
    msg.send()

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




@celery.decorators.periodic_task(run_every=crontab(day_of_month=[1,15]),ignore_result=True,name="task_check_who_filled_the_questionaire",)
def check_who_filled_the_questionaire():
    for campaign in Campaign.objects.all():
        questionnaires = campaign.questionnaires.all()
        for questionnaire in questionnaires:
            emails = campaign.emails
            for email in emails:
                if not RunInfoHistory.objects.filter(subject__email=email,questionnaire=questionnaire):
                    send_email_alert.delay(email,questionnaire)

# from email_campaigns.tasks import send_email
# send_email("mpetyx@me.com")
