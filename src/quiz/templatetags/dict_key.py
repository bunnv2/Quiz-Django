from django import template
from django.template.defaultfilters import register

register = template.Library()


@register.filter(name="dict_key")
def dict_key(dictionary, key):
    """Returns the given key from a dictionary."""
    return dictionary.get(key, None)
