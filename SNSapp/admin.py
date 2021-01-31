from django.contrib import admin
from .models import SnsModel, AppUsers, Follow 

# Register your models here.
admin.site.register(SnsModel)
admin.site.register(Follow)
admin.site.register(AppUsers)
