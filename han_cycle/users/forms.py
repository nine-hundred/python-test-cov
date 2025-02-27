from django import forms

from .models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "nickname", "provider", "profile_image"]
