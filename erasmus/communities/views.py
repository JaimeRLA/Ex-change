# communities/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    City, University, Profile, Community, Membership, Event, RSVP, Post, Comment
)
from .serializers import (
    CitySerializer, UniversitySerializer, ProfileSerializer, CommunitySerializer,
    MembershipSerializer, EventSerializer, RSVPSerializer, PostSerializer, CommentSerializer
)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "created_by", None) == request.user


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filterset_fields = ["country"]
    search_fields = ["name","country"]


class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.select_related("city").all()
    serializer_class = UniversitySerializer
    filterset_fields = ["city__id"]
    search_fields = ["name"]


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all().order_by("-created_at")
    serializer_class = CommunitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filterset_fields = ["kind","city","university","is_private"]
    search_fields = ["name","description"]


def perform_create(self, serializer):
    serializer.save(created_by=self.request.user)


@action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
def join(self, request, pk=None):
    community = self.get_object()
    Membership.objects.get_or_create(user=request.user, community=community)
    return Response({"status":"joined"})


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    filterset_fields = ["user","community","role"]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filterset_fields = ["community"]
    search_fields = ["title","location"]


class RSVPViewSet(viewsets.ModelViewSet):
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    filterset_fields = ["event","user","status"]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("community","author").all()
    serializer_class = PostSerializer
    filterset_fields = ["community","author"]
    search_fields = ["content"]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filterset_fields = ["post","author"]