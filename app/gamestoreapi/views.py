from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.models import User
from gamestore import models
from rest_framework import status, viewsets
from rest_framework.response import Response
from gamestoreapi import serializers

"""
API endpoints that allows users to be viewed or edited.
"""
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.user.is_active = False
            instance.user.save()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

class GameViewSet(viewsets.ModelViewSet):
    queryset = models.Game.objects.all()
    serializer_class = serializers.GameSerializer

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = models.Purchase.objects.all()
    serializer_class = serializers.PurchaseSerializer

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = models.Score.objects.all()
    serializer_class = serializers.ScoreSerializer

class WishListViewSet(viewsets.ModelViewSet):
    queryset = models.WishList.objects.all()
    serializer_class = serializers.WishListSerializer

class GameStateViewSet(viewsets.ModelViewSet):
    queryset = models.GameState.objects.all()
    serializer_class = serializers.GameStateSerializer


