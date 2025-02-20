# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from .views import test_page

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('test/', test_page, name = 'test_page'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
