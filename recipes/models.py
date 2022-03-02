from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import FoodUser
from datetime import timedelta
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize  
from string import punctuation
from math import log
from fractions import Fraction
from django.utils import timezone
from random import choice
# Create your models here.
class Recipe(models.Model):
    
    name = models.CharField(max_length=100)
    timetomake = models.IntegerField()  # How long it takes to make the meal
    image = models.ImageField(upload_to='images/', default='default.jpg', null=True)
    ingredients = models.CharField(max_length=600, default="none") #changed max_length to 600
    recipe = models.TextField(max_length=2000, unique=True)
    
    # Rating attributes
    one_star = models.IntegerField(default=0)    # Number of 1-star ratings 
    two_star = models.IntegerField(default=0)    # Number of 2-star ratings
    three_star = models.IntegerField(default=0)  # Number of 3-star ratings
    four_star = models.IntegerField(default=0)   # Number of 4-star ratings
    five_star = models.IntegerField(default=0)   # Number of 5-star ratings

    num_ratings = models.IntegerField(default=0)
    rating = models.IntegerField(default=0) # Rating
    like = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)
    
    public = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.name}'

    # Calculate rating using weighted average
    @staticmethod
    def calculate_rating(meal,sum_ratings):
        if sum_ratings == 0:
            return 0
        
        return round((1 *meal.one_star + 2*meal.two_star + 3*meal.three_star + 4*meal.four_star + 5*meal.five_star) / sum_ratings)

    @staticmethod   
    def sum_rating(meal):
        return (meal.one_star + meal.two_star + meal.three_star + meal.four_star + meal.five_star)

        
    class Difficulty(models.TextChoices):
        """The possible difficulties to choose from when making a recipe"""
        NOT = 'N', _('Not provided')
        EASY = 'E', _('Easy')
        MEDIUM = 'M', _('Medium')
        HARD = 'H', _('Hard')

    difficulty = models.CharField(max_length=10, choices=Difficulty.choices, default=Difficulty.NOT)
    kcal = models.IntegerField(null=True)
    user = models.ForeignKey(FoodUser, on_delete=models.CASCADE, null=True) #User that created the recipe

    @staticmethod
    def parse_time(time2make):
        """Parses the timetomake from minutes to hours and minutes"""
        time2make = str(timedelta(minutes=time2make))
        time = time2make.split(':')
        minute = 'minutes'
        if time[1] == '01':
            minute = 'minute'

        time2make = f'{time[1]} {minute}'
        if time[0] != '0':
            if time[0] == '1':
                time2make = f'{time[0]} hour {time[1]} {minute}'
            else:
                time2make = f'{time[0]} hours {time[1]} {minute}'
        
        return time2make


    @staticmethod
    def parse_recipe(recipe):
        recipe = recipe.split('\n')
        
        return recipe

    @staticmethod
    def parse_difficulty(meal):
        if meal.difficulty == 'E':
            meal.difficulty = 'Easy'
        elif meal.difficulty == 'M':
            meal.difficulty = 'Medium'
        elif meal.difficulty == 'H': 
            meal.difficulty = 'Hard'
        else:
            meal.difficulty = ''

        return meal.difficulty

# Finds tags for the recipe after the recipe is made
@receiver(post_save, sender=Recipe)
def get_tags(sender, instance, created, **kwargs):
    if created:
        Word.get_new_words(instance)
    # else: # if edited
    #     Word.objects.filter(recipe=instance).delete()
    #     Keyword.objects.filter(recipe=instance).delete()
    #     newWords = Word.get_new_words(instance)

