from django.conf.urls import *
from views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import user_passes_test, login_required

anonymous_required = user_passes_test(lambda u: u.is_anonymous(), '/anlzer/projects')
urlpatterns = patterns(
    '',
    url(r'^login/$', anonymous_required(auth_views.login),
        {
            'template_name': 'questionnaire/analytics/login.html'
        },
        name='login'
        ),
    url(r'^logout/$', login_required(auth_views.logout_then_login), {
        'login_url': '/analytics/login/'
    },
        name='logout'),
)