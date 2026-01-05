from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    """Return the field rendered with the given CSS class appended to any existing classes.

    Usage in template:
        {{ form.my_field|add_class:"form-control" }}
    """
    # Copy existing widget attrs to avoid mutating the shared widget instance
    try:
        widget_attrs = dict(field.field.widget.attrs)
    except Exception:
        widget_attrs = {}

    existing = widget_attrs.get('class', '')
    if existing:
        widget_attrs['class'] = f"{existing} {css}".strip()
    else:
        widget_attrs['class'] = css

    return field.as_widget(attrs=widget_attrs)
