from django.db import models

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=20,verbose_name="名称")
    address = models.CharField(max_length=20,verbose_name = "地址")
    phone = models.CharField(max_length=11,verbose_name = "联系电话")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '学校'
        verbose_name_plural = '学校'
class Class_permission(models.Model):
    name = models.CharField(max_length=8,unique = True,verbose_name = "班级许可码")
    school = models.ForeignKey(School,on_delete=models.CASCADE,verbose_name = "所属学校")
    close_date = models.DateField(verbose_name = "截止日期")
    use = models.BooleanField(verbose_name = "是否使用")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '班级许可码'
        verbose_name_plural = '班级许可码'