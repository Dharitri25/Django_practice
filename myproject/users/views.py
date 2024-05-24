from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

# Create your views here.
# user registration and login
def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect("post:list")
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

# user login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if "next" in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("post:list")
    else:
        form  = AuthenticationForm()
    return render(request, "users/login.html", {'form': form})

# log out
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("user:login")
    