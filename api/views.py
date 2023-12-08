from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductReviewSerializer
import openai
from django.conf import settings

class GetChatGPTSuggestions(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            rating = serializer.validated_data['star_rating']
            suggestions = self.get_chatgpt_suggestions(rating)

            if 'error' in suggestions:
                return Response({'error': suggestions}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'suggestions': suggestions})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_chatgpt_suggestions(self, star_rating):
        try:
            openai.api_key = settings.OPEN_API_KEY
            prompt = f"User rated the product {star_rating} stars. Generate 5 to 6 words for {star_rating}. Ignore description."

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for the product review system."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=60
            )

            suggestions = response['choices'][0]['message']['content']
            return suggestions
        except Exception as e:
            return str(e)


class GetChatGPTReview(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            star_rating = serializer.validated_data['star_rating']
            user_word = serializer.validated_data['user_word']
            review = self.get_chatgpt_review(star_rating, user_word)

            if 'error' in review:
                return Response({'error': review}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'review': review})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_chatgpt_review(self, star_rating, user_word):
        try:
            openai.api_key = settings.OPEN_API_KEY
            prompt = f"User selected the word {user_word} and {star_rating} stars to review a product. Only provide a detailed 80-100 words review in easy language. Ignore description."

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for the product review system."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )
            review = response['choices'][0]['message']['content']
            return review
        except Exception as e:
            return str(e)
