from django.shortcuts import render
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
import xlrd
from . models import School
from teacher.models import Teacher,Question
from student.models import Student
# Create your views here.

#获取学校列表
@require_http_methods(["GET"])
def show_schools(request):
    response = {}
    try:
        schools = School.objects.filter()   #没有设置过滤，即查询所有结果
        response['list'] = json.loads(serializers.serialize("json", schools))
        response['msg'] = 'success'
    except  Exception as e:
        response['msg'] = str(e)
    return JsonResponse(response)

#获取教师密码
@require_http_methods(["GET"])
def get_teacherpw(request):
    response = {}
    try:
        teacher = Teacher.objects.get(username = request.GET.get('acount'))
        response['password'] = json.loads(teacher.passwd)   #get类型直接loads
        response['msg'] = 'success'
    except  Exception as e:
        response['msg'] = str(e)
    return JsonResponse(response)

#删除教师
@require_http_methods(["GET"])  
def del_teacher(request):
    response = {}
    try:
        teacher = Teacher.objects.get(username = request.GET.get('username'))
        teacher.delete()   #或:Book.objects.filter(book_name=request.GET.get('book_name')).delete()
        response['msg'] = 'success'
    except Exception as e:
        response['msg'] = str(e)
    return JsonResponse(response)


#获取教师列表
@require_http_methods(["GET"])
def show_teachers(request):
    response = {}
    try:
        teachers = Teacher.objects.filter()   #没有设置过滤，即查询所有结果
        response['list'] = json.loads(serializers.serialize("json", teachers))
        response['msg'] = 'success'
    except  Exception as e:
        response['msg'] = str(e)
    return JsonResponse(response)

#获取教师个人信息
@require_http_methods(["GET"])
def show_teacher(request):
    response = {}
    try:
        teacher = Teacher.objects.filter(username = request.GET.get('username'))   
        response['list'] = json.loads(serializers.serialize("json", teacher))
        response['msg'] = 'success'
    except  Exception as e:
        response['msg'] = str(e)
    return JsonResponse(response)

