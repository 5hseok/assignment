from artists.models import Artist

def user_extras(request):
    """사용자 관련 추가 정보를 템플릿에 제공"""
    context = {}
    if request.user.is_authenticated:
        try:
            context['user_artist'] = Artist.objects.get(user=request.user)
        except Artist.DoesNotExist:
            context['user_artist'] = None
    else:
        context['user_artist'] = None
    return context
