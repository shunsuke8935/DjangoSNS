from django.contrib import admin
from .models import SnsModel, AppUsers, Follow, Coment

# Register your models here.
admin.site.register(SnsModel)
admin.site.register(Follow)
admin.site.register(AppUsers)
admin.site.register(Coment)
