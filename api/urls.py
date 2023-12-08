from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/rating/', GetChatGPTSuggestions.as_view(), name='submit_rating'),
    path('api/review/', GetChatGPTReview.as_view(), name='generate_review'),

    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

]
