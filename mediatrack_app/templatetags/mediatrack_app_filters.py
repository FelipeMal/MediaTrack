from django import template

register = template.Library()

@register.filter
def minutes_to_hh_mm(total_minutes):
    if total_minutes is None:
        return "--:--"
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours}:{minutes:02d}" 