from patterns.creational_patterns import Engine, Logger
from patterns.structural_patterns import route, method_debug, BaseSerializer
from patterns.behavioral_patterns import SmsSender, EmailSender, ListView, CreateView, TemplateView, ConsoleWriter, \
    FileWriter
from wunderbar.templating import render

site = Engine()
logger = Logger('main', [ConsoleWriter, FileWriter])
sms_sender = SmsSender()
email_sender = EmailSender()
routes = {}


@route(routes, '/')
class Index(TemplateView):
    """Index view"""
    template_name = 'index.html'


@route(routes, '/contact/')
class Contact(TemplateView):
    """Contact view"""
    template_name = 'contact.html'


@route(routes, '/categories/')
class Categories(ListView):
    """Categories view"""
    queryset = site.categories
    template_name = 'categories.html'


@route(routes, '/create-category/')
class CreateCategory(CreateView):
    """Category creation view"""
    template_name = 'create-category.html'

    def create_obj(self, data: dict):
        name = site.decode_value(data['name'])
        category = None
        if category_id := data.get('category_id'):
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.add(new_category)
        logger.log(f'Category "{name}" was created')


@route(routes, '/courses/')
class Courses(ListView):
    """Courses view"""
    queryset = site.courses
    template_name = 'courses.html'


@route(routes, '/category-courses/')
class CategoryCourses:
    """Category courses view"""

    @method_debug
    def __call__(self, request):
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            logger.log(f'Category "{category.name}" courses render was called with courses: '
                       f'{", ".join([course.name for course in category.courses])}')
            return '200 OK', render('category-courses.html', objects_list=category.courses, name=category.name,
                                    id=category.id)
        except KeyError:
            logger.error('No courses have been added yet')
            return '400 Bad Request', 'No courses have been added yet'


@route(routes, '/create-course/')
class CreateCourse:
    """Create course view"""
    category_id = None

    @method_debug
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            if self.category_id is not None:
                category = site.find_category_by_id(self.category_id)

                new_course = site.create_course('record', name, category)
                new_course.observers.append(email_sender)
                new_course.observers.append(sms_sender)
                site.courses.add(new_course)

                logger.log(f'Course "{name}" was created')

                return '200 OK', render('category-courses.html', objects_list=category.courses, name=category.name,
                                        id_=category.id)
            return '400 Bad Request', 'Course Category was not specified'
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(self.category_id)
                logger.log(f'Courses creation for category {category} was rendered')

                return '200 OK', render('create-course.html', name=category.name, id=category.id)
            except KeyError:
                logger.error('Either no category ID was provided or the category does not exist')
                return '400 Bad Request', 'Either no category ID was provided or the category does not exist'


@route(routes, '/copy-course/')
class CopyCourse:
    """Copy Course view"""

    @method_debug
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                old_course.category.courses.append(new_course)
                site.courses.add(new_course)

                logger.log(f'Course "{name}" was copied')

            return '200 OK', render('courses.html', objects_list=site.courses)
        except KeyError:
            logger.error('No courses have been added yet')
            return '400 Bad Request', 'No courses have been added yet'


@route(routes, url='/students/')
class Students(ListView):
    queryset = site.students
    template_name = 'students.html'


@route(routes, url='/create-student/')
class StudentCreate(CreateView):
    template_name = 'create-student.html'

    def create_obj(self, data: dict):
        name = site.decode_value(data['name'])
        new_student = site.create_user('student', name)
        site.students.add(new_student)


@route(routes, url='/add-student/')
class AddStudentToCourse(CreateView):
    template_name = 'add-student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = site.decode_value(data['course_name'])
        course = site.get_course(course_name)
        student_name = site.decode_value(data['student_name'])
        student = site.get_student(student_name)
        course.add_student(student)


@route(routes=routes, url='/api/courses/')
class CourseApi:
    """Course API resource"""

    @method_debug
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).dump()
