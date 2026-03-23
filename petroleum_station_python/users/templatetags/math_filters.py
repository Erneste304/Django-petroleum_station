from django import template

register = template.Library()


@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return 0

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except ValueError:
        return 0

@register.filter
def replace(value, arg):
    """Replaces all occurrences of the first character in arg with the second character."""
    try:
        if ',' in arg:
            old, new = arg.split(',', 1)
            return value.replace(old, new)
        return value
    except:
        return value
