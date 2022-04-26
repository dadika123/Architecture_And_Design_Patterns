from views import Index, Contact, Categories, CreateCategory, Courses, CategoryCourses, CreateCourse, CopyCourse

routes = {
    '/': Index(),
    '/contact/': Contact(),
    '/categories/': Categories(),
    '/courses/': Courses(),
    '/create-category/': CreateCategory(),
    '/category-courses/': CategoryCourses(),
    '/create-course/': CreateCourse(),
    '/copy-course/': CopyCourse()
}
