import os
from django.db import models

CATEGORY_CHOICES = [
    ('audio', 'Audio'),
    ('video', 'Video'),
    ('image', 'Image'),
]

class Media(models.Model):
    file = models.FileField(upload_to='media_files/')
    name = models.CharField(max_length=255, blank=True)
    size = models.PositiveIntegerField(blank=True, null=False) 
    file_type = models.CharField(max_length=50, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True)
    
    def __str__(self):
        return self.name

    def get_extension(self):
        return os.path.splitext(self.file.name)[1].lower()

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = os.path.splitext(self.file.name)[0] 
        
        extension = self.get_extension()
        if extension in ['.mp3', '.wav']:
            self.category = 'audio'
        elif extension in ['.mp4', '.avi', '.mkv']:
            self.category = 'video'
        elif extension in ['.jpeg', '.png', '.gif', '.jpg']:
            self.category = 'image'
        else:
            self.category = 'other'  
        
        if not self.size:
            self.size = self.file.size  
        
        if not self.file_type:
            self.file_type = extension[1:]  
        
        super().save(*args, **kwargs)
