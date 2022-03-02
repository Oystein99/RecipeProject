from django.test import TestCase
from users.forms import RegistrationForm

class registerTest(TestCase):
    def setUp(self):
        self.pwd = 'c0mpl1c4t3dp4ssw0rd'
        self.reg_data = {
            'username':'unitTestUser',
            'first_name':'unit',
            'last_name':'test',
            'email':'unittest@outlook.com',
            'password1':self.pwd,
            'password2':self.pwd
        }
        self.reg_data_fail = {
            'username':  'unitTestUser2',
            'first_name':  'unit',
            'last_name':  'test',
            'email':  'unittest2@outlook.com',
            'password1':  self.pwd,
            'password2':  'wrong'
        }
    
    def test_signUp_success(self):
        response = self.client.post('/register/',self.reg_data,follow=True)
        self.assertRedirects(response,'/login/',status_code=302)

    def test_signUp_fail(self):
        response = self.client.post('/register/',self.reg_data_fail)
        self.assertTemplateUsed(response,'users/register.html')
        self.assertEqual(response.status_code,400)