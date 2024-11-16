from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django import forms
from .models import Property, Photo, Address
from .amenities import AMENITIES

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 5

class AddressInline(admin.StackedInline):
    model = Address
    extra = 1
    max_num = 1

class PropertyAdminForm(forms.ModelForm):
    amenities = forms.MultipleChoiceField(
        choices=AMENITIES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Property
        fields = '__all__'

class PropertyAdmin(admin.ModelAdmin):
    form = PropertyAdminForm
    inlines = [PhotoInline, AddressInline]

admin.site.register(Property, PropertyAdmin)