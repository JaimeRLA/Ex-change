from rest_framework import serializers
from .models import City, University, Profile, Community, Membership, Event, RSVP, Post, Comment


class CitySerializer(serializers.ModelSerializer):
    class Meta: model = City; fields = "__all__"


class UniversitySerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    city_id = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), source="city", write_only=True)
    class Meta: model = University; fields = ["id","name","website","city","city_id"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta: model = Profile; fields = ["id","home_university","languages","interests","arrival_date","departure_date"]


class CommunitySerializer(serializers.ModelSerializer):
    class Meta: model = Community; fields = ["id","name","kind","university","city","description","is_private","created_by","created_at"]
    read_only_fields = ["created_by","created_at"]


class MembershipSerializer(serializers.ModelSerializer):
    class Meta: model = Membership; fields = ["id","user","community","role","joined_at"]
    read_only_fields = ["joined_at"]


class EventSerializer(serializers.ModelSerializer):
    going_count = serializers.IntegerField(source="rsvps.count", read_only=True)
    class Meta: model = Event; fields = ["id","community","title","description","starts_at","ends_at","location","going_count"]


class RSVPSerializer(serializers.ModelSerializer):
    class Meta: model = RSVP; fields = ["id","event","user","status"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta: model = Comment; fields = ["id","post","author","content","created_at"]
    read_only_fields = ["created_at"]


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    class Meta: model = Post; fields = ["id","community","author","content","created_at","comments"]
    read_only_fields = ["created_at"]