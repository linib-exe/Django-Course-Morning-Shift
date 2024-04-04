from django.shortcuts import render,redirect
from .forms import TODOForm
from .models import TODO
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .serializers import TODOSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import ValidationError
from .serializers import UserLoginSerializer
from django.db.models import Q


# --------- REST Framework --------------------
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
# --------- REST Framework --------------------

# Create your views here.
@login_required(login_url="login")
def create(request):
    form = TODOForm()
    if request.method =='POST':
        # print(request.POST)
        form = TODOForm(request.POST,request.FILES)
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
    print(request.user == todo.user)
    if (todo.user == request.user):
        if request.method =='POST':
            # print(request.POST)
            form = TODOForm(request.POST,instance=todo)
            if form.is_valid():
                form.save()
                return redirect('retreive')
        return render(request,'create.html',{'form':form})
    else:
        return HttpResponse("Arkako update garchhas lathuwa")

def delete(request,id):
    todo = TODO.objects.get(id=id)
    if (todo.user == request.user):
        todo.delete()
        return redirect('retreive')
    else:
        return HttpResponse("Arkako delete garchhas lathuwa")

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
    if request.user.is_authenticated:
        return redirect('retreive')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,
                                username=username,
                                password=password)
            if user is not None:
                login(request, user)
                return redirect('retreive')  
        return render(request, 'login.html')

def logoutt(request):
    logout(request)
    return redirect('retreive')

def search(request):
    query = request.GET.get('query')
    if query:
        # results = TODO.objects.filter(title__icontains=query, user=resquest.user)
        try:
            results = TODO.objects.filter(Q(title__icontains=query) & Q(user=request.user))
            if results.exists() == False:
                return HttpResponse("No items found")
        except:
            return redirect('login')
    else:
        results = None
    return render(request, 'search_results.html', {'results': results})


# --------- REST Framework --------------------

# @api_view(['GET'])
# def get_TODO(request):
#     todo = {'title':'api test','description':'This is used to test the api'}
#     return Response(todo)

@api_view(['GET'])
def get_TODO(request):
    todo = TODO.objects.all()
    serializer = TODOSerializer(todo,many=True)
    context = {
        'status':200,
        'data':serializer.data
    }
    return Response(context)

@api_view(['POST'])
def save_TODO(request):
    data = request.data
    serializer = TODOSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                'status':200,
                'data':serializer.data,
                'message':'data saved successfully'
            }
        )
    
    return Response(
        {
            'status':400,
            'message':'Someting went wrong',
            'data':serializer.data
        }
    )

@api_view(['PUT'])

def update_TODO(request,id):
    try:
        todo = TODO.objects.get(id=id)
        
    except:
        return Response({'message':"Couldn't find the todo"})
    print(todo.user,request.user)
    if todo.user == request.user :
        serializer = TODOSerializer(todo,data = request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status':200,
                    'message':"Data updated Successfully",
                    'data':serializer.data
                }
            )
        else:
            return Response({'message':"Data is invalid"})
    else:
        return Response({'message':'User is not valid'})
    
    

@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        # Create an instance of UserLoginSerializer with request data
        serializer = UserLoginSerializer(data=request.data)

        # Validate the serializer data
        if serializer.is_valid():
            try:
                # Retrieve user by username from serializer data
                username = serializer.validated_data.get('username')
                user = User.objects.get(username=username)
                
                # Check if password is correct from serializer data
                password = serializer.validated_data.get('password')
                if check_password(password, user.password):
                    # Generate or retrieve authentication token
                    token, created = Token.objects.get_or_create(user=user)
                    
                    # Return success response with token and admin status
                    return Response({
                        "success": True,
                        "token": token.key,
                        
                    })
                else:
                    return Response({"success": False, "message": "Incorrect password"})
            except ObjectDoesNotExist:
                return Response({"success": False, "message": "User does not exist"})
        else:
            # Return error response if serializer data is invalid
            return Response({"success": False, "errors": serializer.errors})
    

# --------- REST Framework --------------------

