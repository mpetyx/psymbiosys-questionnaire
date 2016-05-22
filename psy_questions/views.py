__author__ = 'mpetyx'

from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from django import http
from django.utils import translation
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