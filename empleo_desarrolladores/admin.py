from django.contrib import admin
from .models import Company, Offer, UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

class CompanyAdmin(admin.ModelAdmin):
    pass
admin.site.register(Company, CompanyAdmin)

class OfferAdmin(admin.ModelAdmin):
    pass
admin.site.register(Offer, OfferAdmin)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

class UserProfileAdmin(UserAdmin):
    inlines=(UserProfileInline, )

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserProfileAdmin)
