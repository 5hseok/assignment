from django import template
from artists.models import Artist

register = template.Library()

@register.filter
def is_artist(user):
    """사용자가 작가인지 확인"""
    if not user.is_authenticated:
        return False
    try:
        Artist.objects.get(user=user)
        return True
    except Artist.DoesNotExist:
        return False

@register.filter
def get_artist(user):
    """사용자의 작가 정보 반환"""
    if not user.is_authenticated:
        return None
    try:
        return Artist.objects.get(user=user)
    except Artist.DoesNotExist:
        return None
