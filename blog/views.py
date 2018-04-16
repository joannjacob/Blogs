from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User,Blog,Like,Comment

from . import serializers
from .models import User, Blog, Comment
from .serializers import UserSerializer, BlogSerializer, CommentSerializer
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer




def home(request):
    return render(request,'home.html')

def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    return render(request, 'home.html')

def add_signup(request):
    if request.method == 'POST':
        if (request.POST.get('firstname') and request.POST.get('lastname') and
            request.POST.get('emailid') and request.POST.get('mobile') and request.POST.get('username') and
            request.POST.get('password') and request.POST.get('retypepassword')
            and request.POST.get('question') and request.POST.get('answer')):

            firstname = request.POST.get('firstname', '')
            lastname = request.POST.get('lastname', '')
            emailid = request.POST.get('emailid', '')
            mobile = request.POST.get('mobile', '')

            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            retypepassword=request.POST.get('retypepassword', '')
            question=request.POST.get('question','')
            answer=request.POST.get('answer','')

            if(password != retypepassword):
                return render(request, 'signup.html')
            else:
                obj=User()
                obj.firstname = firstname
                obj.lastname = lastname
                obj.emailid = emailid
                obj.mobile = mobile
                obj.username=username
                obj.password = password
                obj.security_question = question
                obj.security_answer = answer
                obj.save()
                return render(request, 'login.html')
        else:
            return render(request,'signup.html')

def add_blog(request):
      return render(request,'add_blog.html')



def add_blogentry(request):
    if request.method == 'POST':
        if (request.POST.get('content') and request.POST.get('title')):

            obj=Blog()
            obj.title=request.POST.get('title')
            obj.content=request.POST.get('content')
            obj.email=request.session['emailid']
            obj.save()
            return render(request, 'user.html')
        else:
            return render(request,'fail.html')

def my_blogs(request):
    all_contents = Blog.objects.filter(email=request.session['emailid'])
    html = ''
    for content in all_contents:
        url = "/my_blogs/" + str(content.id) + '/'
        html += '<a href="' + url + '">' + content.content + '</a><br>'
    return HttpResponse(html)


'''class MyBlogs(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'my_blogs.html'

    def get(self, request):
        queryset = Blog.objects.filter(email=request.session['emailid'])
        serializer_class = BlogSerializer
        return Response({'myblogs':queryset})
    

def all_blogs(request):

    myblogs=Blog.objects.all()
    return render(request,'my_blogs.html',{'myblogs':myblogs})
'''

def all_blogs(request):
    all_contents = Blog.objects.all()
    html = ''
    for content in all_contents:
        url = "/all_blogs/" + str(content.id) + '/'
        html += '<a href="' + url + '">' + content.content + '</a><br>'
    return HttpResponse(html)

def detail(request,content_id):
    #return HttpResponse("<h2>Details: "+ str(content_id) +"</h2>")
    try:
        all_contents=Blog.objects.get(id=content_id)
    except Blog.DoesNotExist:
        raise Http404("Blog doesnt exist")
    return render(request, 'all_blogs.html', {'all_blogs': all_contents})



def enter_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            obj=User.objects.get(username=username)
            print(obj)
            if(obj is not None and obj.password==password):
                request.session['emailid'] = obj.emailid
                blogobj=Blog.objects.all()
                blogobj.email=request.session['emailid']
                return render(request, 'user.html')
            else:
                return render(request, 'login.html')
        except User.DoesNotExist:
            return render(request, 'login.html')

def forgot_password(request):
    return render(request, 'forgot_password.html')

def password_update(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        question = request.POST.get('question', '')
        answer=request.POST.get('answer', '')

        try:
            obj=User.objects.get(username=username)
            if(obj.security_question==question and obj.security_answer==answer):
                password = request.POST.get('password', '')
                obj.password = password
                obj.save()
                return render(request, 'login.html')
            else:
               return render(request, 'fail.html')
        except User.DoesNotExist:
            return render(request, 'login.html')

def password_change(request):
    if request.method == 'POST':
        if (request.POST.get('password')):
            password = request.POST.get('password', '')
            obj=User()
            obj.password = password
            obj.save()
            return render(request, 'login.html')
        else:
            return render(request,'update_password.html')



def like_button_clicked(request, blog_id):

    if request.user.is_authenticated():
        blog = Blog.objects.get(id=blog_id)

        liked, created = Like.objects.get_or_create(
            user=request.user,
            blog=blog,
            defaults={'timestamp': datetime.now()}
        )

        if not created:
            liked.delete()

        return render(request, 'success.html')
    else:
        return render(request, 'fail.html')






