import os
import sys
import copy
from datetime import datetime
import quopri


class User:
    pass


class Teacher(User):
    pass


class Student(User):
    pass


class UserFactory:
    _types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_):
        if type_ not in cls._types:
            raise AttributeError(f'Wrong User type. Can be one of: {", ".join(cls._types)}')
        return cls._types[type_]()


class CoursePrototype:

    def clone(self):
        return copy.deepcopy(self)


class Course(CoursePrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class Category:
    _cur_id = 0

    def __init__(self, name, category):
        self.id = self.__class__._cur_id
        self.__class__._cur_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class CourseFactory:
    _types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        if type_ not in cls._types:
            raise AttributeError(f'Wrong course type. Can be one of: {", ".join(cls._types)}')
        return cls._types[type_](name, category)


class Engine:
    def __init__(self):
        self.teachers = set()
        self.students = set()
        self.courses = set()
        self.categories = set()

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id_):
        items = [cat for cat in self.categories if cat.id == id_]
        return items[0] if items else None

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):
        items = [course for course in self.courses if course.name == name]
        return items[0] if items else None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = quopri.decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        name = ''
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):
    _default_log_path = f'{os.path.dirname(sys.argv[0])}/logs'

    def __init__(self, name):
        self.name = name
        if not os.path.exists(self._default_log_path):
            os.mkdir(self._default_log_path)
        self.filepath = f'{self._default_log_path}/{self.name}.txt'

    @staticmethod
    def _append_dt_to_txt(text: str):
        dt_str = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        return f'{dt_str}: {text}'

    @staticmethod
    def _save_file(filepath: str, text: str):
        with open(filepath, 'a+') as f:
            f.write(f'{text}\n')

    def debug(self, text):
        debug_text = self._append_dt_to_txt(f'DEBUG: {text}')
        print(debug_text)
        self._save_file(self.filepath, debug_text)

    def log(self, text):
        log_text = self._append_dt_to_txt(f'LOG: {text}')
        print(log_text)
        self._save_file(self.filepath, log_text)

    def error(self, text):
        error_text = self._append_dt_to_txt(f'ERROR: {text}')
        print(error_text)
        self._save_file(self.filepath, error_text)
