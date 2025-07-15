from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.



@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST['username']
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, "⚠️ Username already taken!")
        else:
            user.username = username
            user.save()
            messages.success(request, "✅ Profile updated successfully!")
        return redirect('profile')
    return render(request, 'students/edit_profile.html', {'user': request.user})



def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Student added successfully!")
            return redirect('student_list')
    else:
        form = StudentForm()    
    return render(request, 'students/add.html',{'form': form})
@login_required(login_url='login')
def student_list(request):
    query = request.GET.get('q')
    if query:
        students = Student.objects.filter(name__icontains=query)
    else:    
        students = Student.objects.all()
    return render(request, 'students/list.html', {'students': students})

def update_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():

            form.save()
            messages.success(request, "✏️ Student updated successfully!")
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)    
    return render(request, 'students/edit.html', {'form': form})

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    messages.success(request, "❌ Student deleted successfully!")
    return redirect('student_list')




def signup(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'students/signup.html', {'error': '⚠️ Username already taken'})
        else:
            User.objects.create_user(username=username, password=password)
        
        return redirect('login')
    return render(request, 'students/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('student_list')
        else:
            return render(request, 'students/login.html', {'error': 'Invalid credentials'})
        
    return render(request, 'students/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile_view(request):
    user = request.user  
    return render(request, 'students/profile.html', {'user': user})




