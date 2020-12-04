from django.shortcuts import render, redirect
from django.views import View
# from django.views.generic import ListView
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy

from rest_framework import generics
from rest_framework import permissions
from .serializers import ArtistSerializer, SongSerializer
from .models import Artist



# Create your views here.
from .models import Artist, Song

# def artist_list(request):
#     artists = Artist.objects.all()
#     return render(request, 'tunr/artist_list.html', {'artists': artists})

class ArtistList(View):
    def get(self, request):
        artists = Artist.objects.all()
        return render(request, 'tunr/artist_list.html', {'artists': artists})

class ArtistDetail(DetailView):
    queryset = Artist.objects.all()
    context_object_name = 'artist'

# def artist_detail(request, pk):
#     artist = Artist.objects.get(id=pk)
#     return render(request, 'tunr/artist_detail.html', {'artist': artist})

# def song_list(request):
#     songs = Song.objects.all()
#     return render(request, 'tunr/song_list.html', {'songs': songs})

class SongList(ListView):
    model = Song
    context_object_name = 'songs'

# def song_detail(request, pk):
#     song = Song.objects.get(id=pk)
#     return render(request, 'tunr/song_detail.html', {'song': song})

class SongDetail(DetailView):
    queryset = Song.objects.all()
    context_object_name = 'song'

from .forms import ArtistForm, SongForm

# def artist_create(request):
#     #Responds whens someone wants to create a new artist
#     if request.method == 'POST':
#         #Make that post request into a model form
#         form = ArtistForm(request.POST)
#         if form.is_valid():
#             artist = form.save()
#             #The above command saves it in the database
#             #The one below redirects to detail page
#             return redirect('artist_detail', pk=artist.pk)
#     else:
#         form = ArtistForm()
#     return render(request, 'tunr/artist_form.html', {'form': form})

class ArtistCreate(View):
    def get(self, request):
        form = ArtistForm()
        return render(request, 'tunr/artist_form.html', {'form': form})

    def post(self, request):
        form = ArtistForm(request.POST)
        if form.is_valid():
            artist = form.save()
            return redirect('artist_detail', pk=artist.pk)

        return render(request, 'tunr/artist_form.html', {'form': form})


def artist_edit(request, pk):
    artist = Artist.objects.get(pk=pk)
    if request.method == "POST":
        form = ArtistForm(request.POST, instance=artist)
        if form.is_valid():
            artist = form.save()
            return redirect('artist_detail', pk=artist.pk)
    else:
        form = ArtistForm(instance=artist)
    return render(request, 'tunr/artist_form.html', {'form': form})


# def song_create(request):
#     if request.method == 'POST':
#         form = SongForm(request.POST)
#         if form.is_valid():
#             song = form.save()
#             return redirect('song_detail', pk=song.pk)
#     else:
#         form = SongForm()
#     return render(request, 'tunr/song_form.html', {'form': form})

# def song_edit(request, pk):
#     song = Song.objects.get(pk=pk)
#     if request.method == "POST":
#         form = SongForm(request.POST, instance=song)
#         if form.is_valid():
#             artist = form.save()
#             return redirect('song_detail', pk=song.pk)
#     else:
#         form = SongForm(instance=song)
#     return render(request, 'tunr/song_form.html', {'form': form})

def artist_delete(request, pk):
    Artist.objects.get(id=pk).delete()
    return redirect('artist_list')

# def song_delete(request, pk):
#     Song.objects.get(id=pk).delete()
#     return redirect('song_list')

class SongCreate(CreateView):
    model = Song
    fields = ('title', 'album', 'preview_url', 'artist')

class SongEdit(UpdateView):
    model = Song
    fields = ('title', 'album', 'preview_url', 'artist')

class SongDelete(DeleteView):
    model = Song
    success_url = reverse_lazy('song_list')

class ArtistList(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ArtistDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer 
    permission_classes = (permissions.IsAuthenticated,)   

class SongList(generics.ListCreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    permission_classes = (permissions.IsAuthenticated,)

class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer 
    permission_classes = (permissions.IsAuthenticated,)       