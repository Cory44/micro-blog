from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import CustomUserCreationForm, CustomAuthForm, PostForm, ProfileImageForm
from django.contrib import messages
from .models import Post, User, UserProfile
from datetime import datetime

# Create your views here.

############################################
#
# Homepage view with form to create a post
# and display a feed of post by most recent
# published
#
############################################
def homepage(request):
    if request.user.is_authenticated:
        return redirect(f'/{request.user.username}')
    else:
        return render(request, 'micro/home.html')


###########################################
#
# Register view with a form to register a 
# user
#
##########################################
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(request, f"New account created: {username}")
            return redirect('micro:homepage')
        else:
            for msg in form.errors:
                for message in form.errors[msg]:
                    messages.error(request, f"{message}")

            return render(request, 'micro/register.html', {"form":form})

    form = CustomUserCreationForm()
    return render(request, 'micro/register.html', {"form":form})


###########################################
#
# Logout request, redirects to homepage
#
###########################################
def logout_request(request):
    logout(request)
    return redirect('micro:homepage')


###########################################
#
# Login view with a form for a user to 
# enter username and password
#
##########################################
def login_request(request):
    if request.method == "POST":
        form = CustomAuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect(f'/{user.username}')
            else:
                messages.error(request, "Invalid username or password")
        else:
             messages.error(request, "Invalid username or password")

    form = CustomAuthForm()
    return render(request, 'micro/login.html', {"form":form})


#########################################
#
# Profile view displays the user profile
# of a specified user and their posts
#
#########################################
def profile(request, username):

    if request.user.is_authenticated:
        if username in [user.username for user in User.objects.all()]:
            if request.method == "POST":
                profileForms(request)
            form = PostForm()
            form2 = ProfileImageForm()
            user = User.objects.get(username=username)
            follows = [follows for follows in request.user.userprofile.follows.all()]
            posts = Post.objects.order_by('-published')
            return render(request, 'micro/profile.html', {"follows":follows, "username":username, "user":user, "posts":posts, "form":form, "form2":form2})
        else:
            messages.error(request, "User does not exist")
            return redirect('micro:homepage')
    else:
        messages.error(request, "Login or signup to view this page")
        return redirect('micro:homepage')
        

def profileForms(request):
    if 'post' in request.POST:
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.published = datetime.now()
            post.save()
            return redirect(f'/{request.user.username}')
        else:
            messages.error(request, "Error!")
    elif 'image' in request.POST:
        userprofile = UserProfile.objects.get(user=request.user)
        form2 = ProfileImageForm(request.POST, request.FILES, instance=userprofile)
        if form2.is_valid():
            image = form2.save(commit=False)
            image.save()
            return redirect(f'/{request.user.username}')
        else:
            messages.error(request, "Error!")

def delete(request, id):
    post = Post.objects.get(id=id).delete()
    return redirect(f'/{request.user.username}')

def unfollow(request, id):
    user = UserProfile.objects.get(user=request.user)
    unfollow = UserProfile.objects.get(id=id)
    user.follows.remove(unfollow)
    return redirect('micro:homepage')

def follow(request, id):
    user = UserProfile.objects.get(user=request.user)
    follow = UserProfile.objects.get(id=id)
    user.follows.add(follow)
    return redirect('micro:homepage')
