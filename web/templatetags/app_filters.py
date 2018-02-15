from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import CommonMark

register = template.Library()


@register.filter
@stringfilter
def markdownyfy(text):
    return mark_safe(CommonMark.commonmark(text))
