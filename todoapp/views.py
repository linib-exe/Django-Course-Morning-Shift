from django.shortcuts import render,redirect
from .forms import TODOForm
from .models import TODO
# Create your views here.
def create(request):
    form = TODOForm()
    if request.method =='POST':
        # print(request.POST)
        form = TODOForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/create')
    return render(request,'create.html',{'form':form})

def retreive(request):
    todos = TODO.objects.all()
    print(type(todos))
    return render(request,'retreive.html',{'todos':todos})