from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from views import clone_questionnaire
from email_campaigns.admin import clone_CloneQuestionnaire
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'q/', include('questionnaire.urls')),
    url(r'analytics/', include('questionnaire.analytics_urls')),

    url(r'^take/(?P<questionnaire_id>[0-9]+)/$', 'questionnaire.views.generate_run'),
    url(r'^$', 'questionnaire.page.views.page', {'page_to_render' : 'index'}),
    url(r'^(?P<lang>..)/(?P<page_to_trans>.*)\.html$', 'questionnaire.page.views.langpage'),
    url(r'^(?P<page_to_render>.*)\.html$', 'questionnaire.page.views.page'),
    url(r'^setlang/$', 'questionnaire.views.set_language'),

    url(r'^complete/$', 'psy_questions.views.complete', {'page_to_render' : 'complete'}),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^clone/(?P<questionnaire_id>[0-9]+)/$', 'psy_questions.views.clone_questionnaire'),
    url(r'^admin_clone/(?P<id>.*)/$', clone_CloneQuestionnaire),
    url(r'^csv/(?P<qid>\d+)/$',
        'questionnaire.views.export_csv', name='export_csv'),
)#+ static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
