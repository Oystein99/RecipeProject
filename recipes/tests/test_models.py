from django.test import TestCase
from django.core.exceptions import ValidationError
from recipes.models import Recipe, Document, Word, Keyword, Ingredient, KeywordScore, RecipeScore, Ratings
from django.contrib.auth.models import User
from users.models import FoodUser
import datetime

class RecipeModelTest(TestCase):
    def setUp(self):
        android = User.objects.create(username='android', password='verysecure123')
        self.u1 = FoodUser.objects.create(user=android, biography='What is life?')
        Recipe.objects.create(name='test1', timetomake=30, ingredients='this needs to be changed', recipe='food and food', kcal=2000, user=self.u1)
        Recipe.objects.create(name='test2', timetomake=30, ingredients='test g', recipe='same recipe', kcal=2000, user=self.u1)
    
    def tearDown(self):
        User.objects.filter(username='android').delete()
        FoodUser.objects.filter(biography='What is life?').delete()
        
    def test_illegal_difficulty_label(self):
        wrong_diff = Recipe(name='Pizza', timetomake=30, difficulty='Super Hard', ingredients="1 Grandiosa Pepperoni", recipe='Put in oven', kcal=2000, user=self.u1)
        with self.assertRaises(AssertionError):
            self.assertIn(wrong_diff.difficulty, Recipe.Difficulty.labels)
    
    def test_illegal_difficulty_value(self):
        wrong_diff = Recipe(name='Pizza', timetomake=30, difficulty='SH', ingredients="1 Grandiosa Pepperoni", recipe='Put in oven', kcal=2000, user=self.u1)
        with self.assertRaises(AssertionError):
            self.assertIn(wrong_diff.difficulty, Recipe.Difficulty.values)
        
    def test_unique_recipe(self):
        same_recipe = Recipe(name='test3', timetomake=40, ingredients='test mL', recipe='same recipe', kcal=2000, user=self.u1)
        with self.assertRaises(ValidationError):
            same_recipe.validate_unique()
        
    def test_too_large_name(self):
        bigname = 'a'*101
        large = Recipe(name=bigname, timetomake=30, difficulty='M', ingredients="some ingredients", recipe='long recipe', kcal=2000, user=self.u1)
        with self.assertRaises(ValidationError):
            large.full_clean()

class WordModelTest(TestCase):  
    def setUp(self):
        android = User.objects.create(username='android', password='verysecure123')
        self.u1 = FoodUser.objects.create(user=android, biography='What is life?')
        Recipe.objects.create(name='test1', timetomake=30, ingredients='this needs to be changed', recipe='food and food', kcal=2000, user=self.u1)
        
    def test_words_created(self):
        word_food = Word.objects.filter(word='food')
        self.assertEqual(word_food[0].occurence, 2)

class KeywordModelTest(TestCase):
    def setUp(self):
        android = User.objects.create(username='android', password='verysecure123')
        self.u1 = FoodUser.objects.create(user=android, biography='What is life?')
        reciep = 'Combine water, stock, celery, carrots, onion, garlic, parsley, thyme, paprika, salt, black pepper, and bay leaf in a pot. Bring to a simmer, cover, and cook until vegetables are soft, 20 to 30 minutes. \n Add cooked chicken and squash to the pot and simmer until squash is tender, about 10 minutes more.'
        self.recipe1 = Recipe.objects.create(name='test1', timetomake=30, ingredients='this needs to be changed', recipe=reciep, kcal=2000, user=self.u1)
        
    def test_keywords_created(self):
        doc = Document.objects.get(recipe=self.recipe1)
        self.assertEqual(doc.numKeywords, 10)
    
    def test_unique_keywords(self):
        keywords = Keyword.objects.filter(recipe=self.recipe1)
        for word in keywords:
            word.validate_unique()

class IngredientModelTest(TestCase):
    def setUp(self):
        android = User.objects.create(username='android', password='verysecure123')
        self.u1 = FoodUser.objects.create(user=android, biography='What is life?')
        self.recipe1 = Recipe.objects.create(name='test1', timetomake=30, ingredients='', recipe='food and food', kcal=2000, user=self.u1)
        self.ing1 = Ingredient.objects.create(recipe=self.recipe1, ingredient='salt', amount=1, measurement='TeS')
        self.ing2 = Ingredient.objects.create(recipe=self.recipe1, ingredient='butter', amount=150, measurement='G')
        self.wrongIng1 = Ingredient.objects.create(recipe=self.recipe1, ingredient='tester', amount=34, measurement='Big spoon')
        self.wrongIng2 = Ingredient.objects.create(recipe=self.recipe1, ingredient='tester', amount=34, measurement='BS')
    
    def test_ingredients_connected(self):
        ingredients = Ingredient.objects.filter(recipe=self.recipe1)
        self.assertEqual(self.ing1, ingredients[0])
        self.assertEqual(self.ing2, ingredients[1])
    
    def test_illegal_measurement_label(self):
        with self.assertRaises(AssertionError):
            self.assertIn(self.wrongIng1.measurement, Ingredient.Measurement.labels)
    
    def test_illegal_measurement_value(self):
        with self.assertRaises(AssertionError):
            self.assertIn(self.wrongIng2.measurement, Ingredient.Measurement.values)

class ScoreModelTest(TestCase):
    def setUp(self):
        android = User.objects.create(username='android', password='verysecure123')
        self.u1 = FoodUser.objects.create(user=android, biography='What is life?')
        legion = User.objects.create(username='legion', password='geth123')
        self.u2 = FoodUser.objects.create(user=legion, biography='Does this unit have a soul?') 

        reciep = 'Combine water, stock, celery, carrots, onion, garlic, parsley, thyme, paprika, salt, black pepper, and bay leaf in a pot. Bring to a simmer, cover, and cook until vegetables are soft, 20 to 30 minutes. \n Add cooked chicken and squash to the pot and simmer until squash is tender, about 10 minutes more.'
        self.recipe1 = Recipe.objects.create(name='test1', timetomake=30, ingredients='this needs to be changed', recipe=reciep, kcal=2000, user=self.u1)
        
        self.rating1 = 4
        Ratings.objects.create(recipe=self.recipe1, user=self.u1, rating=self.rating1)
        self.rating2 = 5
        Ratings.objects.create(recipe=self.recipe1, user=self.u2, rating=self.rating2)
    
    def test_keywordscore_creation(self):
        keywords = Keyword.objects.filter(recipe=self.recipe1)
        for keyword in keywords:
            score = KeywordScore.objects.get(keyword=keyword, user=self.u1)
            self.assertEqual(score.score, self.rating1)

    def test_recipescore_creation(self):
        score = RecipeScore.objects.get(recipe=self.recipe1, user=self.u1)
        self.assertEqual(score.score, self.rating1*10)
    
    def test_different_score_per_user(self):
        keywords = Keyword.objects.filter(recipe=self.recipe1)
        for keyword in keywords:
            score1 = KeywordScore.objects.get(keyword=keyword, user=self.u1)
            self.assertEqual(score1.score, self.rating1)
            score2 = KeywordScore.objects.get(keyword=keyword, user=self.u2)
            self.assertEqual(score2.score, self.rating2)

        score1 = RecipeScore.objects.get(recipe=self.recipe1, user=self.u1)
        self.assertEqual(score1.score, self.rating1*10)
        score2 = RecipeScore.objects.get(recipe=self.recipe1, user=self.u2)
        self.assertEqual(score2.score, self.rating2*10)