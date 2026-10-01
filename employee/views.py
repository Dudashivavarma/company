import json

from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import EmployeeDetails
from django.views.decorators.csrf import csrf_exempt
import bcrypt
from .serializer import EmployeeDetailsSerializer
# Create your views here.
from django.conf import  settings
from django.template.loader import render_to_string 
from django.core.files.storage import FileSystemStorage
mail=settings.DEFAULT_FROM_EMAIL

@csrf_exempt
def entry_page(req):
    valid=False
    if req.method=='POST':
        username=req.POST.get('username')
        password=req.POST.get('password')
        emp_name=EmployeeDetails.objects.get(username=username)
        if password==emp_name.password:
            response=JsonResponse({'status':'Cookiee set'})
            response.set_cookie(
                key='logged_in',
                value=True,
                # httponly=True,

            )
            return response
        else:
            valid=True
            return render(req,'login.html',{'valid':valid})
    return render(req,'login.html',{'valid':valid})

def home(req):
    if 'username' in req.session:
        return JsonResponse({'status':'Welcome to home page'})
    else:
        return JsonResponse({'status':'Login first..!'})
    # print(req.COOKIES.get('logged_in'))
    # if req.COOKIES.get('logged_in')=='True':
    #     return HttpResponse('Welcome to home page')
    # else:
    #     return JsonResponse({'status':'Login first..!'})
    # return HttpResponse('WELCOME TO HOME PAGE')

def dark_theme(req):
    response=JsonResponse({'status':'Themeset..!'})
    response.set_cookie(
        key='Theme',
        value='Dark'
    )
    return response


def delete(req):
    req.session.flush()
    return JsonResponse({'status':'session deleted'})
    # response=JsonResponse({'status':'logged out'})
    # response.delete_cookie('logged_in')
    # return response

@csrf_exempt
def register(req):
    json_data=json.loads(req.body)
    inp_pass=json_data.get('password')
    print(inp_pass)
    encoded=inp_pass.encode('utf-8')
    salt=bcrypt.gensalt(rounds=12)
    hash_password=bcrypt.hashpw(encoded,salt).decode('utf-8')
    json_data['password']=hash_password
    new_data=EmployeeDetailsSerializer(data=json_data)
    if new_data.is_valid():
        new_data.save()
        return JsonResponse({'status':'registerd successfully'})
    else:
        return JsonResponse({'status':'invalid details'})

@csrf_exempt
def login_in(req):
    json_data=json.loads(req.body)
    emp_obj=EmployeeDetails.objects.get(username=json_data['username'])
    inp_data=json_data['password']
    encoded=inp_data.encode('utf-8')
    if bcrypt.checkpw(encoded,emp_obj.password.encode('utf-8')):
        return JsonResponse({'status':'login success'})
    else:
        return JsonResponse({'status':'login failed'})


@csrf_exempt
def update(req):
    json_data=json.loads(req.body)
    emp_obj=EmployeeDetails.objects.get(username=json_data['username'])
    encoded=json_data['password'].encode('utf-8')
    salt=bcrypt.gensalt(rounds=12)
    hashed_password=bcrypt.hashpw(encoded,salt).decode('utf-8')
    json_data['password']=hashed_password
    update_pass=EmployeeDetailsSerializer(emp_obj,data=json_data,partial=True)
    if update_pass.is_valid():
        update_pass.save()
        return JsonResponse({'status':'updated'})
    else:
        return JsonResponse({'status':'incorrect details'})




def disaply(req):
    req.session['username']='ajay'
    return JsonResponse({'status':'session set'})


    
def sending_mail(req):
    html_content = render_to_string("main.html",{"name": "SHIVAVARMA"})     
    email = EmailMultiAlternatives(         
        subject="Welcome",         
       body="Welcome to our website.",         
       from_email=mail,         
       to=["dudashivavarma@gmail.com"]     )     
    email.attach_alternative(html_content,"text/html")     
    email.send()     
    return HttpResponse("Email Sent") 

@csrf_exempt
def store(req):
    if 'resume' in req.FILES:
        fs=FileSystemStorage(location='media/pdf')
        fs.save(req.FILES['resume'].name,req.FILES['resume'])
        return JsonResponse({'status':'file received'})
    return JsonResponse({'status':'file required'})



def middleware(req):
    return JsonResponse({'status':'middleware'})
    