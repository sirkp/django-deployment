from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)#Hashimg the password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user #set up the one to one relationship

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']#profile_pic is defined in model

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html'
                            ,{'user_form':user_form,
                            'profile_form':profile_form,
                            'registered':registered}
                            )

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')# we used get('username') because of
        #<input type="text" name="username" placeholder="Enter Username"> in login.html
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)#It will authenticate automatically

        if user:
            if user.is_active:
                login(request,user)#It will login automatically
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print('Someone tried to login and failed!')
            print('Username: {} and Password {}'.format(username,password))
            return HttpResponse('invalid login details supplied')
    else:
        return render(request, 'basic_app/login.html')

@login_required
def user_logout(request):
    logout(request)#It will logout automatically
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):#some function which requires login
    return HttpResponse('You are logged in, Nice!')
