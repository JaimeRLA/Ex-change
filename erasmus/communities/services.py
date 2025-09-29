# communities/services.py
from django.db.models import Q
from .models import Profile, Community


def suggest_buddies(user, community_id):
    me = Profile.objects.get(user=user)
    qs = Profile.objects.exclude(user=user)
    if me.languages:
        langs = [l.strip() for l in me.languages.split(',')]
        for l in langs:
            qs = qs.filter(languages__icontains=l)
    if me.arrival_date and me.departure_date:
        qs = qs.filter(
        Q(arrival_date__lte=me.departure_date) & Q(departure_date__gte=me.arrival_date))
    # limita a miembros de la comunidad
    qs = qs.filter(user__membership__community_id=community_id).distinct()[:20]
    return qs