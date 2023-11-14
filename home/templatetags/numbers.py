from django import template

register = template.Library()

def format_number(value):
    return f"{value:,}"


def format_number1(value):
    return f"{value:.1f}"

def format_number2(value):
    return f"{value[:4]}"


register.filter('format_number', format_number)
register.filter('format_number1', format_number1)
register.filter('format_number2', format_number2)