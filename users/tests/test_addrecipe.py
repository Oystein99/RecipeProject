from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase
import tempfile
from users.forms import AddRecipeForm
class AddrecipeTest(TestCase):
    def setUp(self):
        self.image = tempfile.NamedTemporaryFile(suffix="jpg").name
        self.req_data = {
            'name': 'burger',
            'timetomake': '5',
            'image':self.image,
            'ingredients': '1 burgermeat',
            'recipe': 'Slap the burger on the pan and fry it',
            'difficulty': 'E'
        }
        self.missing_data = {
            'name': '',
            'timetomake': '5',
            'image':self.image,
            'ingredients': '1 burgermeat',
            'recipe': 'Slap the burger on the pan and fry it',
            'difficulty': 'E'
        }
    def test_get(self):
        response = self.client.get('/addrecipes')
        self.assertEqual(response.status_code, 301)
    def test_form(self):
        filled_form = AddRecipeForm(data=self.req_data)
        self.assertTrue(filled_form.is_valid())
    def test_wrong_form(self):
        filled_form = AddRecipeForm(data=self.missing_data)
        self.assertFalse(filled_form.is_valid())
        self.assertEqual(filled_form.errors['name'][0], "This field is required.")

    