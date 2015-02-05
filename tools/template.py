__author__ = 'Tang'
from jinja2 import Environment, PackageLoader, TemplateNotFound
from conf import TEMPLATE_PATH

env = Environment(loader=PackageLoader('tools', TEMPLATE_PATH))


def render(template_path, **kwargs):
    try:
        template = env.get_template(template_path)
    except TemplateNotFound:
        return None

    return template.render(**kwargs)