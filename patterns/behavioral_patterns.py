from abc import ABC, abstractmethod

import jsonpickle

from wunderbar.templating import render


class Observer(ABC):
    """Abstract observer class"""

    @abstractmethod
    def update(self, course):
        """
        Abstract method to update observers about the course changes
        :param course: observed course
        """
        pass


class CourseNotifier:
    """Course notifier class"""

    def __init__(self):
        self.observers = []

    def notify(self):
        """Notifies course observers"""
        for item in self.observers:
            item.update(self)


class SmsSender(Observer):
    """SMS sender observer"""

    def update(self, course):
        """
        Updates SMS observers via SMS
        :param course: observed course
        """
        print(f'SMS: user {course.students[-1].name} joined course {course.name}')


class EmailSender(Observer):
    """Email sender observer"""

    def update(self, course):
        """
        Updates Email observers via Email
        :param course: observed course
        """
        print(f'EMAIL: user {course.students[-1].name} joined course {course.name}')


# поведенческий паттерн - Шаблонный метод
class TemplateView:
    """Base template view"""
    template_name = 'template.html'

    def get_context_data(self) -> dict:
        """
        Gets context data
        :return: context data
        """
        return {}

    def get_template(self) -> str:
        """
        Gets template name
        :return: template name
        """
        return self.template_name

    def render_template_with_context(self):
        """
        Renders template with context
        :return: status code, view
        """
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        """
        Renders template with context
        :return: status code, view
        """
        return self.render_template_with_context()


class ListView(TemplateView):
    """List view"""
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self) -> list:
        """
        Gets queryset
        :return: queryset
        """
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self) -> str:
        """
        Gets object context name
        :return: object context name
        """
        return self.context_object_name

    def get_context_data(self):
        """
        Gets context data with query set
        :return: context data
        """
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView, ABC):
    """Create view"""
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request: dict):
        """
        Gets request data from request
        :param request: request
        :return: request data
        """
        return request['data']

    @abstractmethod
    def create_obj(self, data: dict):
        """
        Abstract method to create object from data
        :param data: creation data
        """
        pass

    def __call__(self, request):
        """
        Returns a page on GET and creates an object on POST requests
        :param request: request
        :return: status code, view
        """
        if request['method'] == 'POST':
            # метод пост
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)


class Writer(ABC):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def write(self, text):
        pass


class ConsoleWriter(Writer):
    """Basic console writer"""

    def write(self, text):
        """Writes text to console"""
        print(text)


class FileWriter(Writer):
    """Basic file writer"""

    def __init__(self, file_name, **kwargs):
        super().__init__(**kwargs)
        self.file_name = file_name

    def write(self, text):
        """Writes text to end of file"""
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')
