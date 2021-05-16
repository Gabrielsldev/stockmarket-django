from django import forms
from .models import Stock
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["ticker"] #This "ticker is the variable ticker in line  in models.py"


class SignUpForm(UserCreationForm):
    email = forms.EmailField(help_text="",label="", widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Enter Email"})) # The widget is just for formatting the form
    first_name = forms.CharField(help_text="<strong>Can have html style</strong>", label="", max_length=20, widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"First Name"}))
    last_name = forms.CharField(help_text="", label="", max_length=20, widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Last Name"}))

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
    
    # For formatting the fields that are built in UserCreationForm
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs["class"] = "form-control"
        self.fields['username'].widget.attrs["placeholder"] = "Username"
        self.fields['username'].label = ""
        self.fields['username'].help_text = ""
        self.fields['password1'].widget.attrs["class"] = "form-control"
        self.fields['password1'].widget.attrs["placeholder"] = "Password"
        self.fields['password1'].label = ""
        self.fields['password1'].help_text = "<ul class='form-text text muted'><li>Rule 1</li><li>Rule 2</li><li>Rule 3</li><li>Rule 4</li></ul>" # Comentar essa linha para ver quais são as regras
        self.fields['password2'].widget.attrs["placeholder"] = "Confirm Password"
        self.fields['password2'].widget.attrs["class"] = "form-control"
        self.fields['password2'].label = ""
        self.fields['password2'].help_text = ""


class EditProfileForm(UserChangeForm):
    password = forms.CharField(label="", widget=forms.TextInput(attrs={"type":"hidden"})) # Doesn't let the password field show up on page, since it appears with part of the hash number
    class Meta:
        model = User
        # exclude = () -> In case I want to exclude fields
        fields = ("username", "first_name", "last_name", "email", "password") # If I want to pass only some fields
    