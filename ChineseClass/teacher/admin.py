from django.contrib import admin
from .models import Teacher
from .models import Classes
from .models import Question,Question_bank,Homework,Homework_score
# Register your models here.
admin.site.register(Teacher)
admin.site.register(Classes)
admin.site.register(Question)
admin.site.register(Homework_score)
admin.site.register(Homework)
admin.site.register(Question_bank)