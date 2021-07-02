import re
from bson.objectid import ObjectId
from django.http import response
from django.shortcuts import redirect, render
import pymongo
from django.contrib import messages
from bson import Binary, Code
from bson.json_util import dumps# Create your views here.
import time


myclient = pymongo.MongoClient("mongodb+srv://project1:project1@cluster0.ahn2s.mongodb.net/Quiz?retryWrites=true&w=majority")
mydb = myclient['Quiz']
admin_details = mydb["Admin_det"]
questions = mydb["questions"]
student_list_for_quiz = mydb['student_list_for_quiz']
student_details = mydb['student_details']
student_mark = mydb['student_mark']




def home(request):
     return render(request,'Home.html')
def admin(request):
    return render(request,'admin.html')
def signup(request):
     fname = request.POST.get('fname')
     lname = request.POST.get('lname')
     email = request.POST.get('email')
     password = request.POST.get('password')
     mydict = { "fname": fname, "lname": lname,"email":email,"password":password,}
     admin_details.insert_one(mydict)
     return render(request,'admin.html')
def login(request):
     if request.method == 'GET':
          return render(request,'login.html')
     elif request.method == 'POST':
          email = request.POST.get("email")
          password = request.POST.get("password")
          dbRecord = admin_details.find_one({ "email" : email})

          if(dbRecord and (password==dbRecord['password'])):
               return redirect('/dashboard/')
          else:
               context={
                    "error":"Invalid Login"
               }
               return render(request,'login.html',context)

def dashboard(request):
     if request.method == 'GET':
          quizList = questions.find({})
          finalQuizList = []
          for quiz in quizList:
              quiz['id'] = str(quiz.get('_id'))
              finalQuizList.append(quiz)
          return render(request,'admin_dashboard.html',{"val":finalQuizList})
def add_quiz(request):
     return render(request,'add_quiz.html')
def add_quiz_db(request):
    if request.method == 'POST':
         quiz_name = request.POST.get('quiz_name')
         subject = request.POST.get('subject')
         total_question = request.POST.get('tot_question')
         questions_list = []
         for i in range(0,int(total_question)):
               j=str(i)
               question = request.POST.get('question'+j)
               option1 = request.POST.get('option'+j)
               option2 = request.POST.get('optio'+j)
               option3 = request.POST.get('opti'+j)
               option4 = request.POST.get('opt'+j)
               answer = request.POST.get('answer'+j)
               mydict = {  "question": question,"option1":option1,"option2":option2,"option3":option3,"option4":option4,"answer":answer,}
               questions_list.append(mydict)
         questions_dict = {"quiz_name":quiz_name,"subject": subject,"questions":questions_list} 
         x = questions.insert_one(questions_dict)      
         return render(request,'admin_dashboard.html')
def view_quiz(request):
     quizList = questions.find({})
     finalQuizList = []
     for quiz in quizList:
          quiz['id'] = str(quiz.get('_id'))
          finalQuizList.append(quiz)
     return render(request,'view_quiz.html',{"val":finalQuizList})
def delete_quiz(request):
     if request.method == 'GET':
          id = request.GET.get("id")
          quiz_detail_from_db = questions.delete_one({"_id":ObjectId(id)})
     return render(request,'admin_dashboard.html')
def view_questions(request):
     if request.method == 'GET':
          id = request.GET.get("id")
          quiz_detail_from_db = questions.find_one({"_id":ObjectId(id)})
          question_list = quiz_detail_from_db['questions']
     return render(request,'view_question.html',{"quiz_detail_from_db":question_list })
def add_student(request):
     quizList = questions.find({})
     finalQuizList = []
     for quiz in quizList:
          quiz['id'] = str(quiz.get('_id'))
          finalQuizList.append(quiz)
     return render(request,'add_student.html',{"val":finalQuizList})
def add_student_db(request):
     tot_student = request.POST.get('tot_student')
     tot_student = int(tot_student)
     selectedQuiz = request.POST.get('selectedQuiz')
     for i in range(0,tot_student):
         j=str(i)
         email = request.POST.get('field_name'+j)
         student_list_for_quiz.insert_one({"stu_email":email,"quiz_id":selectedQuiz})
     return render(request,'admin_dashboard.html')
def student_signup(request):
    return render(request,'student_signup.html')
def student_register(request):
     fname = request.POST.get('fname')
     lname = request.POST.get('lname')
     email = request.POST.get('email')
     password = request.POST.get('password')
     mydict = { "fname": fname, "lname": lname,"email":email,"password":password,}
     student_details.insert_one(mydict)
     return render(request,'student_signup.html')
