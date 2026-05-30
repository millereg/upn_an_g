from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm

def login_view(request):
    form = LoginForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect("dashboard:index")

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("dashboard:index")
            else:
                form.add_error(None, "Credenciales inválidas")
    return render(request, "acceso/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")
