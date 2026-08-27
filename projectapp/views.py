from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from projectapp.models import Post
from projectapp.forms import PostForm
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
 


def home(request):
    return render(request, "index.html")


def about(request):
    about_message = "This is a message for the about page from the backend"

    best_players = ["Messi", "Ronaldo", "Neymar", "Mbappe"]
    GOAT = "CR7"

    context = {
        "taofeek": about_message,
        "programmer_name": "CR9",
        "age": 23,
        "best_players": best_players,
        "GOAT": GOAT,
    }
    print(context)

    return render(request, "about.html", context)


def profile(request):
    me = {"name": "Awele", "class": "Python", "age": 23}

    return JsonResponse(me)


def posts(request):
    posts = Post.objects.all()
    context = {
        "posts": posts
    }
    return render(request, "posts.html", context)

def post(request, pk):
    # the_post = Post.objects.get(pk=pk)
    the_post = get_object_or_404(Post,pk=pk)
    context = {"post": the_post}
    return render(request, "post.html", context)



def display_form(request):
    return render(request, "user_form.html")



def submit_form(request):
    if request.method =="POST":
        name = request.POST.get("username")
        dept =request.POST.get("department")

        values = {"name": name, "department": dept}
        return JsonResponse(values)

    return redirect("user_form")


def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("posts")
    else:
        form = PostForm()

    form = PostForm()

    context = {"post_form":form}
    return render(request, "post_form.html", context)


def edit_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()

    else:
        form = PostForm(instance=post)

    context = {"post_form":form}
    return render(request, "post_form.html", context)

def create_user(request):

        if request.method == "POST":
            form = UserCreationForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "User Added Successfully")
        else:
            form = UserCreationForm()

        context = {"form": form, "form_name": "User Creation Form"}
        return render(request, "create_user.html", context)

def custom_create_user(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")


        # 1 -Check that there are no empty inputs
        if not (username and email and password and confirm_password):
            messages.error(request, "All fields are required")
            return redirect("custom_create_user")

        is_valid = True
        # 2 - see if the username exists
        if  User.objects.filter(username_iexact=username).exists():
            messages.error(request, "Usernmae taken")
            return redirect("custom_create_user")
            is_valid = False

        if User.objects.filter(email_iexact = email).exist():
            messages.error(request, "Email already taken")
            is_valid = False

        if password != confirm_password:
            messages.error(request, "Two passwords don't match")
            is_valid = False

        if  is_valid==False:
            return redirect("custom_create_user")

        created_user = User.objects.create_user(
            username=username, email=email, password=confirm_password
        )
        messages.success(
            request, f"Hi {created_user.username}! Your account has been created!"
        )
        return redirect("custom_create_user")

    
    return render(request, "custom_create_user.html")

  









