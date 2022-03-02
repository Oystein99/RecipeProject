from recipes.models import Recently_recommended
from users.models import FoodUser
from django.test import TestCase
from django.contrib.auth.models import User
from recipes.models import Recipe
from django.utils import timezone
from datetime import timedelta

class Recently_recommended_test(TestCase):
    def setUp(self):
        android = User.objects.create(username='RR_android', password='verysecure123')
        self.u1 = FoodUser.objects.create(user=android, biography='Does this unit have a soul?')
        self.r1 = Recipe.objects.create(name='RR_recipe', timetomake=30, difficulty='M', ingredients="some ingredients", recipe='long recipe', kcal=2000, user=self.u1)
        self.RR = Recently_recommended.objects.create(user=self.u1,recipe=self.r1)
        self.RR2 = Recently_recommended.objects.create(user=self.u1,recipe=self.r1,expiry_date=timezone.now().date()-timedelta(days=7))
        self.RR3 = Recently_recommended.objects.create(user=self.u1,recipe=self.r1,expiry_date=timezone.now().date()+timedelta(days=2))

    def test_remove_expired(self):
        self.objects = Recently_recommended.objects.all()
        self.assertEqual(len(self.objects),3)
        self.RR.remove_expired()
        self.objects = Recently_recommended.objects.all()
        self.assertEqual(len(self.objects),2)