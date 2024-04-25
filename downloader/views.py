import os
from django.shortcuts import render
from pytube import YouTube

def youtube(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        download_path = r'C:\Users\Lall\Downloads'
        audio_only = request.POST.get('audio_only') == 'on'  # Check if audio_only checkbox is checked
        try:
            video = YouTube(link)
            if audio_only:
                stream = video.streams.filter(only_audio=True).first()  # Get audio stream
            else:
                stream = video.streams.get_highest_resolution()  # Get highest resolution video stream
            if stream:
                stream.download(output_path=download_path)
                return render(request, 'video_downloaded.html', {'audio_only': audio_only})
        except Exception:
            error_message = f"Invalid URL"
            return render(request, 'youtube.html', {'error_message': error_message})
    return render(request, 'youtube.html')
