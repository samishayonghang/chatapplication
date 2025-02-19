from django.shortcuts import render,redirect
from.models import Codeform
from django.contrib import messages
from django.contrib.auth import get_user_model,authenticate,login
User=get_user_model()
user = User.objects.filter(username='samisha').first()
print(user)  # Should print the user object
print(user.check_password('samisha151'))  # Should return True if password is

# Create your views here.
def join(request):
    room_code = None  # Initialize room_code
    username = None  # Initialize username
    if request.method=="POST":
        room_code=request.POST.get('room_code')
        username=request.POST.get('username')
        codes=Codeform(room_code=room_code,username=username)
        codes.save()
    
        
        return redirect(f'/chat/{room_code}/',username=username)


        


    return render(request,'chand/join.html')


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('join')  
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(f"Username entered: {username}")
        print(f"Password entered: {password}")
        user=authenticate(request,username=username,password=password)
        if user is None:
            messages.error(request,'invalid username and  password')
            return redirect('loginpage')

        

        else:
         login(request,user)
         messages.success(request,'welcome to the chatapp')
         return redirect('join')
            
           
        
    return render(request,'chand/loginpage.html')

def signuppage(request):
    if request.method=="POST":
        email=request.POST.get('email')
        username=request.POST.get('username')
        password=request.POST.get('password1')
        confirmpassword=request.POST.get('password2')
        if password!=confirmpassword:
            messages.error(request,"passwords doesnot match")
            return redirect('signuppage')
        if User.objects.filter(username=username):
            messages.error(request,'username already taken')
            return redirect('signuppage')
        if User.objects.filter(email=email):
            messages.error(request,'Email already taken')
            return redirect('signuppage')
        


            
        user=User.objects.create_user(email=email,username=username,password=password)
        user.save()
        print("Password during sign-up:", password)

        messages.success(request,'Account created sucessfully')
        return redirect('loginpage')

        

    return render(request,'chand/signuppage.html')


def chat(request,room_code):
    username=request.GET.get('user')
    context={'room_code':room_code,'user':username}
    
    return render(request,'chand/chat.html',context)
