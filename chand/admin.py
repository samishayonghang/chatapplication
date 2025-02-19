from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from.models import Codeform,CustomUser

admin.site.register(Codeform)
admin.site.register(CustomUser)