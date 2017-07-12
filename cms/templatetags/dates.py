import datetime
from django import template

register = template.Library()

@register.filter(name='date_to_day')
def date_to_weekday(date):
    """
    Accpets datetime.date() object and turn it to week day.
    Precondition: Week starts with saturday.
    """
    days = [0, 'الاتنين', 'التلات', 'الأربع', 'الخميس', 'الجمعة', 'السبت', 'الحد', ]
    if datetime.date.today() == date:
        return 'النهاردة'
    return days[date.isoweekday()]
