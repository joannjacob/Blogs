from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Users, Blog, Like, Comment

from . import serializers

from .serializers import UserSerializer, BlogSerializer, CommentSerializer
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()


class UserList(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserSerializer


def home(request):
    return render(request, 'home.html')


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
            retypepassword = request.POST.get('retypepassword', '')
            question = request.POST.get('question', '')
            answer = request.POST.get('answer', '')

            obj = Users()
            obj.firstname = firstname
            obj.lastname = lastname
            obj.emailid = emailid
            obj.mobile = mobile
            obj.username = username
            obj.password = password
            obj.security_question = question
            obj.security_answer = answer
            obj.save()


            auth_user=User()
            auth_user.first_name=firstname
            auth_user.last_name = lastname
            auth_user.username = username
            auth_user.set_password(password)
            auth_user.is_superuser = 1
            auth_user.save()

            return render(request, 'home.html')
        else:
            return render(request, 'signup.html')


def add_blog(request):
    return render(request, 'add_blog.html')

def edit_blog(request):
    return render(request, 'edit_blog.html')

def edit_blogentry(request):
    if request.method == 'POST':
        if (request.POST.get('content') and request.POST.get('title')):
            current_user=request.user
            obj = Blog()

            obj.title = request.POST.get('title')
            obj.content = request.POST.get('content')
            obj.user=current_user
            obj.save()
            return render(request, 'user.html')
        else:
            return render(request, 'fail.html')




def add_blogentry(request):
    if request.method == 'POST':
        if (request.POST.get('content') and request.POST.get('title')):
            current_user = request.user
            obj = Blog()

            obj.title = request.POST.get('title')
            obj.content = request.POST.get('content')
            obj.user = current_user
            #obj.email = request.session['emailid']
            obj.save()
            return render(request, 'user.html')
        else:
            return render(request, 'fail.html')





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

def my_blogs(request):
    current_user = request.user
    all_contents = Blog.objects.filter(user=current_user)
    html = ''
    for content in all_contents:
        url = "" + str(content.id) + '/'
        html += '<a href="'+url+'">' + content.content + '</a><br>'



    return HttpResponse(html)


def new(request,pk):
    return render(request, 'success.html')

def myblogs_detail(request,content_id):

    try:
        all_contents = Blog.objects.get(id=content_id)
        all_comments = Comment.objects.filter(blog=content_id)
        if Like.objects.filter(user=request.user,blog=content_id):
            flag=True
        else:
            flag=False
    except Blog.DoesNotExist:
        raise Http404("Blog doesnt exist")
    return render(request, 'blog_details.html', {'all_blogs': all_contents,'all_comments' : all_comments,'flag':flag})


def myblog_editupdate(request, content_id):
    # return HttpResponse("<h2>Details: "+ str(content_id) +"</h2>")
    if request.method == 'POST':
        if (request.POST.get('edittedblog')):
            try:
                obj= Blog.objects.get(id=content_id)
                obj.content = request.POST.get("edittedblog")
                obj.save()
                return render(request, 'user.html')
            except Blog.DoesNotExist:
                raise Http404("Blog doesnt exist")
        else:
            return render(request, 'fail.html')


def all_blogs(request):
    all_contents = Blog.objects.all()
    html = ''
    for content in all_contents:
        url = "" + str(content.id) + '/all'
        html += '<a href="' + url + '">' + content.title + '</a><br>'

    return HttpResponse(html)



def allblogs_detail(request, content_id):
    # return HttpResponse("<h2>Details: "+ str(content_id) +"</h2>")
    try:
        all_contents = Blog.objects.get(id=content_id)
        all_comments = Comment.objects.filter(blog=content_id)
        if Like.objects.filter(user=request.user,blog=content_id):
            flag=True
        else:
            flag=False
    except Blog.DoesNotExist:
        raise Http404("Blog doesnt exist")
    return render(request, 'all_blogs.html', {'all_blogs': all_contents,'all_comments' : all_comments,'flag':flag})


def enter_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            obj = Users.objects.get(username=username)
            print(obj)
            if (obj is not None and obj.password == password):
                request.session['emailid'] = obj.emailid
                blogobj = Blog.objects.all()
                blogobj.email = request.session['emailid']
                return render(request, 'user.html')
            else:
                return render(request, 'login.html')
        except Users.DoesNotExist:
            return render(request, 'login.html')


def forgot_password(request):
    return render(request, 'forgot_password.html')


def password_update(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        question = request.POST.get('question', '')
        answer = request.POST.get('answer', '')

        try:
            obj = Users.objects.get(username=username)
            if (obj.security_question == question and obj.security_answer == answer):
                password = request.POST.get('password', '')
                obj.password = password
                obj.save()
                return render(request, 'login.html')
            else:
                return render(request, 'fail.html')
        except Users.DoesNotExist:
            return render(request, 'login.html')


def password_change(request):
    if request.method == 'POST':
        if (request.POST.get('password')):
            password = request.POST.get('password', '')
            obj = Users()
            obj.password = password
            obj.save()
            return render(request, 'login.html')
        else:
            return render(request, 'update_password.html')


def like(request, content_id):

    blogobj=Blog.objects.get(id=content_id)
    current_user = request.user
    obj=Like()
    obj.user=current_user
    obj.blog=blogobj
    obj.save()
    try:
        all_contents = Blog.objects.get(id=content_id)
        all_comments = Comment.objects.filter(blog=content_id)
        if Like.objects.filter(user=request.user,blog=content_id):
            flag=True
        else:
            flag=False
    except Blog.DoesNotExist:
        raise Http404("Blog doesnt exist")
    return render(request, 'all_blogs.html', {'all_blogs': all_contents,'all_comments' : all_comments,'flag':flag})

def add_comment(request,content_id):
    if request.method == 'POST':
        if (request.POST.get('comment')):
            blogobj = Blog.objects.get(id=content_id)
            current_user = request.user
            obj = Comment()
            obj.user = current_user
            obj.blog = blogobj
            obj.comment=request.POST.get("comment")
            obj.save()
            try:
                all_contents = Blog.objects.get(id=content_id)
                all_comments = Comment.objects.filter(blog=content_id)
                if Like.objects.filter(user=request.user, blog=content_id):
                    flag = True
                else:
                    flag = False
            except Blog.DoesNotExist:
                raise Http404("Blog doesnt exist")
            return render(request, 'all_blogs.html',
                          {'all_blogs': all_contents, 'all_comments': all_comments, 'flag': flag})
        else:
            return render(request, 'fail.html')







