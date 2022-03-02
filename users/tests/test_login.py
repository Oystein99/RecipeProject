from django.test import TestCase
from users.models import FoodUser
from django.shortcuts import get_object_or_404
from django.contrib import auth

class loginTest(TestCase):
    def setUp(self):
        self.pwd = 'c0mpl1c4t3dp4ssw0rd'
        self.testUser_data = {
            'username':'tester2',
            'first_name':'unit',
            'last_name':'test',
            'email':'unittest@outlook.com',
            'password1':self.pwd,
            'password2':self.pwd
        }
        self.login_cred = {
            'username':'tester2',
            'password':self.pwd,
        }
        self.invalid_login_cred = {
            'username':'not_realuser',
            'password':self.pwd,            
        }
        self.client.post('/register/',self.testUser_data,follow=True)
    
    def test_login_fail(self):
        response = self.client.post('/login/', self.invalid_login_cred)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response,'users/login.html')
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
        
    def test_login_success(self):
        response = self.client.post('/login/', self.login_cred)
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertRedirects(response,'/profile/',status_code=302)
        