from django.shortcuts import render, HttpResponse, redirect
from blog.models import Blog, Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import math

# HTML Pages
def home(request):
    return render(request, 'index.html')

def blog(request):
    """
        Pagination Design and logic.  < -- can ask me
        check my Logic book TimeStamp : 1557-070721 < -- I will check here
    """

    no_of_posts = 3
    page = request.GET.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)

    blogs = Blog.objects.all()
    length = len(blogs)
    blogs = blogs[(page-1)*no_of_posts: page*no_of_posts]
    if page > 1:
        prev = page - 1
    else:
        prev = None
    if page < math.ceil(length/no_of_posts):
        nxt = page + 1
    else:
        nxt = None

    context = {'blogs': blogs, 'prev': prev, 'nxt': nxt}
    return render(request, 'bloghome.html', context)

def blogpost(request, slug):
    blog = Blog.objects.filter(slug=slug).first()
    context = {'blog': blog}

    return render(request, 'blogpost.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")

        if len(name) < 2 or len(email) < 4 or len(phone) < 10 or len(desc) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            ins = Contact(name=name, email=email, phone=phone, desc=desc)
            ins.save()
            messages.success(
                request, "Your message has been successfully sent")

    return render(request, 'contact.html')

def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        results = Blog.objects.filter(title__contains=searched)
        context = {'searched': searched, 'results': results}
        return render(request, 'search.html', context)
    else:
        return HttpResponse("Your search did not query any data")

# AUTHENTICATION APIs
def handleSignup(request):
    if request.method == 'POST':
        # get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for erroneous inputs
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('/')

        if not username.isalnum():
            messages.error(
                request, "Username should only contain letters and numbers")
            return redirect('/')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('/')

        # create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has been successfully created")
        return redirect('/')
    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):

    if request.method == 'POST':
        # get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "successfully logged in")
            return redirect('/')
        else:
            messages.error(request, 'Invalid Credentials, Please Try again')
            return redirect('/')
    return HttpResponse( '404- Not Found' )

def handleLogout(request):

    logout(request)
    messages.success(request, "successfully logged out")
    return redirect('/')
