from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, FileResponse, Http404
from django.conf import settings
from .model.song import Song
from .model.playlist import Playlist
from .forms import SongRequestForm
from .generator.factory import get_generator_strategy
import os
import requests as http_requests


@login_required
def library_view(request):
    """View to list all generated songs in the library, with optional search."""
    user = request.user
    query = request.GET.get('q', '').strip()
    songs = Song.objects.filter(user=user)
    if query:
        songs = songs.filter(name__icontains=query)
    songs = songs.order_by('-dateOfCreation')
    playlists = Playlist.objects.filter(user=user)
    return render(request, 'musicaaApp/library.html', {
        'songs': songs,
        'playlists': playlists,
        'search_query': query,
    })


@login_required
def generate_view(request):
    """View to handle the song generation form and dispatch to logic."""
    if request.method == 'POST':
        form = SongRequestForm(request.POST)
        if form.is_valid():
            user = request.user
            song_request = form.save(commit=False)
            song_request.user = user
            song_request.save()

            try:
                strategy = get_generator_strategy()
                task_id = strategy.generate(song_request)
                new_song = Song.objects.create(
                    name=song_request.name,
                    lengthInSeconds=song_request.lengthInSeconds,
                    user=user,
                    status=Song.Status.GENERATING,
                    task_id=task_id
                )
            except Exception as e:
                new_song = Song.objects.create(
                    name=song_request.name,
                    lengthInSeconds=song_request.lengthInSeconds,
                    user=user,
                    status=Song.Status.ERROR,
                    task_id=None
                )
                print("Generation Error:", str(e))

            song_request.song = new_song
            song_request.save()
            return redirect('library')
    else:
        form = SongRequestForm()
    return render(request, 'musicaaApp/generate.html', {'form': form})


@login_required
def delete_song_view(request, song_id):
    """Delete a song owned by the current user."""
    song = get_object_or_404(Song, id=song_id, user=request.user)
    if request.method == 'POST':
        # Remove the local MP3 file if it exists
        if song.audio_url and song.audio_url.startswith(settings.MEDIA_URL):
            rel_path = song.audio_url.replace(settings.MEDIA_URL, '')
            abs_path = os.path.join(settings.MEDIA_ROOT, rel_path)
            if os.path.exists(abs_path):
                os.remove(abs_path)
        song.delete()
    return redirect('library')


@login_required
def download_song_view(request, song_id):
    """Serve the MP3 of a user's own song as a file download."""
    song = get_object_or_404(Song, id=song_id, user=request.user)
    return _serve_mp3_download(song)


def shared_song_view(request, share_token):
    """Public view for a shared song — no login required, no creator info exposed."""
    song = get_object_or_404(Song, share_token=share_token, status=Song.Status.READY)
    return render(request, 'musicaaApp/shared_song.html', {'song': song})


def download_shared_song_view(request, share_token):
    """Public download of a shared song — no login required."""
    song = get_object_or_404(Song, share_token=share_token, status=Song.Status.READY)
    return _serve_mp3_download(song)


def _serve_mp3_download(song):
    """Helper to stream an MP3 as a downloadable file response.
    Returns JsonResponse with error if file is not a locally stored file."""
    if song.audio_url and song.audio_url.startswith(settings.MEDIA_URL):
        rel_path = song.audio_url.replace(settings.MEDIA_URL, '', 1).lstrip('/')
        abs_path = os.path.join(settings.MEDIA_ROOT, rel_path)
        if os.path.exists(abs_path):
            response = FileResponse(open(abs_path, 'rb'), content_type='audio/mpeg')
            safe_name = song.name.replace(' ', '_').encode('ascii', 'ignore').decode()
            response['Content-Disposition'] = f'attachment; filename="{safe_name}.mp3"'
            return response
        else:
            return JsonResponse({
                'error': 'The audio file was not found on the server.',
                'detail': 'The file may have been deleted or moved. Try re-generating the song.'
            }, status=404)
    else:
        return JsonResponse({
            'error': 'This song cannot be downloaded.',
            'detail': 'Songs generated in Mock mode do not produce a real audio file. Switch to Suno mode to generate downloadable songs.'
        }, status=400)


