from django import forms
from .models import TravelInfo

class TravelInfoForm(forms.ModelForm):
    class Meta:
        model = TravelInfo
        fields = ['destination', 'travel_start_date', 'travel_end_date', 'favorite_scenic_type', 'travel_companion', 'budget']
