from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm, SignUpForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm



# Create your views here.

def home(request):

    import requests
    import json

    if request.method == "POST": # POST method from search from the base.html file
        ticker = request.POST["ticker"] # This "ticker" is the name of the form
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_5dbda0311aff4b68bcfe7ed258029ba4")

        # Error handling
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error..."
        return render(request, "home.html", {"api": api}) # The key "api" receives the value from the variable api. The key is used in the home.htlm file
    
    else:
        return render(request, "home.html", {"ticker": "Enter a ticker"})


def about(request):
    return render(request, "about.html", {})


def add_stock(request):
    import requests
    import json
    
    if request.method == "POST": # POST method from add stock from the add_stock.html file
        form = StockForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, ("Stock has been added."))
            return redirect("add_stock")

    else:
        stocks_from_db = Stock.objects.all()
                
        output = []
        for ticker_item in stocks_from_db:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_5dbda0311aff4b68bcfe7ed258029ba4")

            # Error handling
            try:
                api = json.loads(api_request.content)
                output.append(api)
            except Exception as e:
                api = "Error..."

        return render(request, "add_stock.html", {"stocks_from_db":stocks_from_db, "output":output})


def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("Stock deleted."))

    return redirect("add_stock")
    

def delete_stock(request):
    stocks_from_db = Stock.objects.all()
    return render(request, "delete_stock.html", {"stocks_from_db":stocks_from_db})

# Functions to control login:

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in"))
            return redirect("home")
        else:
            messages.success(request, ("Error: Not logged in"))
            return redirect("login")
    else:
        return render(request, "login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, ("Logged out"))
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"] #To authenticate the user after registering. Note that doesn't
            password = form.cleaned_data["password1"] # use the POST method like in the login function.
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, ("You have registred"))
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "register.html", {"form":form})


def edit_profile(request):
    if request.method == "POST":
        # form = UserChangeForm(request.POST, instance=request.user) Before I added the class EditProfileForm(UserChangeForm) in forms.py
        form = EditProfileForm(request.POST, instance=request.user)  # After I added the class EditProfileForm(UserChangeForm) in forms.py
        if form.is_valid():
            form.save()
            messages.success(request, ("Changes Saved"))
            return redirect("home")
    else:
        # form = UserChangeForm(instance=request.user)
        form = EditProfileForm(instance=request.user)
    return render(request, "edit_profile.html", {"form":form})

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, ("Changed Password"))
            return redirect("home")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "change_password.html", {"form":form})