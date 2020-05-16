from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'login$', views.login, ),
    url(r'register$', views.register, ),
    url(r'show_students$', views.show_students, ),
    url(r'show_questions$', views.show_questions, ),
    url(r'show_questions_method2$', views.show_questions_method2, ),
    url(r'show_classes$', views.show_classes, ),
    url(r'show_class_infor$', views.show_class_infor),
    url(r'add_questions$', views.add_questions, ),
    url(r'create_class$', views.create_class, ),
    url(r'assign_homework_by_number$', views.assign_homework_by_number, ),
    url(r'show_information$', views.show_information, ),
    url(r'show_question_bank$', views.show_question_bank, ),
    url(r'show_question_bank_infor$', views.show_question_bank_infor, ),
    url(r'create_question_bank$', views.create_question_bank, ),
    url(r'insert_question_bank$', views.insert_question_bank, ),
    url(r'create_question_bank_addQuestion$', views.create_question_bank_addQuestion, ),
    url(r'show_sub_homework$', views.show_sub_homework, ),
    url(r'show_sub_homework_infor$', views.show_sub_homework_infor, ),
    url(r'correct_sub_homework$', views.correct_sub_homework, ),
    url(r'show_student_information$', views.show_student_information, ),
    url(r'delete_student$', views.delete_student, ),
    url(r'show_homework_history$', views.show_homework_history, ),
    url(r'show_homework_situation$', views.show_homework_situation, ),
]