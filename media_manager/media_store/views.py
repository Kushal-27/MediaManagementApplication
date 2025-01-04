from django.shortcuts import render, redirect, get_object_or_404
from .models import Media
from .forms import MediaForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import MediaForm
from .models import Media

def media_management(request):
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES)
        if form.is_valid():
            for media_file in request.FILES.getlist('files'):
                media = Media(file=media_file, name=media_file.name, size=media_file.size, file_type=media_file.content_type)
                media.save()
            messages.success(request, "Files uploaded successfully!")
            return redirect('media_management')
    else:
        form = MediaForm()

    media_files = Media.objects.all()
    paginator = Paginator(media_files, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'form': form, 'page_obj': page_obj})

def media_delete(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    media.delete()
    messages.success(request, 'File deleted successfully!')
    return redirect('media_management')