@login_required
def playlists_view(request):
    """View to list and create playlists."""
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Playlist.objects.create(name=name, user=user)
        return redirect('playlists')
    playlists = Playlist.objects.filter(user=user)
    return render(request, 'musicaaApp/playlists.html', {'playlists': playlists})


@login_required
def playlist_detail_view(request, playlist_id):
    """View songs inside a specific playlist."""
    user = request.user
    try:
        playlist = Playlist.objects.get(id=playlist_id, user=user)
    except Playlist.DoesNotExist:
        return redirect('playlists')
    return render(request, 'musicaaApp/playlist_detail.html', {'playlist': playlist})


@login_required
def add_to_playlist_action(request, song_id):
    """Action to add a song to a playlist."""
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist_id')
        user = request.user
        if playlist_id:
            try:
                playlist = Playlist.objects.get(id=playlist_id, user=user)
                song = Song.objects.get(id=song_id)
                playlist.songs.add(song)
            except (Playlist.DoesNotExist, Song.DoesNotExist):
                pass
    return redirect('library')


@login_required
def remove_from_playlist_action(request, playlist_id, song_id):
    """Action to remove a song from a playlist."""
    if request.method == 'POST':
        user = request.user
        try:
            playlist = Playlist.objects.get(id=playlist_id, user=user)
            song = Song.objects.get(id=song_id)
            playlist.songs.remove(song)
        except (Playlist.DoesNotExist, Song.DoesNotExist):
            pass
    return redirect('playlist_detail', playlist_id=playlist_id)


@login_required
def poll_generation_status(request):
    """API endpoint to poll generating songs and update them if ready."""
    user = request.user
    generating_songs = Song.objects.filter(user=user, status=Song.Status.GENERATING)

    updated_count = 0
    strategy = get_generator_strategy()

    for song in generating_songs:
        if song.task_id:
            try:
                status_data = strategy.get_status(song.task_id)
                status_val = status_data.get('status', '').upper()
                if status_val in ['SUCCESS', 'READY', 'TEXT_SUCCESS', 'FIRST_SUCCESS']:
                    song.status = Song.Status.READY
                    audio_url = status_data.get('audio_url')
                    if audio_url:
                        try:
                            import imageio_ffmpeg
                            import subprocess

                            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                            temp_path = os.path.join(settings.MEDIA_ROOT, f"temp_{song.task_id}.mp3")
                            final_path = os.path.join(settings.MEDIA_ROOT, f"song_{song.task_id}.mp3")
                            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

                            r = http_requests.get(audio_url)
                            if r.status_code == 200:
                                with open(temp_path, 'wb') as f:
                                    f.write(r.content)

                                target_sec = song.lengthInSeconds
                                fade_start = max(0, target_sec - 2)
                                cmd = [
                                    ffmpeg_exe, '-y', '-i', temp_path,
                                    '-t', str(target_sec),
                                    '-af', f'afade=t=out:st={fade_start}:d=2',
                                    final_path
                                ]
                                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                if os.path.exists(temp_path):
                                    os.remove(temp_path)
                                song.audio_url = f"{settings.MEDIA_URL}song_{song.task_id}.mp3"
                            else:
                                song.audio_url = audio_url
                        except Exception as e:
                            print("Error cropping audio:", str(e))
                            song.audio_url = audio_url

                    song.save()
                    updated_count += 1
                elif status_val == 'ERROR':
                    song.status = Song.Status.ERROR
                    song.save()
                    updated_count += 1
            except Exception:
                pass

    return JsonResponse({'updated_count': updated_count})



@login_required
def generate_view(request):
    """View to handle the song generation form and dispatch to logic."""
    if request.method == 'POST':
        form = SongRequestForm(request.POST)
        if form.is_valid():
            user = request.user
            
            song_request = form.save(commit=False)
            song_request.user = user
            song_request.save()
            
            # --- APPLY STRATEGY PATTERN ---
            try:
                strategy = get_generator_strategy()
                task_id = strategy.generate(song_request)
                
                # Create a shell song object to represent it in the library
                new_song = Song.objects.create(
                    name=song_request.name,
                    lengthInSeconds=song_request.lengthInSeconds,
                    user=user,
                    status=Song.Status.GENERATING,
                    task_id=task_id
                )
            except Exception as e:
                # If API fails, create an error song instead of crashing
                new_song = Song.objects.create(
                    name=song_request.name,
                    lengthInSeconds=song_request.lengthInSeconds,
                    user=user,
                    status=Song.Status.ERROR,
                    task_id=None
                )
                print("Generation Error:", str(e))
            
            # Link via OneToOne if necessary
            song_request.song = new_song
            song_request.save()
            
            return redirect('library')
    else:
        form = SongRequestForm()
    return render(request, 'musicaaApp/generate.html', {'form': form})

