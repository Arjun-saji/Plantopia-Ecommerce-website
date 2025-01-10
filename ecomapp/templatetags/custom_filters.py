from django import template

register=template.Library()


@register.filter
def multiply(value,arg):

	return value*arg


@register.filter(name='add_value')
def add_value(value, arg):
    """Adds the given value to the argument."""
    try:
        return value + arg
    except (ValueError, TypeError):
        return 0 