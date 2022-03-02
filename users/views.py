# TODO: Rename FoodUser to member ?
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib import messages
from recipes.models import Recipe, Likes, Recommended, Keyword, Recently_recommended, Ingredient
from .models import FoodUser
from django.contrib.auth.models import User
from recipes.forms import RecipeForm #Import recipeform from Recipes
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm, ProfileForm, AddRecipeForm
from django.contrib.auth import login, logout,authenticate
from django.conf import settings
from datetime import date
import os

# Create your views here.
def register(request):
    if request.method == 'POST':
        # Get submitted form from POST
        form = RegistrationForm(request.POST)
        # Check if the form fields are valid
        if form.is_valid():
            # Create user and redirect to login page
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} sucessfully registered')
            FoodUser.objects.create(user=user)
            return redirect('login')
    else:
        # Not POST method
        form = RegistrationForm()
        return render(request, 'users/register.html', {'form':form})
    #   Failed registration, form invalid
    return render(request, 'users/register.html', {'form':form},status=400)

def profile(request):
    # 'profile' gets the user and modifies the profile if the user changed some values or redirects to his profile page.
    try:
        if request.user.is_authenticated:
            mainUser = request.user
            profileUser = FoodUser.objects.get(user=mainUser) #authenticated user
            recipes = Recipe.objects.filter(user=profileUser)
            liked_recipes = Likes.objects.filter(user=profileUser)
            rec = Recommended.objects.get(user=profileUser)
            recommended_recipe = rec.recipe
            if rec.date < date.today(): # recommends a new recipe if it has gone more than 1 day since last time
                Recently_recommended.remove_expired()
                recommended_recipe = Recommended.recommend_recipe(user=profileUser)
                rec.recipe = recommended_recipe
                rec.save()

            if recommended_recipe:
                recommended_recipe.timetomake = Recipe.parse_time(recommended_recipe.timetomake)
                recommended_recipe.recipe = Recipe.parse_recipe(recommended_recipe.recipe)
                recommended_recipe.difficulty = Recipe.parse_difficulty(recommended_recipe)

            for recipe in recipes:
                recipe.timetomake = Recipe.parse_time(recipe.timetomake)
                recipe.recipe = Recipe.parse_recipe(recipe.recipe)
                recipe.difficulty = Recipe.parse_difficulty(recipe)

            for liked_recipe in liked_recipes:
                liked_recipe.recipe.timetomake = Recipe.parse_time(liked_recipe.recipe.timetomake)
                liked_recipe.recipe.recipe = Recipe.parse_recipe(liked_recipe.recipe.recipe)
                liked_recipe.recipe.difficulty = Recipe.parse_difficulty(liked_recipe.recipe)

        else:
            return redirect('login')
    except FoodUser.DoesNotExist:
        return redirect('login')
    if request.method == 'POST':
        currentProfilePicPath = profileUser.image.path
        form = ProfileForm(request.POST, request.FILES, instance=profileUser, initial={'biography':profileUser.biography})
        currentImage = profileUser.image
        currentBiography = profileUser.biography
        if form.is_valid(): 
            if profileUser.image != currentImage and currentImage.name != 'default.jpg': #Deletes the old profile picture if the user has changed it, and keeps the old one if he didn't
                os.remove(currentProfilePicPath)
            if len(profileUser.biography) > 200:
                profileUser.biography = currentBiography
            form.save()
        return redirect('profile')
    else:
        form = ProfileForm(initial={'biography':profileUser.biography})
    return render(request, 'users/profile.html', {'profileUser' : profileUser, 'recipes': recipes, 'form':form,'liked_recipes':liked_recipes, 'recommended_recipe':recommended_recipe})

def login_view(request):
    # If user is already logged in, redirect to profile page
    if request.user.is_authenticated:   
        return redirect(profile)
    
    if request.method == 'POST':
        # Get login credentials from login form
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username,password=password)
            # If the credentials matches existing user, 
            # login and redirect to profile page
            if user!= None:
                login(request,user)
                return redirect('profile')
            else:
                # Login credentials incorrect
                messages.info(request, 'Username or password is incorrect')
    else:
        # Not a POST request
        form =LoginForm()
        return render(request, 'users/login.html', {'form':form})
    # Invalid login form
    return render(request, 'users/login.html', {'form':form},status=400)

#Allows a user to add his/her own recipes
def add_recipes_view(request):
    #Get the food user from the queryset
    if request.user.is_authenticated:
        actual_user = FoodUser.objects.filter(user=request.user).first()
        if request.method == 'POST':
            form = AddRecipeForm(request.POST, request.FILES) 
            if form.is_valid():
                
                add_recipe = form.save(commit=False)
                #Automatically post as logged in user
                add_recipe.user = actual_user
                add_recipe.save() #after this nothing executes, NLTK error
                for i in range(int(request.POST.get("submit"))):
                    Ingredient.objects.create(ingredient=request.POST.get("ingredient_"+str(i)+"_name"),amount=request.POST.get("ingredient_"+str(i)+"_amount"),measurement=request.POST.get("ingredient_"+str(i)+"_measurement"),recipe=add_recipe)
                return redirect('confirmation')
        else:
            form = AddRecipeForm()
        #Renders the html page with the add_recipe form 
        return render(request, 'users/addrecipe.html',{'form': form})
    else:
        return redirect('login')

def confirmation_page_view(request):

    if request.user.is_authenticated:
        try:
            #Get the latest recipe created
            added_recipe = Recipe.objects.latest('id')
            filter_keywords = Keyword.objects.filter(recipe=added_recipe)
    
        except Recipe.DoesNotExist:
                return redirect('profile')

        if request.method == 'POST':
            try:
                #Iterate over the user input(tags) and create a new keyword related to the recent recipe
                for key, value in request.POST.items():
                    #Ignore CSRF token when fetching inputs from user
                    if not key == "csrfmiddlewaretoken":
                        #Avoid empty tag
                        if len(value) >= 1:
                            new_keyword = Keyword.objects.create(word=value)
                            new_keyword.recipe.add(added_recipe)
                
            #Avoid duplicate tags            
            except IntegrityError:
                return redirect('confirmation')
         
            return redirect('/recipes')

        else:
            context = {'recipe': added_recipe,'keyword':filter_keywords}
            return render(request, 'users/confirmation.html', context)

        return render(request, 'users/confirmation.html', context)
    else:
        return redirect('login')

def user_profile(request, username):
    # If username is the client user, redirect to profile page
    if request.user.username == username:
        return redirect('profile')
    # Find user object with given username
    # and show their userprofile
    target = FoodUser.objects.get(user=User.objects.get(username=username))
    target_recipes = Recipe.objects.filter(user=target)
    return render(request, 'users/other_userprofiles.html',{'target_user':target, 'target_recipes':target_recipes})

# Logs out the authenticated user and redirect to homepage
def logout_view(request):
    logout(request)
    return redirect('/')
