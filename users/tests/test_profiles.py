from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
from users.models import FoodUser
from recipes.models import Recipe
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class User_profile_Test(StaticLiveServerTestCase):
    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        self.browser = webdriver.Firefox(firefox_options=options)
        
        self.u1_firstname = 'MyFirstName'
        self.u1_lastname = 'MyLastName'
        android = User.objects.create_user(username='Profile_android', password='verysecure123',first_name= self.u1_firstname,last_name = self.u1_lastname)
        self.u1_bio = 'why are we still here?'
        self.u1 = FoodUser.objects.create(user=android, biography=self.u1_bio)
        
        self.u2_firstname = 'YourFirstName'
        self.u2_lastname = 'YourLastName'
        android2 = User.objects.create_user(username='Profile_android2', password='verysecure123',first_name= self.u2_firstname,last_name = self.u2_lastname)
        self.u2_bio = "Don't worry about it"
        self.u2 = FoodUser.objects.create(user=android2, biography=self.u2_bio)
        
        self.browser.get(f'{self.live_server_url}/login')
        
        login_button = self.browser.find_element_by_tag_name('button')
        username  = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')
        
        username.send_keys('Profile_android')
        password.send_keys('verysecure123')
        login_button.click()
    
    def test_myprofile(self):
        self.browser.get(f'{self.live_server_url}/profile')
        self.browser.implicitly_wait(1)
        bio = self.browser.find_element_by_id('bio').text
        self.assertEqual(bio, self.u1_bio)

        name= self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(name,self.u1_firstname + ' ' + self.u1_lastname)
    
    def test_yourprofile(self):
        self.browser.get(f'{self.live_server_url}/users/Profile_android2')
        self.browser.implicitly_wait(1)
        
        bio = self.browser.find_element_by_id('bio').text
        self.assertEqual(bio, self.u2_bio)

        name= self.browser.find_element_by_tag_name('h1').text
        self.assertEqual(name,self.u2_firstname + ' ' + self.u2_lastname)
    
    def tearDown(self):
        self.browser.quit()
     
class Addrecipe_Test(StaticLiveServerTestCase):

    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        self.browser = webdriver.Firefox(firefox_options=options)
        self.u1_firstname = 'Robot'
        self.u1_lastname = 'Robotson'
        user_object = User.objects.create_user(username='Robotjohn', password='notarobot420',first_name= self.u1_firstname,last_name = self.u1_lastname)
        self.u1 = FoodUser.objects.create(user=user_object, biography="im alive")

    #Timeout function to wait before moving on    
    def timeout(self, time_to_sleep):
        time.sleep(time_to_sleep)

    def test_add_recipe(self):
        self.browser.get(f'{self.live_server_url}/login')
        #Find elements on page
        login_button = self.browser.find_element_by_tag_name('button')
        username  = self.browser.find_element_by_id('id_username')
        password = self.browser.find_element_by_id('id_password')

        username.send_keys('Robotjohn')
        password.send_keys('notarobot420')
        login_button.click()

        self.browser.get(f'{self.live_server_url}/profile')
        add_button = self.browser.find_element_by_class_name('addrecipes_button')
        add_button.click()
        
        #Find elements on page
        #Find elements on add_recipe page
        name = self.browser.find_element_by_id('id_name')
        timetomake = self.browser.find_element_by_id('id_timetomake')
        ingredients_name = self.browser.find_element_by_id('ingredient_0_name')
        ingredients_amount = self.browser.find_element_by_id('ingredient_0_amount')
        ingredients_measurement = self.browser.find_element_by_id('ingredient_0_measurement')
        recipe = self.browser.find_element_by_id('id_recipe')
        difficulty = self.browser.find_element_by_id('id_difficulty')
        submit_button = self.browser.find_element_by_id('submit_button')
        
        self.browser.implicitly_wait(2)

        name.send_keys('Pizza')
        timetomake.send_keys(20)
        ingredients_name.send_keys('Frozen pizza')
        ingredients_amount.send_keys('1')
        ingredients_measurement.send_keys('g')
        recipe.send_keys('Warm up the owen to 225 degrees celcius and shove that pizza in the oven. Wait around 20-22minutes for it to finish')
        difficulty.send_keys('E')
        submit_button.click()
        
        #Confirmation page
        confirm_button = self.browser.find_element_by_class_name('confirm')
        confirm_button.click()
        self.browser.implicitly_wait(1)

        #Find the created recipe
        recipe = Recipe.objects.get(user = self.u1)
        id = recipe.id

        #Find elements on /recipes to validate the input
        clickable_recipe = self.browser.find_element_by_id(id)
        self.browser.implicitly_wait(2)
        clickable_recipe.click()
        self.timeout(30)
        #Recipe page to validate the inputs in the recipe page
        recipe_name = self.browser.find_element_by_id('title')
        recipe_timetomake = self.browser.find_element_by_class_name('rightcol')
        recipe_ingredients = self.browser.find_element_by_class_name('ing')
        recipe_recipe = self.browser.find_element_by_class_name('recip')
        recipe_difficulty = self.browser.find_element_by_id('diff')
        
        self.assertTrue(recipe_name, 'pizza')
        self.assertTrue(recipe_timetomake, '20 minutes')
        self.assertTrue(recipe_ingredients, '1 g Frozen pizza')
        self.assertTrue(recipe_recipe,'Warm up the owen to 225 degrees celcius and shove that pizza in the oven. Wait around 20-22minutes for it to finish')
        self.assertTrue(recipe_difficulty, "E")
        
     
    def tearDown(self):
        self.browser.quit()









