from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import date, datetime
from .models import Artist, ArtistApplication
from artworks.models import Artwork
import json


class ArtistModelTest(TestCase):
    """Artist 모델에 대한 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_artist_creation(self):
        """작가 생성 테스트"""
        artist = Artist.objects.create(
            user=self.user,
            name='김작가',
            gender='남자',
            birthday=date(1990, 1, 1),
            email='artist@example.com',
            phone_number='010-1234-5678'
        )
        
        self.assertEqual(artist.name, '김작가')
        self.assertEqual(artist.gender, '남자')
        self.assertEqual(artist.user, self.user)
        self.assertEqual(str(artist), '김작가')
    
    def test_artist_phone_number_validation(self):
        """작가 전화번호 유효성 검사 테스트"""
        artist = Artist(
            user=self.user,
            name='김작가',
            gender='남자',
            birthday=date(1990, 1, 1),
            email='artist@example.com',
            phone_number='010-12345-6789'  # 잘못된 형식
        )
        
        with self.assertRaises(ValidationError):
            artist.full_clean()


class ArtistApplicationModelTest(TestCase):
    """ArtistApplication 모델에 대한 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='applicant',
            email='applicant@example.com',
            password='testpass123'
        )
    
    def test_artist_application_creation(self):
        """작가 신청 생성 테스트"""
        application = ArtistApplication.objects.create(
            user=self.user,
            name='신청자',
            gender='여자',
            birthday=date(1995, 5, 15),
            email='applicant@example.com',
            phone_number='010-9876-5432'
        )
        
        self.assertEqual(application.status, 'pending')  # 기본값 확인
        self.assertEqual(application.name, '신청자')
        self.assertEqual(str(application), '신청자 - 대기중')
    
    def test_artist_application_ordering(self):
        """작가 신청 정렬 테스트 (최신순)"""
        app1 = ArtistApplication.objects.create(
            user=self.user,
            name='첫번째',
            gender='남자',
            birthday=date(1990, 1, 1),
            email='first@example.com',
            phone_number='010-1111-1111'
        )
        
        # 약간의 시간 차이를 위해
        app2 = ArtistApplication.objects.create(
            user=self.user,
            name='두번째',
            gender='여자',
            birthday=date(1992, 2, 2),
            email='second@example.com',
            phone_number='010-2222-2222'
        )
        
        applications = ArtistApplication.objects.all()
        self.assertEqual(applications[0], app2)  # 최신이 먼저
        self.assertEqual(applications[1], app1)


class ArtistViewTest(TestCase):
    """Artist 뷰에 대한 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.artist_user = User.objects.create_user(
            username='artist',
            email='artist@example.com',
            password='artistpass123'
        )
        self.artist = Artist.objects.create(
            user=self.artist_user,
            name='김작가',
            gender='남자',
            birthday=date(1990, 1, 1),
            email='artist@example.com',
            phone_number='010-1234-5678'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
    
    def test_artist_list_view(self):
        """작가 목록 조회 테스트"""
        response = self.client.get(reverse('artists:artist_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '김작가')
    
    def test_artist_list_search(self):
        """작가 목록 검색 기능 테스트"""
        response = self.client.get(reverse('artists:artist_list'), {'search': '김작가'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '김작가')
        
        # 없는 이름으로 검색
        response = self.client.get(reverse('artists:artist_list'), {'search': '없는작가'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '김작가')


class ArtistIntegrationTest(TestCase):
    """작가 관련 통합 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
    
    def test_artist_list_workflow(self):
        """작가 목록 조회 워크플로우 테스트"""
        # 작가 생성
        artist_user = User.objects.create_user(
            username='newartist',
            email='newartist@example.com',
            password='artistpass123'
        )
        artist = Artist.objects.create(
            user=artist_user,
            name='신규작가',
            gender='남자',
            birthday=date(1985, 6, 15),
            email='newartist@example.com',
            phone_number='010-5555-6666'
        )
        
        # 작가 목록에서 확인
        response = self.client.get(reverse('artists:artist_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '신규작가')
        
        # 검색 기능 테스트
        response = self.client.get(reverse('artists:artist_list'), {'search': '신규'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '신규작가')