#教师选题
@require_http_methods(["GET"])
def show_questions(request):
    response = {}
    book = xlrd.open_workbook('C:\\excel\\question_bank.xlsx')
    sheet1 = book.sheets()[0]
    nrows = sheet1.nrows #题库表格总行数
    try:
        types = request.GET.get('type')
        subject = request.GET.get('subject')
        homework = []
        if(types == "single"): #单选
            if(subject == "Math"): #数学
                questions = Question.objects.filter(types = "单选", subject = "数学")
                num = Question.objects.filter(types = "单选", subject = "数学").count()
                for i in range(0, num):
                    for j in range(0, nrows): #遍历整个excel表
                        if(questions[i].location == j+1): #找到了对应的题目
                            d = {"order": j+1, "question": sheet1.cell(j,1).value, "choice1": sheet1.cell(j,2).value, 
                            "choice2": sheet1.cell(j,3).value, "choice3": sheet1.cell(j,4).value, "choice4": sheet1.cell(j,5).value
                            ,"answer": sheet1.cell(j,6).value, "description": sheet1.cell(j,7).value}    
                            homework.append(d)
            elif(subject == "Chinese"): #语文
                questions = Question.objects.filter(types = "单选", subject = "语文")
                num = Question.objects.filter(types = "单选", subject = "语文").count()
                for i in range(0, num):
                    for j in range(0, nrows): 
                        if(questions[i].location == j+1): 
                            d = {"order": j+1, "question": sheet1.cell(j,1).value, "choice1": sheet1.cell(j,2).value, 
                            "choice2": sheet1.cell(j,3).value, "choice3": sheet1.cell(j,4).value, "choice4": sheet1.cell(j,5).value
                            ,"answer": sheet1.cell(j,6).value, "description": sheet1.cell(j,7).value}    
                            homework.append(d)
            elif(subject == "English"): #英语
                questions = Question.objects.filter(types = "单选", subject = "英语")
                num = Question.objects.filter(types = "单选", subject = "英语").count()
                for i in range(0, num):
                    for j in range(0, nrows): 
                        if(questions[i].location == j+1): 
                            d = {"order": j+1, "question": sheet1.cell(j,1).value, "choice1": sheet1.cell(j,2).value, 
                            "choice2": sheet1.cell(j,3).value, "choice3": sheet1.cell(j,4).value, "choice4": sheet1.cell(j,5).value
                            ,"answer": sheet1.cell(j,6).value, "description": sheet1.cell(j,7).value}    
                            homework.append(d)
        elif(types == "mul"): #多选
            if(subject == "Math"): #数学
                questions = Question.objects.filter(types = "多选", subject = "数学")
                num = Question.objects.filter(types = "多选", subject = "数学").count()
                for i in range(0, num):
                    for j in range(0, nrows): #遍历整个excel表
                        if(questions[i].location == j+1): #找到了对应的题目
                            d = {"order": j+1, "question": sheet1.cell(j,1).value, "choice1": sheet1.cell(j,2).value, 
                            "choice2": sheet1.cell(j,3).value, "choice3": sheet1.cell(j,4).value, "choice4": sheet1.cell(j,5).value,
                            "choice5": sheet1.cell(j,6).value, "answer": sheet1.cell(j,7).value, "description": sheet1.cell(j,8).value}    
                            homework.append(d)
            elif(subject == "Chinese"): #语文
                questions = Question.objects.filter(types = "多选", subject = "语文")
                num = Question.objects.filter(types = "多选", subject = "语文").count()
                for i in range(0, num):
                    for j in range(0, nrows): 
                        if(questions[i].location == j+1): 
                            d = {"order": j+1, "question": sheet1.cell(j,1).value, "choice1": sheet1.cell(j,2).value, 
                            "choice2": sheet1.cell(j,3).value, "choice3": sheet1.cell(j,4).value, "choice4": sheet1.cell(j,5).value,
                            "choice5": sheet1.cell(j,6).value, "answer": sheet1.cell(j,7).value, "description": sheet1.cell(j,8).value}    
                            homework.append(d)
            elif(subject == "English"): #英语
                questions = Question.objects.filter(types = "多选", subject = "英语")
                num = Question.objects.filter(types = "多选", subject = "英语").count()
                for i in range(0, num):
                    for j in range(0, nrows): 
                        if(questions[i].location == j+1): 
                            d = {"order": j+1, "question": sheet1.cell(j,1).value, "choice1": sheet1.cell(j,2).value, 
                            "choice2": sheet1.cell(j,3).value, "choice3": sheet1.cell(j,4).value, "choice4": sheet1.cell(j,5).value,
                            "choice5": sheet1.cell(j,6).value, "answer": sheet1.cell(j,7).value, "description": sheet1.cell(j,8).value}    
                            homework.append(d)
        elif(types == "completion"): #填空
            if(subject == "Math"): #数学
                questions = Question.objects.filter(types = "填空", subject = "数学")
                num = Question.objects.filter(types = "填空", subject = "数学").count()
                for i in range(0, num):
                    for j in range(0, nrows): #遍历整个excel表
                        if(questions[i].location == j+1): #找到了对应的题目
                            d = {"order": j+1, "question": sheet1.cell(j,1).value, "answer": sheet1.cell(j,2).value, 
                            "description": sheet1.cell(j,3).value}    
                            homework.append(d)
            elif(subject == "Chinese"): #语文
                questions = Question.objects.filter(types = "填空", subject = "语文")
                num = Question.objects.filter(types = "填空", subject = "语文").count()
                for i in range(0, num):
                    for j in range(0, nrows): #遍历整个excel表
                        if(questions[i].location == j+1): #找到了对应的题目
                            d = {"order": j+1, "question": sheet1.cell(j,1).value, "answer": sheet1.cell(j,2).value, 
                            "description": sheet1.cell(j,3).value}    
                            homework.append(d)
            elif(subject == "English"): #英语
                questions = Question.objects.filter(types = "填空", subject = "英语")
                num = Question.objects.filter(types = "填空", subject = "英语").count()
                for i in range(0, num):
                    for j in range(0, nrows): #遍历整个excel表
                        if(questions[i].location == j+1): #找到了对应的题目
                            d = {"order": j+1, "question": sheet1.cell(j,1).value, "answer": sheet1.cell(j,2).value, 
                            "description": sheet1.cell(j,3).value}    
                            homework.append(d)
        elif(types == "judgement"): #判断
            if(subject == "Math"): #数学
                questions = Question.objects.filter(types = "判断", subject = "数学")
                num = Question.objects.filter(types = "判断", subject = "数学").count()
                for i in range(0, num):
                    for j in range(0, nrows): #遍历整个excel表
                        if(questions[i].location == j+1): #找到了对应的题目
                            d = {"order": j+1, "question": sheet1.cell(j,1).value, "answer": sheet1.cell(j,2).value, 
                            "description": sheet1.cell(j,3).value}   
                            homework.append(d)
            elif(subject == "Chinese"): #语文
                questions = Question.objects.filter(types = "判断", subject = "语文")
                num = Question.objects.filter(types = "判断", subject = "语文").count()
                for i in range(0, num):
                    for j in range(0, nrows): #遍历整个excel表
                        if(questions[i].location == j+1): #找到了对应的题目
                            d = {"order": j+1, "question": sheet1.cell(j,1).value, "answer": sheet1.cell(j,2).value, 
                            "description": sheet1.cell(j,3).value}   
                            homework.append(d)
            elif(subject == "English"): #英语
                questions = Question.objects.filter(types = "判断", subject = "英语")
                num = Question.objects.filter(types = "判断", subject = "英语").count()
                for i in range(0, num):
                    for j in range(0, nrows): #遍历整个excel表
                        if(questions[i].location == j+1): #找到了对应的题目
                            d = {"order": j+1, "question": sheet1.cell(j,1).value, "answer": sheet1.cell(j,2).value, 
                            "description": sheet1.cell(j,3).value}   
                            homework.append(d)
        elif(types == "subjective"): #主观
            if(subject == "Math"): #数学
                questions = Question.objects.filter(types = "主观", subject = "数学")
                num = Question.objects.filter(types = "主观", subject = "数学").count()
                for i in range(0, num):
                    for j in range(0, nrows): #遍历整个excel表
                        if(questions[i].location == j+1): #找到了对应的题目
                            d = {"order": j+1, "question": sheet1.cell(j,1).value, "description": sheet1.cell(j,2).value}   
                            homework.append(d)
            elif(subject == "Chinese"): #语文
                questions = Question.objects.filter(types = "主观", subject = "语文")
                num = Question.objects.filter(types = "主观", subject = "语文").count()
                for i in range(0, num):
                    for j in range(0, nrows): #遍历整个excel表
                        if(questions[i].location == j+1): #找到了对应的题目
                            d = {"order": j+1, "question": sheet1.cell(j,1).value, "description": sheet1.cell(j,2).value}   
                            homework.append(d)
            elif(subject == "English"): #英语
                questions = Question.objects.filter(types = "主观", subject = "英语")
                num = Question.objects.filter(types = "主观", subject = "英语").count()
                for i in range(0, num):
                    for j in range(0, nrows): #遍历整个excel表
                        if(questions[i].location == j+1): #找到了对应的题目
                            d = {"order": j+1, "question": sheet1.cell(j,1).value, "description": sheet1.cell(j,2).value}
                            homework.append(d)
        response['list'] = homework
        response['msg'] = 'success'
    except  Exception as e:
        response['msg'] = 'failure'
    return JsonResponse(response)

#获取学生列表
@require_http_methods(["GET"])
def show_students(request):
    response = {}
    try:
        students = Student.objects.filter()   #没有设置过滤，即查询所有结果
        response['list'] = json.loads(serializers.serialize("json", students))
        response['msg'] = 'success'
    except  Exception as e:
        response['msg'] = 'fail'
    return JsonResponse(response)