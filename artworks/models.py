from django.db import models
from artists.models import Artist
from django.core.validators import MinValueValidator, MaxValueValidator

class Artwork(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    price = models.PositiveBigIntegerField()  # 0 이상 자동 보장
    size_number = models.PositiveIntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(500)
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.artist.name}"
    
    def formatted_price(self):
        """가격을 천 단위 콤마로 포맷팅"""
        return f"{self.price:,}"
    
    class Meta:
        ordering = ['-created_at']
