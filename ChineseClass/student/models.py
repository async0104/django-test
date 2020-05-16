from django.db import models

# Create your models here.
class Student(models.Model):
    username = models.CharField(max_length=10,unique = True,verbose_name="用户名")
    realname = models.CharField(max_length=10,verbose_name="真实姓名")
    sex = models.CharField(max_length=10,verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄")
    phone = models.CharField(max_length=11,verbose_name="电话号码")
    password = models.CharField(max_length=80,verbose_name="密码")
    grade = models.IntegerField(verbose_name="年级")
    userIcon = models.CharField(max_length=30,verbose_name="头像")
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = '学生'
        verbose_name_plural = '学生'
class Student_Class(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    classes = models.ForeignKey('teacher.classes',on_delete=models.CASCADE)
