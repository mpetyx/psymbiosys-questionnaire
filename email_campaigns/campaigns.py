__author__ = 'mpetyx'

from questionnaire.views import *
from django.contrib.sites.models import Site
from tasks import send_email_campagin

current_site = Site.objects.all()[0].name

def generate_campaign_run( questionnaire_id, subject_id=None):

    qu = get_object_or_404(Questionnaire, id=questionnaire_id)
    qs = qu.questionsets()[0]

    if subject_id is not None:
        su = get_object_or_404(Subject, pk=subject_id)
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

    return str(current_site)+"q/%s/"%key



def campagin_from_a_list_of_mails(questionnaire_id,mails):
    for mail in mails:
        su = Subject.objects.filter( email=mail)

        if not su:
            su = Subject.objects.filter(email=mail)
            su.save()

        qu = generate_campaign_run(questionnaire_id,su.id)
        send_email_campagin.delay(su.email,qu=qu)



# from email_campaigns.campaigns import generate_run
# generate_run(1,2)