from django.conf.urls import *
from views import *
from questionnaire.excel import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test, login_required

anonymous_required = user_passes_test(lambda u: u.is_anonymous(), '/analytics/')
urlpatterns = patterns(
    '',
    url(r'^$', login_required(index),  name='index'
    ),
    url(r'^login/$', anonymous_required(auth_views.login),
        {
            'template_name': 'questionnaire/analytics/login.html'
        },
        name='login'
    ),
    url(r'^logout/$', login_required(auth_views.logout_then_login), {
        'login_url': '/analytics/login/'
    },
        name='logout'
    ),

    url(r'^workers-sentiment/$', login_required(workers_sentiment), name='workers-sentiment'),
    url(r'^brand-value/$', login_required(brand_value), name='brand-value'),

    url(r'^brand-value-charts/$', login_required(brand_value_charts),
        name='brand-value-charts'
    ),
    url(r'^brand-value-stats/$', login_required(brand_value_stats),
        name='brand-value-stats'
    ),
    url(r'^workers-sentiment-charts/(?P<part>[0-9]+)/', login_required(workers_sentiment_charts),
        name='workers-sentiment-charts'
    ),
    url(r'^workers-sentiment-stats/(?P<part>[0-9]+)/', login_required(workers_sentiment_stats),
        name='workers-sentiment-stats'
    ),
    url(r'^workers-sentiment-export/', login_required(workers_sentiment_detailed_results),
        name='workers-sentiment-detailed-results'
    ),
    url(r'^brand-values-export/', login_required(brand_values_detailed_results),
        name='brand-values-detailed-results'
    )
)