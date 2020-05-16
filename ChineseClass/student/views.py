from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
import xlrd
import time
import datetime
from django.contrib.auth.hashers import make_password, check_password
from . models import Student
from.models import Student_Class
from control.models import Class_permission
from teacher.models import Classes, Homework, Homework_score, Mistake, Question, Sub_answer, Teacher
# Create your views here.

#学生登录
@require_http_methods(["POST"])
def login(request):
    response = {}
    result = json.loads(request.body.decode())
    try:
        student = Student.objects.get(username = result.get('username'))
        if(check_password(result.get('password'),student.password)):
            response['msg'] = 'success'
        else:
            response['msg'] = 'passwordfailure'
    except  Exception as e:
        response['msg'] = 'usernamefailure'
    return JsonResponse(response)

#学生注册
@require_http_methods(["POST"])
def register(request):
    response = {}
    result = json.loads(request.body.decode())
    try:
        student = Student (
            username = result.get('username'),
            password = make_password(result.get('password')),
            realname = result.get('realname'),
            sex = result.get('sex'),
            age = result.get('age'),
            phone = result.get('phone'),
            grade = result.get('grade'),
            userIcon = result.get('userIcon')
        )
        student.save()
        response['msg'] = 'success'
    except  Exception as e:
        response['msg'] = 'failure'
    return JsonResponse(response)

#学生查看个人信息
@require_http_methods(["GET"])
def show_information(request):
    response = {}
    try:
        student = Student.objects.get(username = request.GET.get('username'))
    except Exception as e:
        response['msg'] = 'failure' #学生不存在
        return  JsonResponse(response)
    response['username'] = student.username
    response['realname'] = student.realname
    response['sex'] = student.sex
    response['age'] = student.age
    response['phone'] = student.phone
    response['grade'] = student.grade
    response['userIcon'] = student.userIcon
    return  JsonResponse(response)

#学生加入班级
@require_http_methods(["GET"])
def joinclass(request):
    response = {}
    try:
        permission = Class_permission.objects.get(name = request.GET.get('permission'))
    except  Exception as e:
        response['msg'] = 'permission_failure' #许可不存在
        return JsonResponse(response)
    
    try:
        classes = Classes.objects.get(permission = permission)
    except  Exception as e:
        response['msg'] = 'classes_failure' #班级未开班
        return JsonResponse(response)
    
    try:
        student = Student.objects.get(username = request.GET.get('username'))
    except  Exception as e:
        response['msg'] = 'student_failure'#学生不存在
        return JsonResponse(response)
    
    try:
        sc = Student_Class(
            student = student,
            classes = classes
        )
        sc.save()
        response['msg'] = 'success'
    except  Exception as e:
        response['msg'] = 'sc_failure'#进班失败
    return JsonResponse(response)

#学生查看自己加入的班级
@require_http_methods(["GET"])
def show_classes(request):
    response = {}
    try:
        student = Student.objects.get(username = request.GET.get('username'))
    except  Exception as e:
        response['msg'] = 'student_failure'#学生不存在
        return JsonResponse(response)
    scs = Student_Class.objects.filter(student = student)
    classes = []
    if scs.count() == 0:
        response['msg'] = 'noneclasses'#没加入班级
        return JsonResponse(response)
    for sc in scs:
        classes.append(sc.classes.name)
    response['list'] = classes
    return JsonResponse(response)

#学生点击某个班级查看详细信息(根据班级名字)
@require_http_methods(["GET"])
def show_class_infor(request):
    response = {}
    try:
        classes = Classes.objects.get(name = request.GET.get('name'))
    except Exception as e:
        response['msg'] = 'class_failure' #班级不存在
        return JsonResponse(response)
    response['description'] = classes.description
    teacher = Teacher.objects.get(username = classes.teacher.username)
    response['teacher'] = teacher.realname
    response['createdate'] = classes.create_date
    names = []
    homework = Homework.objects.filter(classes = classes)
    num = Homework.objects.filter(classes = classes).count()
    for i in range(0, num):
        names.append(homework[i].name)
    response['homework'] = names
    response['msg'] = 'success'
    return JsonResponse(response)


