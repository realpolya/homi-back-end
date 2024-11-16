from django.contrib import admin
from django import forms
from .models import Property, Address
from .amenities import AMENITIES

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

admin.site.register(Property, PropertyAdmin)
admin.site.register(Address)