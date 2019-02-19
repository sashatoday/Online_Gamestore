from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from gamestore import models
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_active')
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }

class PurchaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Purchase
        fields = ('__all__')

class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Score
        fields = ('__all__')

class WishListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.WishList
        fields = ('__all__')

class GameStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.GameState
        fields = ('__all__')

class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Game
        fields = ('__all__')

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.UserProfile
        fields = ('id', 'url', 'user', 'birth_date', 'gender', 'country', 'city', 'address', 'bio', 'photo_url', 'role', 'developer', 'buyer')
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        developer_data = validated_data.pop('developer')
        buyer_data = validated_data.pop('buyer')
        user = User.objects.create(**user_data)
        user_profile = models.UserProfile.objects.create(user=user, **validated_data)
        user_profile.developer.set(developer_data)
        user_profile.buyer.set(buyer_data)
        user_profile.save()

        return user_profile

    def update(self, instance, validated_data):
        user = list(validated_data.get('user', instance.user).items())
        instance.user.username = user[0][1]
        instance.user.first_name = user[1][1]
        instance.user.last_name = user[2][1]
        instance.user.email = user[3][1]
        instance.user.is_active = user[4][1]
        instance.user.save()
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.address = validated_data.get('address', instance.address)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.photo_url = validated_data.get('photo_url', instance.photo_url)
        instance.role = validated_data.get('role', instance.role)
        instance.developer.set(validated_data.get('developer', instance.developer))
        instance.buyer.set(validated_data.get('buyer', instance.buyer))
        instance.save()
        
        return instance
