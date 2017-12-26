from django import forms
from models import UserModel,PostModel,LikeModel


class SignUpForm (forms.ModelForm):
    class Meta:
        model= UserModel
        fields=["name","email","username","password"]

class logInForm (forms.ModelForm):
    class Meta :
        model=UserModel
        fields=["username","password"]

class PostForm(forms.ModelForm):
    class Meta:
        model=PostModel
        field=["image","caption"]

class LikeForm(forms.ModelForm):
    class Meta:
        model=LikeModel
        field=["post"]