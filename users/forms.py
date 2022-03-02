from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import FoodUser
from recipes.models import Recipe
from recipes.models import Ingredient

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
        }
        
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
    
class ProfileForm(forms.ModelForm):

    biography = forms.CharField(required=False)
    image = forms.ImageField(required=False)
    class Meta:
        model = FoodUser
        fields = ['biography','image']

class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'timetomake', 'image', 'recipe', 'difficulty']
        labels = {"timetomake": "Time to make"}


