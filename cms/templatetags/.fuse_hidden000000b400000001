from django import template

register = template.Library()

@register.filter(name='week_number')
def get_week_number(week_materials, week_number):
    """
    Accepts a list of weeks materials and return a specific index according to week_number value.
    """
    return week_materials[week_number]

@register.filter(name='get_table_list')
def get_table_list(user_table):
    """Calls to_list() of given string."""
    try:
        return user_table.to_list(user_table.topics)
    except:
        return []

@register.filter(name='dynamic_index')
def dynamic_index(list_instance, index):
    """
    Accepts a list of weeks materials and return a specific index according to week_number value.
    """
    try:
        return list_instance[index]
    except:
        return ''