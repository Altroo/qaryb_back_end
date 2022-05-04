from django.urls import path
from .views import RatingsView

app_name = 'ratings'

urlpatterns = [
    # GET : Return all ratings details for a user.
    # POST : Add a rating.
    path('', RatingsView.as_view()),
]