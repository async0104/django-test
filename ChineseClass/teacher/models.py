from django.db import models

# Create your models here.
class Teacher(models.Model):
    username = models.CharField(max_length=10,unique = True,verbose_name = "用户名")
    realname = models.CharField(max_length=10,verbose_name = "真实姓名")
    sex = models.CharField(max_length=10,verbose_name = "性别")
    age = models.IntegerField(verbose_name = "年龄")
    phone = models.CharField(max_length=11,verbose_name = "电话号码")
    password = models.CharField(max_length=80,verbose_name = "密码")
    subject = models.CharField(max_length=10,verbose_name = "学科")
    school = models.ForeignKey('control.School', on_delete=models.CASCADE,verbose_name = "所属学校")
    userIcon = models.CharField(max_length=30,verbose_name = "头像")
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = '教师'
class Classes(models.Model):
    name = models.CharField(max_length=20,unique = True,verbose_name = "名称")
    description = models.CharField(max_length=50,verbose_name = "简介")
    permission = models.ForeignKey('control.Class_permission',on_delete=models.CASCADE,verbose_name = "许可码")
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name = "所属教师")
    create_date = models.DateField(auto_now_add = True,verbose_name = "开班日期")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '班级'
        verbose_name_plural = '班级'

class Question(models.Model):
    types = models.CharField(max_length=10,verbose_name = "类型")
    subject = models.CharField(max_length=10,verbose_name = "学科")
    difficulty = models.IntegerField(verbose_name = "难度")
    location = models.IntegerField(verbose_name = "题号")

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = '题目'
class Question_bank(models.Model):
    name = models.CharField(max_length=20,verbose_name = "名称")
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,verbose_name = "所属教师")
    question = models.ManyToManyField(Question,verbose_name = "题目")

    class Meta:
        verbose_name = '题库'
        verbose_name_plural = '题库'

class Homework(models.Model):
    name = models.CharField(max_length=20,unique = True,verbose_name = "名称")
    classes = models.ForeignKey(Classes,on_delete=models.CASCADE,verbose_name = "所属班级")
    question = models.ManyToManyField(Question,verbose_name = "题目")
    create_time = models.DateTimeField(auto_now_add = True,verbose_name = "创建时间")
    close_time = models.DateTimeField(verbose_name = "截止时间")
    student = models.ManyToManyField('student.Student', through='Homework_score',verbose_name = "学生")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '作业'
        verbose_name_plural = '作业'
class Homework_score(models.Model):
    homework  = models.ForeignKey(Homework,on_delete=models.CASCADE,verbose_name = "作业")
    student = models.ForeignKey('student.Student',on_delete=models.CASCADE,verbose_name = "学生")
    score = models.IntegerField(verbose_name = "得分")
    create_time = models.DateTimeField(auto_now_add = True,verbose_name = "创建时间")
    comment = models.TextField(null = True,verbose_name = "教师评论")

    class Meta:
        verbose_name = '作业得分'
        verbose_name_plural = '作业得分'
class Sub_answer(models.Model):
    homework = models.ForeignKey(Homework,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    student = models.ForeignKey('student.Student',on_delete=models.CASCADE)
    answer = models.TextField(null = True)

class Mistake(models.Model):
    homework  = models.ForeignKey(Homework,on_delete=models.CASCADE)
    student = models.ForeignKey('student.Student',on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)