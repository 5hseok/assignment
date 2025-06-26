from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Exhibition, ExhibitionArtwork
from artists.models import Artist
from artworks.models import Artwork

def exhibition_list(request):
    exhibitions = Exhibition.objects.all().order_by('-created_at')
    return render(request, 'gallery/exhibition_list.html', {
        'exhibitions': exhibitions
    })

@login_required
def create_exhibition(request):
    try:
        artist = Artist.objects.get(user=request.user)
    except Artist.DoesNotExist:
        messages.error(request, '작가로 등록되지 않은 사용자입니다.')
        return redirect('auth_management:home')
    
    artworks = Artwork.objects.filter(artist=artist)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        selected_artworks = request.POST.getlist('artworks')
        
        if not all([title, start_date, end_date]):
            messages.error(request, '제목, 시작일, 종료일을 모두 입력해주세요.')
            return render(request, 'artist/create_exhibition.html', {'artworks': artworks})
        
        if not selected_artworks:
            messages.error(request, '최소 하나 이상의 작품을 선택해주세요.')
            return render(request, 'artist/create_exhibition.html', {'artworks': artworks})
        
        try:
            exhibition = Exhibition.objects.create(
                artist=artist,
                title=title,
                start_date=start_date,
                end_date=end_date
            )
            
            # 선택된 작품들을 전시에 추가
            for artwork_id in selected_artworks:
                artwork = Artwork.objects.get(id=artwork_id, artist=artist)
                ExhibitionArtwork.objects.create(
                    exhibition=exhibition,
                    artwork=artwork
                )
            
            messages.success(request, '전시가 성공적으로 등록되었습니다.')
            return redirect('artists:artist_dashboard')
        except Exception as e:
            messages.error(request, f'전시 등록 중 오류가 발생했습니다: {str(e)}')
    
    return render(request, 'artist/create_exhibition.html', {'artworks': artworks})
