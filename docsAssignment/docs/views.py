from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm
from .models import Authorized, Documents
from django.views import defaults


# Create your views here.
def register_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'docs/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'docs/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    return render(request, 'docs/dashboard.html')


@login_required(login_url='login')
def room(request, room_name):
    doc_name = Documents.objects.filter(name=room_name)
    if doc_name:
        auth = Authorized.objects.filter(user=request.user,document=doc_name[0])
        if auth and auth[0].authorized:
            return render(request, 'docs/room.html', {
                'room_name': room_name,
                'user_name': request.user.username
            })
        else:
            return defaults.permission_denied(request, '',
                                              template_name='403.html')
    else:
        return defaults.page_not_found(request, '', template_name='404.html')
