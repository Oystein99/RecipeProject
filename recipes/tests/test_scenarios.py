from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from users.models import FoodUser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from recipes.models import Recipe
import time

class VisitTest(StaticLiveServerTestCase):
    
    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        self.browser = webdriver.Firefox(firefox_options=options)

        android = User.objects.create(username='Legion', password='verysecure123')
        self.u1 = FoodUser.objects.create(user=android, biography='Does this unit have a soul?')
        self.r1 = Recipe.objects.create(name='r1', timetomake=30, difficulty='M', ingredients="some ingredients", recipe='long recipe', kcal=2000, user=self.u1)

    def tearDown(self):
        self.browser.quit()
    
    def test_visit_and_read(self):
        self.browser.get(f'{self.live_server_url}/recipes')
        self.browser.implicitly_wait(1)
        recipe_r1 = self.browser.find_element_by_id(self.r1.id)
        recipe_r1.click()
        name = self.browser.find_element_by_id('title').text
        self.assertEqual(name, self.r1.name)
        
