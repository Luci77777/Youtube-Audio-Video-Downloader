import os
from django.http import FileResponse
from django.shortcuts import render
from django.conf import settings
from pytube import YouTube

def youtube(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        audio_only = request.POST.get('audio_only') == 'on'

        try:
            video = YouTube(link)

            if audio_only:
                stream = video.streams.filter(only_audio=True).first()
            else:
                stream = video.streams.get_highest_resolution()

            if not stream:
                raise Exception("Stream not found")

            # Use MEDIA_ROOT or a temp folder
            download_path = os.path.join(settings.MEDIA_ROOT, 'downloads')
            os.makedirs(download_path, exist_ok=True)

            file_path = stream.download(output_path=download_path)

            return FileResponse(
                open(file_path, 'rb'),
                as_attachment=True,
                filename=os.path.basename(file_path)
            )

        except Exception:
            return render(request, 'youtube.html', {
                'error_message': 'Invalid URL or download failed'
            })

    return render(request, 'youtube.html')
