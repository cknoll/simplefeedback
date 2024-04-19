from django import template
import markdown

register = template.Library()


@register.filter
def render_markdown(txt):

    if txt is None:
        txt = ""
    return markdown.markdown(txt)
