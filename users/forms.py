from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm, PasswordResetForm, PasswordChangeForm
from .models import User , Issuse


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')




class ChangeUserDataForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': "form-control", "placeholder": "Email Address"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

        widgets = {
            'username': forms.TextInput(
                attrs={"class": "form-control", "placeholder": "User name"}),
            'email': forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Email"}),
            'first_name': forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First name"}),
            'last_name': forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last name"}),
        }


class IssuseForm(forms.ModelForm):
    report_text = forms.CharField(
        widget=forms.Textarea(
        attrs={
            "class": "form-control", 
            "id": "exampleFormControlTextarea1", 
            "rows": "12"},
        ))
    report_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(
        attrs={
            "class": "form-control",
            "value":"upload",
        }))


    class Meta:
        model = Issuse
        fields = ('report_text', 'report_image')
    

    # widgets = {
    #         'report_text': forms.TextInput(
    #             attrs={"class": "form-control", "id": "exampleFormControlTextarea1", "rows": "6"}),
    #     }

