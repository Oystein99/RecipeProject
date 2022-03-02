from django.shortcuts import redirect, render
from .models import Recipe,Ratings, Likes, Ingredient
from django.http import JsonResponse
import os
from django.urls import reverse
from django.conf import settings
from django.shortcuts import render
from django.templatetags.static import static
from django.contrib.auth.models import User
from users.models import FoodUser
from django.contrib import messages
from django.db import IntegrityError
# Create your views here.
def index(request):
    meals = Recipe.objects.all()
    for meal in meals:
        meal.timetomake = Recipe.parse_time(meal.timetomake)
        meal.recipe = Recipe.parse_recipe(meal.recipe)
        meal.difficulty = Recipe.parse_difficulty(meal)

    context = {'recipes': meals}

    return render(request, 'index.html', context)


def recipes(request):
    if request.method == 'POST':
        meals = Recipe.objects.filter(name__contains=request.POST.get('search'))
        
    else: 
        meals = Recipe.objects.all()
    for meal in meals:
        meal.timetomake = Recipe.parse_time(meal.timetomake)
        meal.recipe = Recipe.parse_recipe(meal.recipe)
        meal.difficulty = Recipe.parse_difficulty(meal)

    context = {'recipes': meals}
    return render(request, 'recipes.html', context)

def recipepage(request, recipe_id):
    try:
        meal = Recipe.objects.get(id=recipe_id)
    except Recipe.DoesNotExist:
        return redirect('recipes')

    ingredients = Ingredient.objects.filter(recipe=meal)

    meal.num_ratings = Recipe.sum_rating(meal)
    meal.rating = Recipe.calculate_rating(meal, meal.num_ratings)
    meal.save()
    meal.timetomake = Recipe.parse_time(meal.timetomake)
    meal.recipe = Recipe.parse_recipe(meal.recipe)
    meal.difficulty = Recipe.parse_difficulty(meal)

    if request.user.is_authenticated:
        try:
            like = Likes.objects.get(recipe=meal, user=FoodUser.objects.get(user=request.user))
            context = {'recipe': meal, 'ingredients': ingredients, 'rating' : range(meal.rating), 'empty_stars':range(5-meal.rating),'like':like}
        except:
            context = {'recipe': meal, 'ingredients': ingredients, 'rating' : range(meal.rating), 'empty_stars':range(5-meal.rating)}
    else:
        context = {'recipe': meal, 'ingredients': ingredients, 'rating' : range(meal.rating), 'empty_stars':range(5-meal.rating)}
    return render(request, 'recipe.html', context)


def rate_view(request):
    user = request.user
    # User must be authenticated to rate recipes
    if user.is_authenticated:
        if request.method == 'POST':
            # Get recipe object with id
            recipe_id = request.POST.get('recipe_id')
            recipe = Recipe.objects.get(id=recipe_id)
            # What rating the user rates recipe 
            rating = int(request.POST.get('rating'))
            url= f"/recipes/{int(recipe_id)}/"
            try:
                # Try to create rating object to rate recipe.
                # Will fail if user has already rated this recipe
                Ratings.objects.create(recipe=recipe,user= FoodUser.objects.get(user=user),rating=rating)
                # Update rating
                if rating:
                    if rating == 1:
                        recipe.one_star = recipe.one_star + 1
                    elif rating == 2:
                        recipe.two_star = recipe.two_star + 1
                    elif rating == 3:
                        recipe.three_star = recipe.three_star + 1
                    elif rating == 4:
                        recipe.four_star = recipe.four_star + 1
                    elif rating == 5:
                        recipe.five_star = recipe.five_star + 1

                    recipe.save()
                    recipe = Recipe.objects.get(id=recipe_id)
                    # Success message
                    messages.success(request, f'Successfully rated with {rating}')
                    return JsonResponse({'success':'true','url':url})
            except IntegrityError:
                #User has already rated this recipe
                messages.warning(request,"You've already rated this recipe!")
                return JsonResponse({'success':'already_rated','url':url})
    errmsg = "User not authenticated!"
    return JsonResponse({'success':'false','errmsg':errmsg})


def like_view(request):
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            recipe_id = request.POST.get('recipe_id')
            recipe = Recipe.objects.get(id=recipe_id)
            try:
                Likes.objects.create(recipe = recipe,user = FoodUser.objects.get(user=user),like = True)
                recipe.save()
                recipe = Recipe.objects.get(id=recipe_id)
                return recipepage(request,recipe_id)
            except:
                Likes.objects.get(recipe = recipe,user = FoodUser.objects.get(user=user)).delete()
                recipe.save()
                recipe = Recipe.objects.get(id=recipe_id)   
                return redirect('recipe', recipe_id=recipe_id)
    return redirect('recipes')



