from django.urls import path
from . import  views 
from django.contrib.auth.views import LogoutView
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('student/', views.student, name='student'),
    path('company/', views.company, name='company'),
    path('student/register', views.add_student, name='student_register'),
    path('company/register', views.add_company, name='company_register'),
    path('login', views.MyLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(next_page=settings.HOME), name='logout'),
    path('profile', views.profile, name='profile'),
    path('student/update', views.update_student, name='student_update'),
    path('success', views.success, name='success'),
    path('change_password', views.change_password, name='password_change'),
    path('company/register/job', views.reg_offer, name='register_job'),
    path('offer/view', views.view_jobs, name='view_jobs'),
    path('contact', views.contact_us, name='contact_us'),
    
]

app_name = 'users'