def student_login(request):
     if request.method == 'GET':
          return render(request,'student_login.html')
     elif request.method == 'POST':
          email = request.POST.get("email")
          password = request.POST.get("password")
          dbRecord = student_details.find_one( { "email" : email} )
          if(dbRecord and (password==dbRecord['password'])):
               return redirect('/student_dashboard/?email='+email)
          else:
               context={
                    "error":"Invalid Login"
               }
               return render(request,'student_login.html',context)
def student_dashboard(request):
     if request.method == 'GET':
          email = request.GET.get("email")
          quizList = student_list_for_quiz.find({"stu_email":email})
          student_quiz_details = []
          for quiz in quizList:
               quiz_detail_from_db = questions.find_one({"_id":ObjectId(quiz['quiz_id'])})
               quiz_detail_from_db['id'] = str(quiz_detail_from_db.get('_id'))
               quiz_detail_from_db['student_quiz_id'] = str(quiz.get('_id'))
               student_quiz_details.append(quiz_detail_from_db)
          return render(request,'student_dashboard.html',{"quiz_list":student_quiz_details})
def show_question_for_quiz(request):
     quiz_id = request.GET.get("id")
     question_id = request.GET.get("question_id")
     student_quiz_id=request.GET.get("student_quiz_id")
     quiz_detail_from_db = questions.find_one({"_id":ObjectId(quiz_id)})
     if(question_id):
          question_number = question_id
     else :
          question_number = 0
     
     questions_list = quiz_detail_from_db['questions']
     student_quiz_details = student_list_for_quiz.find_one({"_id": ObjectId(student_quiz_id)})

     if(int(question_number) < len(questions_list)):
          question = quiz_detail_from_db['questions'][int(question_number)]
          if(not (student_quiz_details.get('start_time'))):
               milliseconds = int(round(time.time() * 1000))
               student_list_for_quiz.update({"_id": ObjectId(student_quiz_id)} , {"$set" : {"start_time":milliseconds}})
          answer = question['answer']
          isCorrect = False
          submitted_answer = ""
          student_submitted_answer = student_quiz_details.get('answers')

          if(student_submitted_answer):
               if(str(int(question_number) + 1) in student_submitted_answer):
                    answer_details = student_submitted_answer[str(int(question_number) + 1)]
                    isCorrect=answer_details['isCorrect']
                    submitted_answer=answer_details['submitted_answer']
          context = {
               "quiz_id":quiz_id,
               "question_obj":question,
               "quiz_name":quiz_detail_from_db['quiz_name'],
               "question_number":int(question_number),
               "student_quiz_id":student_quiz_id,
               "isCorrect":isCorrect,
               "answer":answer,
               "submitted_answer" : submitted_answer
          }
          return render(request,'take_quiz_question.html',context)
     else :
          if(not (student_quiz_details.get('end_time'))):
               milliseconds = int(round(time.time() * 1000))
               student_list_for_quiz.update({"_id": ObjectId(student_quiz_id)} , {"$set" : {"end_time":milliseconds}})
          student_quiz_details = student_list_for_quiz.find_one({"_id": ObjectId(student_quiz_id)})
          correct_answer = 0
          submitted_answers = student_quiz_details['answers']
          for answer in submitted_answers:
               if(submitted_answers[answer]['isCorrect']):
                    correct_answer += 1
          context = {
               "correct_answer_count":correct_answer,
               "end_time":student_quiz_details['end_time'],
               "start_time":student_quiz_details['start_time'],
               "total_questions":len(questions_list)
          }
          student_mark_view = {
               "correct_answer_count":correct_answer,
               "total_questions":len(questions_list),
               "student_quiz_id":student_quiz_id,
               "quiz_id":quiz_id,
          }
          student_mark.insert_one(student_mark_view)
          return render(request,'show_result.html',context)


     
def submit_quiz(request,quiz_id,student_quiz_id,question_id):
     quiz_detail_from_db = questions.find_one({"_id":ObjectId(quiz_id)})
     answer = quiz_detail_from_db['questions'][question_id]['answer']
     submitted_answer = request.POST.get("option")
     if( answer == submitted_answer):
          isCorrect=True
     else :
          isCorrect=False
     answered_question = {
          "answers."+str(question_id + 1): {
               "isCorrect":isCorrect,
               "submitted_answer":submitted_answer
          }
     }
     student_list_for_quiz.update({"_id": ObjectId(student_quiz_id)}, {"$set": answered_question}, upsert = True)
     question = quiz_detail_from_db['questions'][question_id]
     context = {
          "quiz_id":quiz_id,
          "question_obj":question,
          "quiz_name":quiz_detail_from_db['quiz_name'],
          "question_number":int(question_id),
          "student_quiz_id":student_quiz_id,
          "isCorrect":isCorrect,
          "answer":answer,
          "submitted_answer":submitted_answer
     }
     return render(request,'take_quiz_question.html',context)
