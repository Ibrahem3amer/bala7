from django import template

register = template.Library()

@register.filter(name='dynamic_index')
def dynamic_index(list_instance, index):
    """
    Accepts a list of weeks materials and return a specific index according to week_number value.
    """
    try:
        return list_instance[index]
    except:
        return ''