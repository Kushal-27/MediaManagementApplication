from django import forms
from django.core.exceptions import ValidationError

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True  

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())  
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            if len(data) > 10:
                raise ValidationError("You can only upload up to 10 files.")
            
            result = [single_file_clean(d, initial) for d in data]
            for file in result:
                self.validate_file_size(file)
                self.validate_file_type(file)
        else:
            result = single_file_clean(data, initial)
            self.validate_file_size(result)
            self.validate_file_type(result)

        return result

    def validate_file_size(self, file):
        max_size = 5 * 1024 * 1024  # 5 MB
        min_size = 100 * 1024       # 100 KB

        if file.size < min_size:
            raise ValidationError(f"The file {file.name} does not meet the minimum size requirement of 100KB.")
        if file.size > max_size:
            raise ValidationError(f"The file {file.name} exceeds the size limit of 5MB.")

    def validate_file_type(self, file):
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf']
        extension = file.name.split('.')[-1].lower()
        if f'.{extension}' not in allowed_extensions:
            raise ValidationError(f"The file {file.name} has an unsupported file type. Allowed types: {', '.join(allowed_extensions)}.")


class MediaForm(forms.Form):
    files = MultipleFileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), required=True)
