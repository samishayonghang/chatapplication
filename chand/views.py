from django.shortcuts import render,redirect
from.models import Codeform
# Create your views here.
def home(request):
    room_code = None  # Initialize room_code
    username = None  # Initialize username
    if request.method=="POST":
        room_code=request.POST.get('room_code')
        username=request.POST.get('username')
        codes=Codeform(room_code=room_code,username=username)
        codes.save()
    
        
        return redirect(f'/chat/{room_code}/',username=username)


        


    return render(request,'chand/home.html')

def chat(request,room_code):
    username=request.GET.get('user')
    context={'room_code':room_code,'user':username}
    
    return render(request,'chand/chat.html',context)
    