#学生查看当前作业
@require_http_methods(["GET"])
def show_homework(request):
    response = {}
    try:
        student = Student.objects.get(username = request.GET.get('username'))
    except  Exception as e:
        response['msg'] = 'student_failure'#学生不存在
        return JsonResponse(response)
    scs = Student_Class.objects.filter(student = student)
    classes = []
    names = []
    if scs.count() == 0:
        response['msg'] = 'noneclasses'#没加入班级
        return JsonResponse(response)
    for sc in scs:
        classes.append(sc.classes)
    for cl_ass in classes:
        homeworks = Homework.objects.filter(classes = cl_ass)
        for homework in homeworks:
            if (Homework_score.objects.filter(homework = homework,student = student).count() != 0):
                d = {"homework": homework.name, "create_time": homework.create_time.strftime("%Y-%m-%d %H:%M:%S"), 
                "close_time": homework.close_time.strftime("%Y-%m-%d %H:%M:%S"),"status":'已批改'}
            elif (Sub_answer.objects.filter(homework = homework,student = student).count()!=0):
                d = {"homework": homework.name, "create_time": homework.create_time.strftime("%Y-%m-%d %H:%M:%S"), 
                "close_time": homework.close_time.strftime("%Y-%m-%d %H:%M:%S"),"status":'已完成'}
            elif (homework.close_time.replace(tzinfo=None).__lt__(datetime.datetime.now())):
                d = {"homework": homework.name, "create_time": homework.create_time.strftime("%Y-%m-%d %H:%M:%S"), 
                "close_time": homework.close_time.strftime("%Y-%m-%d %H:%M:%S"),"status":'已过期'}
            else:
                d = {"homework": homework.name, "create_time": homework.create_time.strftime("%Y-%m-%d %H:%M:%S"), 
                "close_time": homework.close_time.strftime("%Y-%m-%d %H:%M:%S"),"status":'未完成'}
            names.append(d)
    response['names'] = names
    return JsonResponse(response)

#显示某个作业的内容
@require_http_methods(["GET"])
def show_homework_infor(request):
    response = {}
    try:
        homework = Homework.objects.get(name = request.GET.get('name'))
    except Exception as e:
        response['msg'] = 'homework_failure' #作业不存在
        return JsonResponse(response)
    try: #读取题库
        book = xlrd.open_workbook('C:\\excel\\question_bank.xlsx')
        sheet1 = book.sheets()[0]
        nrows = sheet1.nrows #题库表格总行数
    except Exception as e:
        response['msg'] = 'questionBank_failure' #读取题库遇到错误
        return JsonResponse(response)
    questions = homework.question.all() #此作业对应的那些题目/.all()很重要
    single = []
    mul = []
    completion = []
    judgement = []
    subjective = []
    num = questions.count()
    for i in range(0, num):
        if(questions[i].types == "单选"):
            c = questions[i].location - 1
            d = {"location": c+1, "question": sheet1.cell(c,1).value, "choice1": sheet1.cell(c,2).value, 
            "choice2": sheet1.cell(c,3).value, "choice3": sheet1.cell(c,4).value, "choice4": sheet1.cell(c,5).value
            ,"answer": sheet1.cell(c,6).value, "description": sheet1.cell(c,7).value}
            single.append(d)
        elif(questions[i].types == "多选"):
            c = questions[i].location - 1
            d = {"location": c+1, "question": sheet1.cell(c,1).value, "choice1": sheet1.cell(c,2).value, 
            "choice2": sheet1.cell(c,3).value, "choice3": sheet1.cell(c,4).value, "choice4": sheet1.cell(c,5).value,
            "choice5": sheet1.cell(c,6).value, "answer": sheet1.cell(c,7).value, "description": sheet1.cell(c,8).value}
            mul.append(d)
        elif(questions[i].types == "填空"):
            c = questions[i].location - 1
            d = {"location": c+1, "question": sheet1.cell(c,1).value, "answer": sheet1.cell(c,2).value, 
            "description": sheet1.cell(c,3).value}
            completion.append(d)
        elif(questions[i].types == "判断"):
            c = questions[i].location - 1
            d = {"location": c+1, "question": sheet1.cell(c,1).value, "answer": sheet1.cell(c,2).value, 
            "description": sheet1.cell(c,3).value}
            judgement.append(d)
        elif(questions[i].types == "主观"):
            c = questions[i].location - 1
            d = {"location": c+1, "question": sheet1.cell(c,1).value, "description": sheet1.cell(c,2).value}
            subjective.append(d)
    response['single'] = single
    response['mul'] = mul
    response['completion'] = completion
    response['judgement'] = judgement
    response['subjective'] = subjective
    response['msg'] = 'success'
    return JsonResponse(response)
    
