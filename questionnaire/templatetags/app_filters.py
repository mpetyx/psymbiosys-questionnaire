__author__ = 'mpetyx'


from django import template


register = template.Library()


@register.filter
def get_admin_results(cl):
    return cl.result_list

@register.filter
def qtext_parse(txt, part):
    return txt.split('-')[int(part)].strip()

@register.filter
def contains(txt, part):
    return part.lower() in txt.lower()

@register.filter
def split_brand_value(txt, part):
    return txt.split(' - ')[int(part)]