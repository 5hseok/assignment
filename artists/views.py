from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.utils import timezone
from .models import Artist, ArtistApplication
from artworks.models import Artwork
import csv

def artist_list(request):
    search_query = request.GET.get('search', '')
    artists = Artist.objects.all().order_by('-created_at')
    
    if search_query:
        artists = artists.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    
    paginator = Paginator(artists, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'gallery/artist_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })

@login_required
def apply_artist(request):
    # 관리자는 작가 신청할 수 없음
    if request.user.is_staff:
        messages.error(request, '관리자는 작가 등록을 신청할 수 없습니다.')
        return redirect('auth_management:home')
    
    # 이미 작가로 승인된 사용자는 접근 불가
    try:
        artist = Artist.objects.get(user=request.user)
        messages.warning(request, '이미 작가로 등록되어 있습니다.')
        return redirect('artists:artist_dashboard')
    except Artist.DoesNotExist:
        pass
    
    # 이미 신청한 사용자는 접근 불가
    existing_application = ArtistApplication.objects.filter(user=request.user, status='pending').first()
    if existing_application:
        messages.warning(request, '이미 작가 등록 신청을 하셨습니다.')
        return redirect('auth_management:home')
    
    if request.method == 'POST':
        # 폼 데이터 검증 및 저장
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        birthday = request.POST.get('birthday')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        
        # 기본 검증 (JavaScript에서도 검증하지만 서버에서도 검증)
        if not all([name, gender, birthday, email, phone_number]):
            messages.error(request, '모든 필드를 입력해주세요.')
            return render(request, 'artist/apply.html')
        
        try:
            application = ArtistApplication.objects.create(
                user=request.user,
                name=name,
                gender=gender,
                birthday=birthday,
                email=email,
                phone_number=phone_number
            )
            messages.success(request, '작가 등록 신청이 완료되었습니다. 관리자 승인을 기다려주세요.')
            return redirect('auth_management:home')
        except Exception as e:
            messages.error(request, f'신청 중 오류가 발생했습니다: {str(e)}')
    
    return render(request, 'artist/apply.html')

@login_required
def artist_dashboard(request):
    try:
        artist = Artist.objects.get(user=request.user)
    except Artist.DoesNotExist:
        messages.error(request, '작가로 등록되지 않은 사용자입니다.')
        return redirect('auth_management:home')
    
    artworks = Artwork.objects.filter(artist=artist).order_by('-created_at')
    
    return render(request, 'artist/dashboard.html', {
        'artist': artist,
        'artworks': artworks
    })

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, '관리자만 접근할 수 있습니다.')
        return redirect('auth_management:home')
    
    # 통계 데이터 계산
    total_artists = Artist.objects.count()
    total_artworks = Artwork.objects.count()
    pending_applications = ArtistApplication.objects.filter(status='pending').count()
    
    return render(request, 'admin/dashboard.html', {
        'total_artists': total_artists,
        'total_artworks': total_artworks,
        'pending_applications': pending_applications,
    })

@login_required
def admin_applications(request):
    if not request.user.is_staff:
        messages.error(request, '관리자만 접근할 수 있습니다.')
        return redirect('auth_management:home')
    
    search_query = request.GET.get('search', '')
    applications = ArtistApplication.objects.all().order_by('-applied_at')
    
    if search_query:
        applications = applications.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    
    return render(request, 'admin/applications.html', {
        'applications': applications,
        'search_query': search_query
    })

@login_required
def admin_statistics(request):
    if not request.user.is_staff:
        messages.error(request, '관리자만 접근할 수 있습니다.')
        return redirect('auth_management:home')
    
    # 작가별 통계 계산
    artists = Artist.objects.annotate(
        small_artwork_count=Count('artwork', filter=Q(artwork__size_number__lte=100)),
        avg_price=Avg('artwork__price')
    ).order_by('name')
    
    return render(request, 'admin/statistics.html', {
        'artists': artists
    })

@login_required
def process_applications(request):
    if not request.user.is_staff:
        return JsonResponse({'error': '권한이 없습니다.'}, status=403)
    
    if request.method == 'POST':
        action = request.POST.get('action')  # approve or reject
        application_ids = request.POST.getlist('application_ids')
        
        if not application_ids:
            return JsonResponse({'error': '선택된 신청이 없습니다.'}, status=400)
        
        applications = ArtistApplication.objects.filter(
            id__in=application_ids, 
            status='pending'
        )
        
        count = 0
        for application in applications:
            if action == 'approve':
                # Artist 객체 생성
                Artist.objects.create(
                    user=application.user,
                    name=application.name,
                    gender=application.gender,
                    birthday=application.birthday,
                    email=application.email,
                    phone_number=application.phone_number
                )
                application.status = 'approved'
            elif action == 'reject':
                application.status = 'rejected'
            
            application.processed_at = timezone.now()
            application.save()
            count += 1
        
        return JsonResponse({
            'success': True,
            'message': f'{count}개의 신청이 처리되었습니다.',
            'processed_count': count
        })
    
    return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)
