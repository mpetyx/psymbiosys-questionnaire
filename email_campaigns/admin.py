__author__ = 'mpetyx'

from django.contrib import admin
from django.db import models
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from signals import *


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(Campaign, CampaignAdmin)



class CloneQuestionnaireManager(models.Manager):
    def get_queryset(self):
        return super(CloneQuestionnaireManager, self).get_queryset()


class CloneQuestionnaire(Questionnaire):
    class Meta:
        proxy = True

    objects = CloneQuestionnaireManager()


class CloneQuestionnaireAdmin(admin.ModelAdmin):
    pass


admin.site.register(CloneQuestionnaire, CloneQuestionnaireAdmin)


# custom views

def CloneQuestionnaire_update(request, id):
    if not request.user.is_superuser:
        return HttpResponse('Only administrators can edit CloneQuestionnaire requests', status=401)

    q_original = get_object_or_404(Questionnaire, id=id)
   

    # q_original = Questionnaire.objects.get(id=id)
    q = q_original
    q.pk = None
    q.save()
    q.name = q.name + " -" + str(q.id)
    q.save()

    q_original = Questionnaire.objects.get(id=id)

    for qs in q_original.questionsets():
        qs_original_id = qs.id
        qs.pk = None
        # qs.save()
        qs.questionnaire = q
        qs.save()
        qs_original = QuestionSet.objects.get(id=qs_original_id)

        for question in qs_original.questions():
            original_question_id = question.id
            question.pk = None
            question.save()
            question.questionset = qs
            question.save()

            for choice in Question.objects.get(id=original_question_id).choices():
                choice.pk = None
                choice.save()
                choice.question = question
                choice.save()

    return redirect('/admin/email_campaigns/clonequestionnaire/')


def clone_CloneQuestionnaire(request, id):
    """
    Clone a CloneQuestionnaire request
    """
    return CloneQuestionnaire_update(request, id)
