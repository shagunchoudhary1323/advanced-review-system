from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductReviewSerializer
import openai
from django.conf import settings

class GetChatGPTSuggestions(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            star_rating = serializer.validated_data['star_rating']
            product_name = serializer.validated_data['product_name']
            suggestions = self.get_chatgpt_suggestions(star_rating,product_name)

            if 'error' in suggestions:
                return Response({'error': suggestions}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'suggestions': suggestions})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_chatgpt_suggestions(self, star_rating,product_name):
        try:
            openai.api_key = settings.OPEN_API_KEY
            prompt = f"User rated the product{product_name} {star_rating} stars. Generate 5 to 6 words for {star_rating} of {product_name}. Ignore description."

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
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductReviewSerializer(data=request.data)
        if serializer.is_valid():
            star_rating = serializer.validated_data['star_rating']
            user_word = serializer.validated_data['user_word']
            product_name = serializer.validated_data['product_name']
            review = self.get_chatgpt_review(star_rating, user_word,product_name)

            if 'error' in review:
                return Response({'error': review}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'review': review})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_chatgpt_review(self, star_rating, user_word, product_name):
        try:
            openai.api_key = settings.OPEN_API_KEY
            prompt = f"User selected {user_word} as best describing word for {product_name} and rated {star_rating} stars for review.Only provide a detailed 80-100 words review based on {product_name} in easy language. Ignore description."

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for a product review system."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )
            review = response['choices'][0]['message']['content']
            return review
        except Exception as e:
            return str(e)
