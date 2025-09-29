from django.contrib import admin
from .models import City, University, Community
admin.site.register([City, University, Community])
