from django.urls import path
from budget.views import *

urlpatterns = [
    path("", budget, name="budget"),
]