#学生完成客观题并点击确认
@require_http_methods(["POST"])
def finish_objective_question(request):
    result = json.loads(request.body.decode())
    response = {}
    try:
        homework = Homework.objects.get(name = result.get('name'))
        student = Student.objects.get(username = result.get('username'))
        locations = result.get('location') #前端返回的错题位置列表
    except Exception as e:
        response['msg'] = 'getInformation_failure'
        return JsonResponse(response)
    for i in range(0, len(locations)):
        question = Question.objects.get(location = locations[i])
        mistake = Mistake(homework = homework, student = student, question = question)
        mistake.save()
    total = homework.question.count()
    score = round((total - len(locations))/total, 2)
    score = score * 100
    homework_score = Homework_score(homework = homework, student = student, score = score)
    homework_score.save() 
    response['msg'] = 'success'
    response['score'] = score   
    return JsonResponse(response) 

#学生完成主观题
@require_http_methods(["POST"])
def finish_subjective_question(request):
    response = {}
    result = json.loads(request.body.decode())
    try:
        homework = Homework.objects.get(name = result.get('name'))
    except Exception as e:
        response['msg'] = 'homework_failure'
        return JsonResponse(response)
    try:
        student = Student.objects.get(username = result.get('username'))
    except Exception as e:
        response['msg'] = 'student_failure'
        return JsonResponse(response)
    try:
        question = Question.objects.get(location = result.get('location'))
    except Exception as e:
        response['msg'] = 'question_failure'
        return JsonResponse(response)
    
    try:
        sub_answer = Sub_answer(
            homework = homework,
            student = student,
            question = question,
            answer = result.get('answer')
        )
        sub_answer.save()
    except Exception as e:
        response['msg'] = 'answer_faiure' #创建答案失败
    response['msg'] = 'success'
    return JsonResponse(response)

#学生查看错题(选择语文、数学、外语等)
@require_http_methods(["GET"])
def show_mistake(request):
    response = {}
    book = xlrd.open_workbook('C:\\excel\\question_bank.xlsx')
    sheet1 = book.sheets()[0]
    nrows = sheet1.nrows #题库表格总行数
    Chinese_name = {'Math': '数学', 'Chinese': '语文', 'English': '英语'}
    single = []
    mul = []
    completion = []
    judgement = []
    try:
        student = Student.objects.get(username = request.GET.get('username'))
        subject = request.GET.get('subject')
    except Exception as e:
        response['msg'] = 'student_failure' #没有该学生
        return JsonResponse(response)
    mistakes = Mistake.objects.filter(student = student)
    for i in range(0, mistakes.count()):
        question = mistakes[i].question
        if(question.subject == Chinese_name[subject]):
            if(question.types == "单选"):
                c = question.location - 1
                d = {"location": c+1, "question": sheet1.cell(c,1).value, "choice1": sheet1.cell(c,2).value, 
                "choice2": sheet1.cell(c,3).value, "choice3": sheet1.cell(c,4).value, "choice4": sheet1.cell(c,5).value
                ,"answer": sheet1.cell(c,6).value, "description": sheet1.cell(c,7).value}
                single.append(d)
            elif(question.types == "多选"):
                c = question.location - 1
                d = {"location": c+1, "question": sheet1.cell(c,1).value, "choice1": sheet1.cell(c,2).value, 
                "choice2": sheet1.cell(c,3).value, "choice3": sheet1.cell(c,4).value, "choice4": sheet1.cell(c,5).value,
                "choice5": sheet1.cell(c,6).value, "answer": sheet1.cell(c,7).value, "description": sheet1.cell(c,8).value}
                mul.append(d)
            elif(question.types == "填空"):
                c = question.location - 1
                d = {"location": c+1, "question": sheet1.cell(c,1).value, "answer": sheet1.cell(c,2).value, 
                "description": sheet1.cell(c,3).value}
                completion.append(d)
            elif(question.types == "判断"):
                c = question.location - 1
                d = {"location": c+1, "question": sheet1.cell(c,1).value, "answer": sheet1.cell(c,2).value, 
                "description": sheet1.cell(c,3).value}
                judgement.append(d)
    response['single'] = single
    response['mul'] = mul
    response['completion'] = completion
    response['judgement'] = judgement
    response['msg'] = 'success'
    return JsonResponse(response)

