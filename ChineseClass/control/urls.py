from django.conf.urls import url, include
from . import views

urlpatterns = [

    url(r'show_schools$', views.show_schools, ),
    url(r'del_teacher$', views.del_teacher, ),
    url(r'show_teachers$', views.show_teachers, ),
    url(r'show_questions$', views.show_questions, ),
    url(r'show_students$', views.show_students, ),
]