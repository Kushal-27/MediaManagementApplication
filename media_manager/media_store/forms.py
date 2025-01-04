from django import forms
from .models import Media
from django.core.exceptions import ValidationError

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data['file']
        valid_extensions = ['.mp3', '.mp4', '.jpeg', '.png', '.gif', '.jpg']
        max_size = 10 * 1024 * 1024 
        min_size = 100 * 1024  

        # Validate file extension
        if not any(file.name.endswith(ext) for ext in valid_extensions):
            raise ValidationError('Invalid file extension.')

        # Validate file size
        if file.size < min_size or file.size > max_size:
            raise ValidationError(f"File size must be between {min_size} and {max_size} bytes.")

        return file
