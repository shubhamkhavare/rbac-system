from contextlib import redirect_stderr
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import CustomUser, profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser, API

def UserLogin(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        try:
            user = CustomUser.objects.get(username=username)
            if user.password == password:
                refresh = RefreshToken.for_user(user)
                tokens = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                token1, _ = profile.objects.get_or_create(user_id=user.pk)
                token1.token = tokens['access']
                token1.save()

                request.session['access_token'] = tokens['access']
                
                if user.role == "Admin":
                    return render(request, "admin.html")
                elif user.role == "User":
                    return render(request, "user.html")
                elif user.role == "Viewer":
                    return render(request, "viewer.html")
            else:
                return HttpResponse("Invalid Credentials")
        except CustomUser.DoesNotExist:
            return HttpResponse("Username does not exist")
    else:
        request.session.clear()
        return render(request, 'login.html')

def add_user(request):
    if 'access_token' in request.session:
        token = AccessToken(request.session.get('access_token'))
        user = CustomUser.objects.get(id=token['user_id'])
        if user.role == 'Admin':
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                role = request.POST['role']
                            
                if CustomUser.objects.filter(username=username).exists():
                    return HttpResponse("Username already exists")
                            
                selected_apis = request.POST.getlist('API')
                new_user = CustomUser(username=username, password=password, role=role)
                new_user.save()
                new_user.apis.set(API.objects.filter(api_name__in=selected_apis))
                return HttpResponse("User Added Successfully")
            else:
                apis = API.objects.all()
                return render(request, 'add_user.html', {'apis':apis})
        else:
            return HttpResponse("Only Admin can access this page")
    else:
        return HttpResponse('No User Logged in')               
    
    
def add_api(request):
    if 'access_token' in request.session:
        token = AccessToken(request.session.get('access_token'))
        user = CustomUser.objects.get(id=token['user_id'])
        if user.role == 'Admin' or user.role == 'User':
            if request.method == 'POST':
                api = request.POST['api']
                if API.objects.filter(api_name=api).exists():
                    return HttpResponse("API Already exists")
                else:
                    new_api = API.objects.create(api_name=api)
                return HttpResponse("API added Succesfully")
            else:
                return render(request, "add_api.html")
        else:
                return HttpResponse("Only Admin and User can access this page")
    else:
        return HttpResponse("No user Logged in")


def remove_user(request):
    if 'access_token' in request.session:
        token = AccessToken(request.session.get('access_token'))
        user = CustomUser.objects.get(id=token['user_id'])
        if user.role == 'Admin':
            if request.method == 'POST':
                username = request.POST['username']
                try:
                    user = CustomUser.objects.get(username=username)
                    user.delete()
                    return HttpResponse("User Removed Successfully")
                except CustomUser.DoesNotExist:
                    return HttpResponse("User not found")
            else:
                return render(request, "remove_user.html")
        else:
            return HttpResponse("Only Admin can access this page") 
    else:
        return HttpResponse("No user Logged in")   


def update_user(request):
    if 'access_token' in request.session:
        token = AccessToken(request.session.get('access_token'))
        user = CustomUser.objects.get(id=token['user_id'])
        if user.role == 'Admin':
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                role = request.POST['role']
                selected_apis = request.POST.getlist('API')

                try:
                    user = CustomUser.objects.get(username=username)
                    if password != "":
                        user.password = password
                    if role != "":
                        user.role = role
                    user.save()
                    user.apis.set(API.objects.filter(api_name__in=selected_apis))
                    return HttpResponse('User Updated Successfully')  
                except CustomUser.DoesNotExist:
                    return HttpResponse('User not found')
            else:
                apis = API.objects.all()
                return render(request, "update_user.html", {'apis':apis})
        else:
            return HttpResponse("Only Admin can access this page")
    else:
        return HttpResponse("User not logged in")
    
def remove_api(request):
    if 'access_token' in request.session:
        token = AccessToken(request.session.get('access_token'))
        user = CustomUser.objects.get(id=token['user_id'])
        if user.role == 'Admin':
            if request.method == 'POST':
                api = request.POST['api_name']
                try:
                    user = API.objects.get(api_name=api)
                    user.delete()
                    return HttpResponse("API Removed Successfully")
                except API.DoesNotExist:
                    return HttpResponse("API does not exist")
            else:
                return render(request, "remove_api.html")
        else:
            return HttpResponse("Only Admin can access this page")
    else:
        return HttpResponse("User not logged in")


def update_api(request):
    if 'access_token' in request.session:
        token = AccessToken(request.session.get('access_token'))
        user = CustomUser.objects.get(id=token['user_id'])
        if user.role == 'Admin' or user.role == 'User':
            if request.method == 'POST':
                try:
                    apiname = request.POST['apiname']
                    updatenname = request.POST['updatename']     
                    user = API.objects.get(api_name=apiname)
                    user.api_name = updatenname
                    user.save()
                    return HttpResponse('API Updated Successfully')  
                except API.DoesNotExist:
                    return HttpResponse('API not found')
            else:
                return render(request, "update_api.html")
        else:
            return HttpResponse("Only Admin and User can access this page")
    else:
        return HttpResponse("User not logged in")
    
def view_api(request):
    user = CustomUser.objects.prefetch_related('apis')
    return render(request, 'view_api.html', {'user_api': user})

def home(request):
    return render(request, "home.html")



# jsonresult = json.loads(request.body)

#                 if CustomUser.objects.filter(username=jsonresult['username']).exists():
#                     return HttpResponse("Username already exists")
                            
#                 selected_apis = request.POST.getlist('API')
#                 new_user = CustomUser(username=jsonresult['username'], password=jsonresult['password'], role=jsonresult['role'])
#                 new_user.save()
#                 new_user.apis.set(API.objects.filter(api_name__in=selected_apis))
#                 return HttpResponse("User Added Successfully")

