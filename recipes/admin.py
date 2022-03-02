from django.contrib import admin
from .models import Recipe, Ratings, Likes, Ingredient, Document, Keyword, Word, RecipeScore, KeywordScore, Recommended, Recently_recommended

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Ratings)
admin.site.register(Likes)
admin.site.register(Ingredient)
admin.site.register(Document)
admin.site.register(Keyword)
admin.site.register(Word)
admin.site.register(Recently_recommended)
admin.site.register(RecipeScore)
admin.site.register(KeywordScore)
admin.site.register(Recommended)