class Keyword(models.Model):
    word = models.CharField(max_length=50, unique=True)
    recipe = models.ManyToManyField(Recipe)

    def __str__(self):
        return f'{self.word}'

    @staticmethod
    def calculate_tf():
        """ Calculates the term frequency(tf) of each word.
            tf is the number of times a word appears in a document 
            divded by the total number of words in the document.
        """
        uncalculatedWords = Word.objects.filter(termFrequency=0)
        for word in uncalculatedWords:
            numWords = word.document.numWords
            word.termFrequency = word.occurence / float(numWords)
            word.save()

    @staticmethod
    def calculate_idf(newWords):
        """ Calculates the inverse data frequency(idf) for each word.
            idf is the log of the number of documents 
            divided by the number of documents that contain the word.
        """
        numDocuments = Document.objects.all().count()
        for newWord in newWords:
            words = Word.objects.filter(word=newWord)
            for word in words:
                word.docFrequency += 1
                word.save()
        
        idfDict = {}        
        for word in newWords:
            idfDict[word.word] = log(numDocuments / word.docFrequency)

        return idfDict

    def calculate_tfidf(self, document):
        newWords = Word.objects.filter(document=document)
        self.calculate_tf()
        idfDict = self.calculate_idf(newWords)
        tfidf = {}
        for word in newWords:
            tfidf[(word.word, word.document)] = word.termFrequency * idfDict[word.word]
        
        return tfidf

    def add_keywords(self, document):
        """ After tidif scores are calculated, takes the 10 most important word for each recipe
            and adds them as keywords"""
        tfidf = self.calculate_tfidf(document)
        tfidf = dict(sorted(tfidf.items(), key=lambda item: item[1], reverse=True)) # sorts the dict by score
        
        for (word, doc), score in tfidf.items():
            document = Document.objects.get(recipe=doc.recipe)
            if document.numKeywords < 10: # Finds the top 10 most important words
                tag, created = Keyword.objects.get_or_create(word=word)
                document.numKeywords += 1 
                tag.recipe.add(doc.recipe)
                document.save()


class Document(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, unique=True)
    numWords = models.IntegerField()
    numKeywords = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.numWords} words in {self.recipe}'
    
    
class Word(models.Model):
    """Stores all the words in all the recipes for later converting to keywords"""
    word = models.CharField(max_length=50)
    occurence = models.IntegerField() 
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    termFrequency = models.FloatField(default=0)
    docFrequency = models.FloatField(default=1)

    def __str__(self):
        return f'{self.word}'

    @staticmethod
    def get_new_words(recipe):
        measurements = ['ca', 'g', 'ss', 'ts', 'dl', 'cup', 'cups', 'ounces', 'ml', 'l', 'teaspoons', 'tablespoon', 'teaspoon', 'tablespoons', 'pinch', 'minutes']
        words = []
        words.extend(recipe.name.lower().split())
        words.extend(recipe.recipe.lower().split())
        ingredients = Ingredient.objects.filter(recipe=recipe)
        for ingredient in ingredients:
            words.extend(ingredient.ingredient.lower())
            
        # words.extend(recipe.ingredients.lower().split())

        # Removes punctuations from words
        words = [word.translate(str.maketrans('', '', punctuation)) for word in words]

        # Removes all numbers, special characters, stopwords and measurements from the words list
        words = [item for item in words if item.isalpha() and 
                not item in stopwords.words('english') and 
                not item in measurements]
        
        uniqueWords = set(words) # Finds the unique word in the list
        numOfWords = dict.fromkeys(uniqueWords, 0)
        for word in words:
            numOfWords[word] +=1
        
        numWords = len(words)
        doc = Document.objects.create(recipe=recipe, numWords=numWords)
        
        uniqueWords = list(uniqueWords)
        for word in uniqueWords:
            Word.objects.create(word=word, occurence=numOfWords[word], document=doc)

        Keyword().add_keywords(doc)
    
    def get_all_words(self):
        recipes = Recipe.objects.all()
        for recipe in recipes:
            self.get_new_words(recipe)


