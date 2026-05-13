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
    """
    Replaces all occurrences of the substring before the first comma in 'arg'
    with the substring after it within the 'value' string.
    Example: {{ "hello world"|replace:"o,x" }} would output "hellx wxrld"
    """
    # Ensure value is a string for the replace method
    if not isinstance(value, str):
        value = str(value)

    # Ensure arg is a string and contains a comma for the split operation
    if isinstance(arg, str) and ',' in arg:
        old, new = arg.split(',', 1)
        return value.replace(old, new)

    # If arg is not a string or doesn't contain a comma, return the original value
    return value
