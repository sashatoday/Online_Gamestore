
from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'games', views.GameViewSet)
router.register(r'purchases', views.PurchaseViewSet)
router.register(r'scores', views.ScoreViewSet)
router.register(r'wishlists', views.WishListViewSet)
router.register(r'gamestates', views.GameStateViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]