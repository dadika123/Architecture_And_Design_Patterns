from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    Renders template via template name and with custom kwargs
    :param template_name: name of the template
    :param folder: templates folder, default is "templates'
    :param kwargs: template kwargs
    :return: rendered template
    """
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)


class DefaultIndex:
    """Default index view"""

    def __call__(self, *args, **kwargs):
        return '200 Success', 'Welcome to my custom framework!'


class PageNotFound404:
    """Default 404 view"""

    def __call__(self, *args, **kwargs):
        return '404 Page Not Found', render('404.html', 'wunderbar/default_templates')
