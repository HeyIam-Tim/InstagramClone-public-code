from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import CreateUserForm
from .decorators import unauthenticated_user


@unauthenticated_user
def registerPage(request):
  form = CreateUserForm()
  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      form.save()
      print('USER_CREATED: ', form.cleaned_data.get('username'))

      username = form.cleaned_data.get('username')
      messages.success(request, 'Account was created for ' + username)
      return redirect('login_register:login')

  context = {'form':form}
  return render(request, 'login_register/register.html', context)


@unauthenticated_user
def loginPage(request):
  
  if request.method == 'POST':
    print('LOGIN: ',request.POST)
    username = request.POST.get('username').lower()
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)
    
    if user is not None:
      login(request, user)
      print('LOGGEDIN: ', user)
      return redirect("user_page", user.id)
    else:
      messages.info(request, 'Username OR Password is incorrect')

  return render(request, 'login_register/login.html')


def logoutUser(request):
  logout(request)
  return redirect('login_register:login')
