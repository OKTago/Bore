from django import template
register = template.Library()

DOJO_VERSION = "1.5"
DOJO_THEME = "claro"

@register.inclusion_tag('dojo.html')
def dojo_include():
    return {'DOJO_VERSION': DOJO_VERSION, 'DOJO_THEME': DOJO_THEME}

