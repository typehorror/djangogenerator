from django import template

register = template.Library()

def var(parser, token):
    tokens = token.split_contents()
    tag_name, parameters = tokens[0], tokens[1:]
    return VarNode(parameters)

class VarNode(template.Node):
    def __init__(self, content):
        self.content = content
    def render(self, context):
        return u"{{ %s }}" % ' '.join(self.content)
register.tag('var', var)

def tag(parser, token):
    tokens = token.split_contents()
    tag_name, parameters = tokens[0], tokens[1:]
    return TagNode(parameters)

class TagNode(template.Node):
    def __init__(self, content):
        self.content = content
    def render(self, context):
        return u"{%% %s %%}" % ' '.join(self.content)

register.tag('tag', tag)


