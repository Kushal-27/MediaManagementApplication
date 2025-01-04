from django import template
import os

register = template.Library()

@register.filter
def splitext(value):
    """Split the file path into base name and extension."""
    return os.path.splitext(value)[-1].lstrip('.')
