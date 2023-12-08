from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import ProductReview

class ProductReviewSerializer(serializers.ModelSerializer):
    user_word = serializers.CharField(max_length=200, required=False)

    class Meta:
        model = ProductReview
        fields = [ 'star_rating','user_word']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

