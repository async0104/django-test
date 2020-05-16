from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'login$', views.login, ),
    url(r'register$', views.register, ),
    url(r'joinclass$', views.joinclass, ),
    url(r'show_information$', views.show_information, ),
    url(r'show_classes$', views.show_classes, ),
    url(r'show_homework$', views.show_homework, ),
    url(r'show_homework_infor$', views.show_homework_infor, ),
    url(r'show_class_infor$', views.show_class_infor, ),
    url(r'finish_objective_question$', views.finish_objective_question, ),
    url(r'finish_subjective_question$', views.finish_subjective_question, ),
    url(r'show_mistake$', views.show_mistake, ),
    url(r'show_homework_score$', views.show_homework_score, ),
]