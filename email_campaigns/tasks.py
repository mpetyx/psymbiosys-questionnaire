# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random

from django.shortcuts import get_object_or_404
from hashlib import md5

__author__ = 'mpetyx'

import celery
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
from django.template import Context
from django.template.loader import get_template
from django.core.mail import EmailMessage
from datetime import timedelta, datetime
from questionnaire.models import *
from django.contrib.sites.models import Site
from django.template import loader
from django.core.mail import send_mail
from questionnaire import questionnaire_start


current_site = Site.objects.all()[0].name


def generate_campaign_run(questionnaire_id, email=None, campaign_id=None):
    qu = get_object_or_404(Questionnaire, id=questionnaire_id)
    qs = qu.questionsets()[0]

    str_to_hash = "".join(map(lambda i: chr(random.randint(0, 255)), range(16)))
    str_to_hash += settings.SECRET_KEY
    key = md5(str_to_hash).hexdigest()

    if email is not None:
        su = Subject.objects.filter(email__iexact=email)
        if su.exists():
            su = su[0]
        else:
            su = Subject.objects.create(email=email)
    else:
        su = Subject(givenname=key, surname='Anonymous User')
        su.save()

    run = RunInfo(subject=su, random=key, runid=key, questionset=qs, campaign_id=campaign_id)
    run.save()

    questionnaire_start.send(sender=None, runinfo=run, questionnaire=qu)

    return str(current_site) + "/q/%s/" % key


def retrieve_campaign_run(questionnaire_id, email, campaign_id):
    """
    This creates a link that will be added on the button of the template you received via email
    """
    qu = get_object_or_404(Questionnaire, id=questionnaire_id)
    qs = qu.questionsets()[0]

    potential_run_info = RunInfo.objects.filter(
        subject__email=email,
        questionset=qs,
        campaign_id=campaign_id
    )

    if potential_run_info.exists():
        return str(current_site) + "/q/%s/" % potential_run_info[0].runid
    else:
        return generate_campaign_run(questionnaire_id, email, campaign_id)


@shared_task(ignore_result=True)
def send_email_alert(email, questionnaire):
    subject = "Give us your perspective for the brand values of the AIDIMME workplace !"
    to = [email]
    from_email = 'aidimme-questionnaires@psymbiosys.info'

    ctx = {
        # 'user': str(user.first_name+ " "+user.last_name),
        # 'invoice_id': invoice_id,
        # 'amount' : amount,
        # 'overall_balance':balance,
        # 'billing_date':str(date.today())
        'questionnaire': str(questionnaire)
    }

    message = get_template('mails/questionaire.html').render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    # msg.content_subtype = "html"
    # msg.send()


    html_message = loader.render_to_string(
        'mails/questionaire.html',
        {
            'questionnaire': str(questionnaire)
        }
    )

    send_mail(subject, message, from_email, to, fail_silently=True, html_message=html_message)

    return True


@shared_task(ignore_result=True)
def send_email_campaign(email, url, questionnaire, campaign):
    subject = "Give us your perspective for the %s in the %s !" % (
        questionnaire.type.replace('_', ' ').title(),
        campaign.name
    )
    to = [email]
    from_email = 'aidimme-questionnaires@psymbiosys.info'

    ctx = {
        'url': url,
        'questionnaire': questionnaire,
        'campaign': campaign
    }

    html_template = 'mails/%s.html' % (questionnaire.type.lower())

    message = get_template(html_template).render(Context(ctx))
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    # msg.content_subtype = 'html'
    # msg.send()

    html_message = loader.render_to_string(html_template, {
        'questionnaire': questionnaire,
        'campaign': campaign,
        'url': url
    })

    send_mail(subject, message, from_email, to, fail_silently=True, html_message=html_message)

    return True


def a_campaign_modified(instance):
    campaign = instance

    questionnaires = campaign.questionnaires.all()
    for questionnaire in questionnaires:
        emails = list(campaign.users.values_list('email', flat=True))
        emails.append(campaign.director.email)
        for email in emails:
            print 'Started email sending on: %s' % email

            run_info = RunInfo.objects.filter(
                subject__email=email,
                questionset__questionnaire=questionnaire,
                campaign_id=campaign.id
            )
            run_info_history = RunInfoHistory.objects.filter(
                subject__email=email,
                questionnaire=questionnaire,
                campaign_id=campaign.id
            )

            if (not run_info_history.exists() and not run_info.exists()) or (run_info.exists() and not bool(run_info[0].emailsent)):

                print 'Ok, sending an email to: %s' % email
                campaign_run = retrieve_campaign_run(questionnaire.id, email, campaign.id)
                if run_info.exists():
                    run_info_instance = run_info[0]
                    run_info_instance.emailsent = datetime.now()
                    run_info_instance.save()

                send_email_campaign(email, str(campaign_run), questionnaire, campaign)




