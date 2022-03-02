from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from users.models import FoodUser
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from recipes.models import Recipe

class Recipe_rating_Test(StaticLiveServerTestCase):
    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        self.browser = webdriver.Firefox(firefox_options=options)
        
        self.u1_firstname = 'MyFirstName'
        self.u1_lastname = 'MyLastName'
        android = User.objects.create_user(username='Profile_android3', password='verysecure123',first_name= self.u1_firstname,last_name = self.u1_lastname)
        self.u1 = FoodUser.objects.create(user=android)
        self.r1 = Recipe.objects.create(name='rate1', timetomake=30, ingredients='test g', recipe='very_different', kcal=2000, user=self.u1)
        self.r2 = Recipe.objects.create(name='rate2', timetomake=30, ingredients='test g', recipe='very_different2', kcal=2000, user=self.u1)
        
        self.browser.get(f'{self.live_server_url}/login')
        
        login_button = self.browser.find_element_by_tag_name('button')
        username  = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')

        username.send_keys('Profile_android3')
        password.send_keys('verysecure123')
        login_button.click()
    

    
    def test_rating_successful(self):
        self.browser.get(f'{self.live_server_url}/recipes')
        self.browser.implicitly_wait(1)
        recipe_r1 = self.browser.find_element_by_id(self.r1.id)
        recipe_r1.click()

        rate_button=self.browser.find_element_by_id('rate_button')
        rate_button.click()

        third_star = self.browser.find_element_by_id('third_star')
        third_star.click()
        self.browser.implicitly_wait(1)

        message = self.browser.find_element_by_id('msg-area').text
        self.assertEqual(message,'Successfully rated with 3')
        
        recipe =Recipe.objects.get(id=self.r1.id)
        self.assertEqual(recipe.three_star,1)
        self.assertEqual(recipe.num_ratings,1)
        self.assertEqual(recipe.rating,3)
    
    def test_alreadyRated(self):
        self.browser.get(f'{self.live_server_url}/recipes')
        self.browser.implicitly_wait(1)
        recipe_r2 = self.browser.find_element_by_id(self.r2.id)
        recipe_r2.click()

        rate_button=self.browser.find_element_by_id('rate_button')
        rate_button.click()

        third_star = self.browser.find_element_by_id('third_star')
        third_star.click()
        self.browser.implicitly_wait(1)


        rate_button=self.browser.find_element_by_id('rate_button')
        rate_button.click()

        third_star = self.browser.find_element_by_id('third_star')
        third_star.click()
        self.browser.implicitly_wait(1)

        message = self.browser.find_element_by_id('msg-area').text
        self.assertEqual(message,"You've already rated this recipe!")
    
    def tearDown(self):
        self.browser.quit()
     

