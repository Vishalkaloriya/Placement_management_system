from django.http.response import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse

from Project.settings import EMAIL_HOST
from .forms import StudentForm, CompanyForm, StudentUpdateForm, OfferForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Student, Company, Offer
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from accounts.models import Account
from django.core.mail import send_mail


#################################### Success Page #####################################

def success(request):
    return render(request, 'success.html')

#################################### Login User #####################################

class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'web/student_login/index.html'
    
    def get_success_url(self):
        return reverse_lazy('users:profile') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))

################################# Logout User #######################################

class MyLogoutView(LogoutView):
    template_name = 'logout.html'
    def get_success_url(self):
        return reverse_lazy('users:index') 
    
############################## Utility Functions ##################################

def index(request):
    return render(request, 'web/Homepage/index.html')

###################################################################################

def student(request):
    return render(request, 'web/student_page/index.html')

###################################################################################

def company(request):
    return render(request, 'web/company_page/index.html')

###################################################################################
def add_student(request):
    if request.method != 'POST':
        form = StudentForm()
    else:
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            next = request.POST.get('next', request.GET.get('next', ''))
            if next:
                print(str(next))
                return HttpResponseRedirect(next)
            HttpResponseRedirect(reverse('users:success'))
    context = { 'form':form}
    return render(request, 'regstudent.html', context)

###################################################################################

def add_company(request):
    if request.method != 'POST':
        form = CompanyForm()
    else:
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            next = request.POST.get('next', request.GET.get('next', ''))
            if next:
                print(str(next))
                return HttpResponseRedirect(next)
            HttpResponseRedirect(reverse('users:index'))
    context = { 'form':form}
    return render(request, 'web/company_signup/index.html', context)

###################################################################################

@login_required
def profile(request):
    if request.user.student:
        model = request.user.student
        context = { 'model': model }
        return render(request, 'stuprofile.html', context)
    elif request.user.company:
        model = request.user.company
        context = { 'model': model }
        return render(request, 'comprofile.html', context)
    return render(request, 'index.html')

###################################################################################
    
@login_required
def update_student(request):
    student = Student.objects.get(Email=request.user.student.Email)
    if request.method != 'POST':
        form = StudentUpdateForm(instance=student)
    else:
        form = StudentUpdateForm(instance=student, data=request.POST)
        if form.is_valid():
            student = form.save()
            student.save()
            HttpResponseRedirect(reverse('users:profile'))
    context = {'form':form}
    return render(request, 'update_student.html', context)

###################################################################################

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            HttpResponseRedirect(reverse('users:profile'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password/password_change.html', {
        'form': form
    })

###################################################################################

def create_student_user():
    students = Student.objects.filter(Is_Created=False)
    email_from = EMAIL_HOST
    if students:
        subject = 'Placemnt Cell Account '
        body = 'UserName : %s\nPassword : %s'
        for student in students:
            email = student.Email
            password = email.spilt('@')[0]
            account = Account.objects.create_user(email, password)
            account.student = student
            account.save()
            student.Is_Created = True
            student.save()
            send_mail( subject, body %(email, password), email_from, [email,] )
            
###################################################################################

@login_required
def reg_offer(request):
    if not request.user.company:
        return HttpResponseBadRequest('You are not allowed to complete this application.')
    if request.method != 'POST':
        form = OfferForm()
    else:
        form = OfferForm(request.POST)
        if form.is_valid():
            job = form.save()
            job.company = request.user.company
            job.save()
            next = request.POST.get('next', request.GET.get('next', ''))
            if next:
                return HttpResponseRedirect(next)
            HttpResponseRedirect(reverse('users:index'))
    context = { 'form':form}
    return render(request, 'web/offer_page/index.html', context)

###################################################################################

def create_company_user():
    email_from = EMAIL_HOST
    companys = Company.objects.filter(Is_Created=False)
    if companys:
        subject = 'Placemnt Cell Account '
        body = 'UserName : %s\nPassword : %s'
        for com in companys:
            email = com.Email
            password = email.split('@')[0]
            account = Account.objects.create_user(email, password)
            account.company = com
            account.save()
            com.Is_Created = True
            com.save()
            send_mail( subject, body %(email, password), email_from, [email,] )

###################################################################################

def view_students(request):
    students = Student.objects.all()
    context = {'students':students}
    return render(request, 'students.html', context)

###################################################################################

@login_required
def view_jobs(request):
    if request.method != 'POST':
        offers = Offer.objects.all()
    else:
        offers = Offer.objects.all()
        if 'title' in request.POST:
            offers = offers.filter(Title__contains=request.POST['title'])
        if 'branch' in request.POST:
            offers = offers.filter(Branch=request.POST['branch'])
    context = {'offers':offers}
    return render(request, 'offers.html', context)
        
###################################################################################

def contact_us(request):
    return render(request, 'web/Contact_Us/index.html')

###################################################################################