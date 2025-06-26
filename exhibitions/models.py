from django.db import models
from artists.models import Artist
from artworks.models import Artwork

class Exhibition(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    start_date = models.DateField()
    end_date = models.DateField()
    artworks = models.ManyToManyField(Artwork, through='ExhibitionArtwork')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.artist.name}"
    
    class Meta:
        ordering = ['-created_at']

class ExhibitionArtwork(models.Model):
    """전시-작품 연결 모델"""
    exhibition = models.ForeignKey(Exhibition, on_delete=models.CASCADE)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('exhibition', 'artwork')
