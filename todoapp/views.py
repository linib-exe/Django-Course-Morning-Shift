from django.shortcuts import render,redirect
from .forms import TODOForm
from .models import TODO
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="login")
def create(request):
    form = TODOForm()
    if request.method =='POST':
        # print(request.POST)
        form = TODOForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            form.save()
            return redirect('/retreive')
    return render(request,'create.html',{'form':form})

def retreive(request):
    # todos = TODO.objects.all()
    try:
        todos = TODO.objects.filter(user=request.user)
    except:
        todos = []
    return render(request,'retreive.html',{'todos':todos})

def update(request,id):
    todo = TODO.objects.get(id=id)
    form = TODOForm(instance=todo)
    if request.method =='POST':
        # print(request.POST)
        form = TODOForm(request.POST,instance=todo)
        if form.is_valid():
            form.save()
            return redirect('/retreive')
    return render(request,'create.html',{'form':form})

def delete(request,id):
    todo = TODO.objects.get(id=id)
    todo.delete()
    return redirect('retreive')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        User.objects.create_user(username=username,
                                 password=password,
                                 email=email)
        return redirect('retreive')
    return render(request,'register.html')

def loginn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,
                            username=username,
                            password=password)
        if user is not None:
            login(request, user)
            return redirect('retreive')  # Assuming this is the correct URL for redirection upon successful login
    return render(request, 'login.html')

def logoutt(request):
    logout(request)
    return redirect('retreive')

