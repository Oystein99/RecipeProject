from django.test import TestCase
from django.contrib.auth.models import User
from users.models import FoodUser
from recipes.models import Recipe, Recommended
from datetime import date, timedelta

class UserViewTest(TestCase):
    def setUp(self):
        android = User.objects.create_user(username='Profile_android_view', password='verysecure123')
        self.u1 = FoodUser.objects.create(user=android, biography='What is life?')
        self.recipe1 = Recipe.objects.create(name='test1', timetomake=30, ingredients='', recipe='food and food', kcal=2000, user=self.u1)


    def test_login_page(self):
        response = self.client.get(f'/login/')
        self.assertTemplateUsed(response, 'users/login.html')
        
    def test_register_page(self):
        response = self.client.get(f'/register/')
        self.assertTemplateUsed(response, 'users/register.html')
    
    def test_myprofile_page(self):
    
        self.client.login(username='Profile_android_view',password ='verysecure123')
        response = self.client.get('/profile/')
        self.assertTemplateUsed(response, 'users/profile.html')

        self.client.logout()

    def test_recommendation(self):
        self.client.login(username='Profile_android_view',password ='verysecure123')
        date1 = date.today()-timedelta(days=1)
        Recommended.objects.get(user=self.u1).delete()
        Recommended.objects.create(user=self.u1, date=date1)
        response = self.client.get('/profile/')

        rec = Recommended.objects.get(user=self.u1)
        self.assertGreater(rec.date, date1)
        self.assertEqual(rec.date, date.today())