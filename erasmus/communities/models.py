from django.conf import settings
from django.db import models


class City(models.Model):
    name = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    def __str__(self): return f"{self.name}, {self.country}"


class University(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="universities")
    website = models.URLField(blank=True)
    def __str__(self): return self.name


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    home_university = models.CharField(max_length=200, blank=True)
    languages = models.CharField(max_length=200, blank=True) # "es,en,it"
    interests = models.TextField(blank=True)
    arrival_date = models.DateField(null=True, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    def __str__(self): return self.user.get_username()


class Community(models.Model):
    KIND_CHOICES = [
    ("CITY", "City"), ("UNIVERSITY", "University"), ("COURSE", "Course"),
    ]
    name = models.CharField(max_length=200)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default="UNIVERSITY")
    university = models.ForeignKey(University, null=True, blank=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    is_private = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("name", "kind", "university", "city")
        def __str__(self): return self.name


class Membership(models.Model):
    ROLE_CHOICES = [("MEMBER","Member"),("MOD","Moderator"),("OWNER","Owner")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="MEMBER")
    joined_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ("user","community")


class Event(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)


class RSVP(models.Model):
    GOING = "GOING"; MAYBE="MAYBE"; NO="NO"
    STATUS_CHOICES = [(GOING,"Going"),(MAYBE,"Maybe"),(NO,"No")]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="rsvps")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=GOING)
    class Meta:
        unique_together = ("event","user")


class Post(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)