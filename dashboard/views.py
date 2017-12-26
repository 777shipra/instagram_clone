# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,redirect
from datetime import datetime
from forms import SignUpForm,logInForm,PostForm
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponse
from models import UserModel, SessionToken , PostModel
from imgurpython import ImgurClient
from Django.settings import BASE_DIR,IMGUR_CLIENT_ID,IMGUR_CLIENT_SECRET
import os




def signup_view(request):
    if request.method =='Get':
        form= SignUpForm()
        today=datetime.now()
        return render(request,"signup.html",{"tareekh":today},{"form":form})
    else:
        form =SignUpForm(request.POST)
        if form.is_valid():
            name= form.cleaned_data['name']
            email= form.cleaned_data['email']
            password= form.cleaned_data['password']
            username= form.cleaned_data['username']

            #save data
            new_user=UserModel(name=name,email=email,username=username,password=make_password(password))
            new_user.save()
            return render(request,"success.html")

def login_view(request):
    if check_validation(request)==None: #if check validation returns none follow the precedure
        if request.method=="GET":
            login_form=logInForm()
            return render(request, "login.html",{"form":login_form})

        else:
            #when request is post
            login_form=logInForm(request.POST)
            if login_form.is_valid():
                #seperate data
                uname=login_form.cleaned_data["username"]
                pwsd=login_form.cleaned_data["password"]
                #check user in db ot not
                user=UserModel.objects.filter(username=uname).first()
                if user:
                    #if there is a user compare password
                    if check_password(pwsd,user.password):
                        new_session=SessionToken(user=user)#mapping with unique key
                        new_session.create_token()#creating a unique token
                        new_session.save()#save the token in db
                        #redirect to feed
                        response=redirect("/feed")
                        response.set_cookie(key='session_token',value=new_session.session_token)
                        return response
                        #login successful
                        return HttpResponse("login is successfull")
                    else:
                        return HttpResponse("login failed")
                else:
                    return HttpResponse("username doesnot exit")
            else:
                return HttpResponse("formm data is not valid")
    else:
        return redirect('/feed')


def feed_view(request):
    user=check_validation(request)
    if user:
        #user is already logged in
        #get all posts from db
        posts= PostModel.objects.all().order_by('-created_on')
        return render(request,'feed.html',{'all_posts':posts})
    else:
        #user is not authenticated
        return redirect('/login/')

def like_view(request):
    user=check_validation(request)
    if user:
        pass
    else:
        return redirect('/login/')


#it is used to make to check whether user is already logged in before redirecting the user to feed
def check_validation(request):
    if request.COOKIES.get("session_token"):
        session=SessionToken.objects.filter(session_token=request.COOKIES.get("session_token")).first()#check the token value frm database
        if session: #if it has some value
            return session.user #login with the user
        else:
            return None#don't
    else:
        return None

def post_view(request):
    valid_user=check_validation(request)
    if valid_user:
        if request.method =='Get':
            form=PostForm
            return render(request,"post.html",{"post_form":form})
        else:
            form=PostForm(request.POST,request.FILES)
            if form.is_valid():
                uploaded_image=form.cleaned_data.get('image')
                caption=form.cleaned_data.get('caption')
                new_post=PostModel(user=valid_user,image=uploaded_image,caption=caption)
                new_post.save()
                path=os.path.join(BASE_DIR,new_post.image.url)

                client=ImgurClient(IMGUR_CLIENT_ID,IMGUR_CLIENT_SECRET)
                new_post.image_url=client.upload_from_path(path,annon=True)['link']
                new_post.save()

                return redirect("/feed/")
    else:
        return redirect("/login/")
