from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class UserSettingsForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    current_password = forms.CharField(widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'profile_image', 'bio']
        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and new_password != confirm_password:
            raise ValidationError("New passwords don't match")
        return cleaned_data