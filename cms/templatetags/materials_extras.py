from django import template

register = template.Library()

@register.filter(name='week_number')
def get_week_number(week_materials, week_number):
    """
    Accepts a list of weeks materials and return a specific index according to week_number value.
    """
    return week_materials[week_number]