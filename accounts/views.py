from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate,login,logout
from .forms import Registerform
from .forms import ProfilePicForm
from home.models import User
# Create your views here.



def RegisterView(request):
    form = Registerform(request.POST)

    context = {
        'form':form
        }
    
    if form.is_valid():
        user1 = form.save(commit=False)
        user1.user = request.user
        user1.save()
        return redirect('login')
    
    
    return render(request, 'registration/register.html', context)



def LogouView(request):
    logout(request)
    return redirect('/accounts/login')


def update_user(request):
    if request.user.is_authenticated:
        current_user =  User.objects.get(id=request.user)
        profile_form = ProfilePicForm(request.POST or None, instance=current_user)
        if profile_form.is_valid():
            profile_form.save()
        return  render(request, 'home/pages/update_user.html')