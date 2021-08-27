from django import template
import datetime
register = template.Library()


@register.filter(name='fromunix')
def fromunix(value):
    try:
        new_value = datetime.datetime.fromtimestamp(int(value))
    except:
        new_value = None
    return new_value


@register.filter
def replace_screenshot(value):
    return value.replace('t_thumb', 't_screenshot_huge')