@login_required
def playlists_view(request):
    """View to list and create playlists."""
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Playlist.objects.create(name=name, user=user)
        return redirect('playlists')
        
    playlists = Playlist.objects.filter(user=user)
    return render(request, 'musicaaApp/playlists.html', {'playlists': playlists})

@login_required
def playlist_detail_view(request, playlist_id):
    """View songs inside a specific playlist."""
    user = request.user
    try:
        playlist = Playlist.objects.get(id=playlist_id, user=user)
    except Playlist.DoesNotExist:
        return redirect('playlists')
    return render(request, 'musicaaApp/playlist_detail.html', {'playlist': playlist})

@login_required
def add_to_playlist_action(request, song_id):
    """Action to add a song to a playlist."""
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist_id')
        user = request.user
        if playlist_id:
            try:
                playlist = Playlist.objects.get(id=playlist_id, user=user)
                song = Song.objects.get(id=song_id)
                playlist.songs.add(song)
            except (Playlist.DoesNotExist, Song.DoesNotExist):
                pass
    return redirect('library')

@login_required
def remove_from_playlist_action(request, playlist_id, song_id):
    """Action to remove a song from a playlist."""
    if request.method == 'POST':
        user = request.user
        try:
            playlist = Playlist.objects.get(id=playlist_id, user=user)
            song = Song.objects.get(id=song_id)
            playlist.songs.remove(song)
        except (Playlist.DoesNotExist, Song.DoesNotExist):
            pass
    return redirect('playlist_detail', playlist_id=playlist_id)

from django.http import JsonResponse

@login_required
def poll_generation_status(request):
    """API endpoint to poll generating songs and update them if ready."""
    user = request.user
    generating_songs = Song.objects.filter(user=user, status=Song.Status.GENERATING)
    
    updated_count = 0
    strategy = get_generator_strategy()
    
    for song in generating_songs:
        if song.task_id:
            try:
                status_data = strategy.get_status(song.task_id)
                status_val = status_data.get('status', '').upper()
                if status_val in ['SUCCESS', 'READY', 'TEXT_SUCCESS', 'FIRST_SUCCESS']:
                    song.status = Song.Status.READY
                    audio_url = status_data.get('audio_url')
                    if audio_url:
                        try:
                            import imageio_ffmpeg
                            import subprocess
                            import os
                            import requests
                            from django.conf import settings
                            
                            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
                            
                            temp_path = os.path.join(settings.MEDIA_ROOT, f"temp_{song.task_id}.mp3")
                            final_path = os.path.join(settings.MEDIA_ROOT, f"song_{song.task_id}.mp3")
                            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
                            
                            r = requests.get(audio_url)
                            if r.status_code == 200:
                                with open(temp_path, 'wb') as f:
                                    f.write(r.content)
                                    
                                target_sec = song.lengthInSeconds
                                fade_start = max(0, target_sec - 2)
                                
                                # Crop to target length and add a 2 second fade out using direct ffmpeg call
                                cmd = [
                                    ffmpeg_exe,
                                    '-y',
                                    '-i', temp_path,
                                    '-t', str(target_sec),
                                    '-af', f'afade=t=out:st={fade_start}:d=2',
                                    final_path
                                ]
                                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                
                                if os.path.exists(temp_path):
                                    os.remove(temp_path)
                                    
                                song.audio_url = f"{settings.MEDIA_URL}song_{song.task_id}.mp3"
                            else:
                                song.audio_url = audio_url
                        except Exception as e:
                            print("Error cropping audio:", str(e))
                            song.audio_url = audio_url
                            
                    song.save()
                    updated_count += 1
                elif status_val == 'ERROR':
                    song.status = Song.Status.ERROR
                    song.save()
                    updated_count += 1
            except Exception:
                pass
                
    return JsonResponse({'updated_count': updated_count})
