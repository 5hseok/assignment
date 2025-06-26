from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Artwork
from artists.models import Artist

def artwork_list(request):
    search_query = request.GET.get('search', '')
    artworks = Artwork.objects.all().order_by('-created_at')
    
    if search_query:
        artworks = artworks.filter(
            Q(title__icontains=search_query) |
            Q(artist__name__icontains=search_query)
        )
    
    paginator = Paginator(artworks, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'gallery/artwork_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })

@login_required
def create_artwork(request):
    try:
        artist = Artist.objects.get(user=request.user)
    except Artist.DoesNotExist:
        messages.error(request, '작가로 등록되지 않은 사용자입니다.')
        return redirect('auth_management:home')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        size_number = request.POST.get('size_number')
        
        if not all([title, price, size_number]):
            messages.error(request, '모든 필드를 입력해주세요.')
            return render(request, 'artist/create_artwork.html')
        
        try:
            # 가격에서 콤마 제거
            price = int(price.replace(',', ''))
            size_number = int(size_number)
            
            artwork = Artwork.objects.create(
                artist=artist,
                title=title,
                price=price,
                size_number=size_number
            )
            messages.success(request, '작품이 성공적으로 등록되었습니다.')
            return redirect('artists:artist_dashboard')
        except ValueError:
            messages.error(request, '가격과 호수는 숫자여야 합니다.')
        except Exception as e:
            messages.error(request, f'작품 등록 중 오류가 발생했습니다: {str(e)}')
    
    return render(request, 'artist/create_artwork.html')
