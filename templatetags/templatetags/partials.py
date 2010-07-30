from django.template import Library, Node, Variable, loader
from django.template.context import Context

register = Library()

class PartialTemplateNode(Node):
  def __init__(self, template_name, context_item):
    self.template_name = template_name
    self.context_item = Variable(context_item)

  def render(self, context):
    template = loader.get_template('partials/%s.html' % (self.template_name,))
    item = self.context_item.resolve(context)
    template_context = Context({
      'item': item
    })
    return template.render(template_context)

@register.tag(name='render_partial')
def partial_template(parser, token):
  tag, template_name, context_item = token.split_contents()
  return PartialTemplateNode(template_name, context_item)