#学生查看作业得分情况
@require_http_methods(["GET"])
def show_homework_score(request):
    response={}
    book = xlrd.open_workbook('C:\\excel\\question_bank.xlsx')
    sheet1 = book.sheets()[0]
    try:
        student = Student.objects.get(username = request.GET.get('username'))
    except Exception as e:
        response['msg'] = 'student_failure' #没有该学生
        return JsonResponse(response)
    
    try:
        homework = Homework.objects.get(name = request.GET.get('homework_name'))
    except Exception as e:
        response['msg'] = 'homework_failure' #没有该作业
        return JsonResponse(response)
    
    try:
        homework_score = Homework_score.objects.get(homework = homework,student = student)
    except Exception as e:
        response['msg'] = 'homework_score_failure' #没有该作业的得分记录
        return JsonResponse(response)

    mistakes = Mistake.objects.filter(homework = homework,student = student)
    single = []
    mul = []
    completion = []
    judgement = []
    sub = []
    questions = homework.question.all()
    for question in questions:
        if(question.types == '主观'):
            c = questions[i].location - 1
            d = {"location": c+1, "question": sheet1.cell(c,1).value, "description": sheet1.cell(c,2).value}
            sub.append(d)
    for mistake in mistakes:
        question = mistake.question
        if(question.types == "单选"):
            c = question.location - 1
            d = {"location": c+1, "question": sheet1.cell(c,1).value, "choice1": sheet1.cell(c,2).value, 
            "choice2": sheet1.cell(c,3).value, "choice3": sheet1.cell(c,4).value, "choice4": sheet1.cell(c,5).value
            ,"answer": sheet1.cell(c,6).value, "description": sheet1.cell(c,7).value}
            single.append(d)
        elif(question.types == "多选"):
            c = question.location - 1
            d = {"location": c+1, "question": sheet1.cell(c,1).value, "choice1": sheet1.cell(c,2).value, 
            "choice2": sheet1.cell(c,3).value, "choice3": sheet1.cell(c,4).value, "choice4": sheet1.cell(c,5).value,
            "choice5": sheet1.cell(c,6).value, "answer": sheet1.cell(c,7).value, "description": sheet1.cell(c,8).value}
            mul.append(d)
        elif(question.types == "填空"):
            c = question.location - 1
            d = {"location": c+1, "question": sheet1.cell(c,1).value, "answer": sheet1.cell(c,2).value, 
            "description": sheet1.cell(c,3).value}
            completion.append(d)
        elif(question.types == "判断"):
            c = question.location - 1
            d = {"location": c+1, "question": sheet1.cell(c,1).value, "answer": sheet1.cell(c,2).value, 
            "description": sheet1.cell(c,3).value}
            judgement.append(d)
    response['score'] = homework_score.score
    response['create_time'] = homework_score.create_time
    response['comment'] = homework_score.comment
    response['single'] = single
    response['mul'] = mul
    response['completion'] = completion
    response['judgement'] = judgement
    response['subjective'] = sub
    response['msg'] = 'success'
    return JsonResponse(response)


