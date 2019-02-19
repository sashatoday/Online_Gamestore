from django.shortcuts import render
from django.http import Http404, HttpRequest
from django.contrib.auth.models import User
from gamestore import models
from rest_framework import status, viewsets, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from gamestoreapi.permissions import IsOwnerOrAdminElseReadOnly
from gamestoreapi import serializers

"""
API endpoints that allows users to be viewed or edited.
"""
class UserViewSet(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = serializers.UserProfileSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('list', 'retrieve', 'destroy'):
            permission_classes = [IsOwnerOrAdminElseReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.user.delete()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

class GameViewSet(viewsets.ModelViewSet):
    queryset = models.Game.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = serializers.GameSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('list', 'retrieve', 'update', 'partial_update', 'destroy'):
            permission_classes = [IsOwnerOrAdminElseReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
    
class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = models.Purchase.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = serializers.PurchaseSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('list', 'retrieve'):
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = models.Score.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = serializers.ScoreSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('list', 'retrieve'):
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class WishListViewSet(viewsets.ModelViewSet):
    queryset = models.WishList.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = serializers.WishListSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('list', 'retrieve'):
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

class GameStateViewSet(viewsets.ModelViewSet):
    queryset = models.GameState.objects.all()
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    serializer_class = serializers.GameStateSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ('list', 'retrieve'):
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


