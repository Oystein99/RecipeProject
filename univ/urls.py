#Edits
# feb19, added '' path as static wasnt working, Preben

"""univ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static      # Include statics
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from users import views as user_views
from recipes import views as recipe_views

#from django.conf.urls.static import RECIPES_URLS


urlpatterns = [
    path('', recipe_views.index, name='index'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('recipes/', include('recipes.urls')),
    path('profile/', user_views.profile, name='profile'),
    path('logout/', user_views.logout_view, name='logout'),
    path('login/',user_views.login_view, name='login'),
    path('addrecipes/', user_views.add_recipes_view, name='addrecipes'), #Path to add_recipe view which will be a "path" to html page
    path('logout/',user_views.logout_view, name='logout'),
    path('users/', include('users.urls')),
    path('rate/',recipe_views.rate_view,name='rate'),
    path('like/',recipe_views.like_view, name='like'),
    path('confirmation/', user_views.confirmation_page_view, name='confirmation')
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)