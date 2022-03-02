from django.test import TestCase
from recipes.models import Recipe
from django.contrib.auth.models import User
from users.models import FoodUser

class RecipeViewTest(TestCase):
    def setUp(self):
        android = User.objects.create(username='android', password='verysecure123')
        u1 = FoodUser.objects.create(user=android, biography='What is life?')
        self.r1 = Recipe.objects.create(name='r1', timetomake=50, ingredients='r1 5g', recipe='Test', kcal=2000, user=u1)

    def test_recipe_url_resolve_to_recipe_page(self):
        response = self.client.get(f'/recipes/{self.r1.id}/')
        self.assertTemplateUsed(response, 'recipe.html')
    
    def test_context_has_the_recipe(self):
        response = self.client.get(f'/recipes/{self.r1.id}/')
        self.assertEqual(response.context['recipe'], self.r1)

    def test_redirect_when_recipe_does_not_exist(self):
        response = self.client.get('/recipes/99/')
        self.assertRedirects(response, '/recipes/')

class RecipesViewTest(TestCase):
    def test_recipe_url_resolve_to_recipe_page(self):
        android = User.objects.create(username='android', password='verysecure123')
        u1 = FoodUser.objects.create(user=android, biography='What is life?')
        r1 = Recipe.objects.create(name='r1', timetomake=50, ingredients='r1 5g', recipe='Test', kcal=2000, user=u1)
        response = self.client.get(f'/recipes/')
        self.assertTemplateUsed(response, 'recipes.html')