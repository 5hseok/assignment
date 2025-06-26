from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Artist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    gender = models.CharField(max_length=6, choices=[('남자', '남자'), ('여자', '여자')])
    birthday = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, validators=[
        RegexValidator(r'^\d{3}-\d{4}-\d{4}$', '000-0000-0000 형식으로 입력하세요.')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class ArtistApplication(models.Model):
    """작가 등록 신청 모델"""
    STATUS_CHOICES = [
        ('pending', '대기중'),
        ('approved', '승인'),
        ('rejected', '반려'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    gender = models.CharField(max_length=6, choices=[('남자', '남자'), ('여자', '여자')])
    birthday = models.DateField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, validators=[
        RegexValidator(r'^\d{3}-\d{4}-\d{4}$', '000-0000-0000 형식으로 입력하세요.')
    ])
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
    
    class Meta:
        ordering = ['-applied_at']
