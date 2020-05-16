from django.contrib import admin
from .models import School
from .models import Class_permission
# Register your models here.
admin.site.register(School)
admin.site.register(Class_permission)
admin.site.site_header = '中华小课堂后台管理'
admin.site.site_title = '中华小课堂后台管理'