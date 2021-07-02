"""quiz_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from quiz import views
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url
from django.conf.urls.static import static

urlpatterns = [
    path(r'', views.home,name='home'),
    path(r'admin/',views.admin,name='admin'),
    path(r'admin_register/',views.signup),
    path(r'login/',views.login),
    path(r'dashboard/',views.dashboard),
    path(r'add_quiz/',views.add_quiz),
    path(r'after_add_quiz/dashboard/',views.add_quiz_db),
    path(r'view_quiz/',views.view_quiz),
    path(r'after_delete_quiz/dashboard/',views.delete_quiz),
    path(r'view_question/',views.view_questions),
    path(r'add_student/',views.add_student),
    path(r'after_add_student/dashboard/',views.add_student_db),
    path(r'student_signup/',views.student_signup),
    path(r'student_register/',views.student_register),
    path(r'student_login/',views.student_login),
    path(r'student_dashboard/',views.student_dashboard),
    path(r'show_question_for_quiz/',views.show_question_for_quiz),
    path(r'submit_quiz/<quiz_id>/<student_quiz_id>/<int:question_id>',views.submit_quiz),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':       settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
urlpatterns = urlpatterns+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)