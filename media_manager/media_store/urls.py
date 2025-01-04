from django.urls import path
from .views import media_management, media_delete

urlpatterns = [
    path('', media_management, name='media_management'),
    path('delete/<int:media_id>/', media_delete, name='media_delete'),
]
