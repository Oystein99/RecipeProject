from django.apps import AppConfig


class FoodConfig(AppConfig):
    name = 'recipes'
    def ready(self):
        import nltk
        nltk.download('stopwords')
        from .models import Word
        if not Word.objects.exists(): # Finds every word in every recipe as long as they have never been found before
            Word().get_all_words()