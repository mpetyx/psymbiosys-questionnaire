__author__ = 'mpetyx'

from tasks import *





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