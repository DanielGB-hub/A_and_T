from daniel_framework.templator import render
from patterns.сreational_patterns import Engine, Logger
from datetime import date
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, \
    TemplateView, ListView, CreateView, BaseSerializer

site = Engine()
logger = Logger('main')

routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', data_month=request.get('data_month', None))


@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html',  data=request.get('data', None))


@AppRoute(routes=routes, url='/input/')
class Input:
    @Debug(name='Input')
    def __call__(self, request):
        return '200 OK', render('input.html',  data=request.get('data', None))


@AppRoute(routes=routes, url='/editor/')
class Editor:
    def __call__(self, request):
        return '200 OK', render('editor.html', objects_list=site.categories)


class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@AppRoute(routes=routes, url='/contacts/')
class Contacts:
    @Debug(name='Contacts')
    def __call__(self, request):
        return '200 OK', render('contacts.html')


# контроллер - Расписания
# class StudyPrograms:
#     def __call__(self, request):
#         return '200 OK', render('study-programs.html', data=date.today())


# контроллер - список курсов
@AppRoute(routes=routes, url='/courses-list/')
class CoursesList:
    @Debug(name='CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html', objects_list=category.courses, name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать курс
@AppRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @Debug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            type_ = data['type_']
            type_ = site.decode_value(type_)

            teacher = data['teacher']
            teacher = site.decode_value(teacher)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course(type_, name, category, teacher)
                site.courses.append(course)

            return '200 OK', render('course_list.html', objects_list=category.courses,
                                    name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - создать категорию
@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @Debug(name='CreateCategory')
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('editor.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


# контроллер - список категорий
@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', objects_list=site.categories)


# контроллер - копировать курс
@AppRoute(routes=routes, url='/copy-course/')
class CopyCourse:
    @Debug(name='CopyCourse')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('course_list.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать категорию "Преподаватель" (Teacher)

# class AddTeacher:
#     @Debug(name='AddTeacher')
#     def __call__(self, request):
#         if request['method'] == 'POST':
#             # метод пост
#             data = request['data']
#
#             firstname = data['firstname']
#             firstname = site.decode_value(firstname)
#
#             teachers = None
#             lastname = data['lastname']
#             lastname = site.decode_value(lastname)
#             user = site.create_user('teacher', firstname, lastname)
#             site.teachers.append(user)
#
#             return '200 OK', render('course_list.html', objects_list=teachers.user,
#                                     firstname=teachers.firstname, lastname=teachers.lastname)


# @AppRoute(routes=routes, url='/teacher-list/')
# class TeacherListView(ListView):
#     queryset = site.teachers
#     template_name = 'teacher_list.html'


# @AppRoute(routes=routes, url='/create-teacher/')
# class TeacherCreateView(CreateView):
#     @Debug(name='CreateTeacher')
#     def __call__(self, request):
#         template_name = 'create_teacher.html'
#
#     #def create_obj(self, data: dict):
#     def create_obj(self, request):
#         if request['method'] == 'POST':
#             data = request['data']
#             firstname = data['firstname']
#             firstname = site.decode_value(firstname)
#
#             teachers = None
#             lastname = data['lastname']
#             lastname = site.decode_value(lastname)
#             teacher = site.create_user('teacher', firstname, lastname)
#             site.teachers.append(teacher)
#
#             return '200 OK', render('teacher_list.html', objects_list=teachers.teacher,
#                                     firstname=teachers.firstname, lastname=teachers.lastname)

        # name = data['name']
        # name = site.decode_value(name)
        # new_obj = site.create_user('teacher', name)
        # site.students.append(new_obj)


# @AppRoute(routes=routes, url='/add-student/')
# class AddStudentByCourseCreateView(CreateView):
#     template_name = 'add_student.html'
#
#     def get_context_data(self):
#         context = super().get_context_data()
#         context['courses'] = site.courses
#         context['students'] = site.students
#         return context
#
#     def create_obj(self, data: dict):
#         course_name = data['course_name']
#         course_name = site.decode_value(course_name)
#         course = site.get_course(course_name)
#         student_name = data['student_name']
#         student_name = site.decode_value(student_name)
#         student = site.get_student(student_name)
#         course.add_student(student)


@AppRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'


@AppRoute(routes=routes, url='/create-student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        firstname = data['firstname']
        firstname = site.decode_value(firstname)
        lastname = data['lastname']
        lastname = site.decode_value(lastname)
        new_obj = site.create_user('student', firstname, lastname)

        site.students.append(new_obj)


@AppRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        course.add_student(student)