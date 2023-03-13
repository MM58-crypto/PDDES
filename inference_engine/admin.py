from django.contrib import admin
from .models import GHQ12Response, GHQ12Question
# Register your models here.

admin.site.register(GHQ12Question)
admin.site.register(GHQ12Response)