class Ingredient(models.Model):
    ingredient = models.CharField(max_length=100)
    amount = models.FloatField(blank=True, null=True)

    class Measurement(models.TextChoices):
        """The possible measurements to choose from when making a adding an ingredient"""
        PIECE = 'P', _('')
        GRAM = 'G', _('g')
        LITER = 'L', _('L')
        KILO = 'KG', _('kg')
        DECI = 'DL', _('dL')
        MILI = 'ML', _('mL')
        TABLE = 'TaS', _('tablespoons')
        TEA = 'TeS', _('teaspoons')
        CUP = 'C', _('cups')
        BOAT = 'B', _('boats')
        OUNCE = 'O', _('ounces')
        SLICE = 'S', _('slices')
        PINCH = 'PCH', _('pinch')
        POUND = 'PD', _('pounds')

    measurement = models.CharField(max_length=10, choices=Measurement.choices, default=Measurement.PIECE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        if self.amount is not None:
            amount = self.parse_amount() 
        else:
            amount = ''

        measure = self.get_measurement_display()
        if self.measurement != 'P' and self.amount <= 1:
            measure = self.parse_measurement(measure)
        
        return f'{amount} {measure} {self.ingredient}'

    def parse_amount(self):
        """Displays the amount as a proper fraction"""
        f = Fraction(self.amount)
        if f.numerator > 100 or f.denominator > 100:
            return self.amount # if the fraction is too large, the float is used instead
        
        if f.numerator % f.denominator != 0:
            if f.numerator // f.denominator > 0:
                f = ('%d %d/%d' % (f.numerator // f.denominator, f.numerator % f.denominator, f.denominator))
            else:
                f = ('%d/%d' % (f.numerator % f.denominator, f.denominator))
        
        return f

    def parse_measurement(self, measurement):
        """Removes the s at the back of the measurement if the amount is 1 or lower"""
        if measurement[-1] == 's':
            measurement = measurement[:-1]
        
        return measurement

class Ratings(models.Model):
    user = models.ForeignKey(FoodUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    class Meta():
        constraints =[
            models.UniqueConstraint(fields=['user','recipe'],name='unique_rating')
        ]

class Likes(models.Model): 
    user = models.ForeignKey(FoodUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    class Meta():
        constraints = [
            models.UniqueConstraint(fields=['user','recipe'], name='unique_like')
        ]

class KeywordScore(models.Model):
    """Keeps track of the importance of each keyword for each user"""
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    user = models.ForeignKey(FoodUser, on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    
    def __str__(self):
        return f'{self.keyword} - {self.user}, {self.score}'

    @staticmethod
    def calculate_score(user, recipe, rating):
        keywords = Keyword.objects.filter(recipe=recipe)
        for keyword in keywords:
            scored = KeywordScore.objects.get(keyword=keyword, user=user)
            if scored.score == 0:
                scored.score = rating
            else:
                scored.score = (scored.score + rating) / 2

            scored.save()

class RecipeScore(models.Model):
    """Keeps track of the importance of each recipe for each user"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(FoodUser, on_delete=models.CASCADE)
    score = models.FloatField(default=0)

    def __str__(self):
        return f'{self.recipe} - {self.user}, {self.score}'

    @staticmethod
    def calculate_score(recipe, user):
        keywords = Keyword.objects.filter(recipe=recipe)
        recipeScore = RecipeScore.objects.get(recipe=recipe, user=user)
        for keyword in keywords:
            keyScore = KeywordScore.objects.get(keyword=keyword, user=user)
            recipeScore.score += keyScore.score
        
        recipeScore.save()


@receiver(post_save, sender=FoodUser)
def create_score(sender, instance, created, **kwargs):
    if created:
        keywords = Keyword.objects.all()
        for keyword in keywords:
            KeywordScore.objects.create(user=instance, keyword=keyword)
        recipes = Recipe.objects.all()
        for recipe in recipes:
            RecipeScore.objects.create(recipe=recipe, user=instance)
        Recommended.objects.create(user=instance)

@receiver(post_save, sender=Ratings)
def calculate_score(sender, instance, created, **kwargs):
    KeywordScore.calculate_score(instance.user, instance.recipe, instance.rating)
    RecipeScore.calculate_score(recipe=instance.recipe, user=instance.user)
    
@receiver(post_save, sender=Keyword)
def add_new_keyword_scores(sender, instance, created, **kwargs):
    if created:
        users = FoodUser.objects.all()
        for user in users:
            KeywordScore.objects.create(keyword=instance, user=user)

@receiver(post_save, sender=Recipe)
def add_new_recipe_scores(sender, instance, created, **kwargs):
    if created:
        users = FoodUser.objects.all()
        for user in users:
            RecipeScore.objects.create(recipe=instance, user=user)

# Object of recently recommended recipe for a user
class Recently_recommended(models.Model):
    user = models.ForeignKey(FoodUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    # Expires after 3 days so recipe can be recommended again
    expiry_date = models.DateField(default=timezone.now().date() + timedelta(days=3)) 
    
    # Removes all expired objects
    @staticmethod
    def remove_expired():
        expired = Recently_recommended.objects.filter(expiry_date__lt=timezone.now().date())
        for entry in expired:
            entry.delete()

class Recommended(models.Model):
    user = models.OneToOneField(FoodUser, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now=True)   # Last day it was recommended

    @staticmethod
    def recommend_recipe(user):
        Recently_recommended.remove_expired()
        recipe_scores = RecipeScore.objects.filter(user=user)
        scores = []
        for score in recipe_scores:
            scores.append(score.score)

        scores.sort(reverse=True)
        for score in scores:
            recipes = RecipeScore.objects.filter(user=user, score=score)
            recipe = choice(recipes)
            
            recent, created = Recently_recommended.objects.get_or_create(recipe=recipe.recipe, user=user)
            if created:
                return recipe.recipe