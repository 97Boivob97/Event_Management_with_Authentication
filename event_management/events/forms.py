from django import forms
from .models import UserProfile,Event,Booking

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"