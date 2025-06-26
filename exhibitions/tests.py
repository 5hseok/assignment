from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from artists.models import Artist
from artworks.models import Artwork
from .models import Exhibition, ExhibitionArtwork


class ExhibitionModelTest(TestCase):
    """Exhibition 모델에 대한 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='artist',
            email='artist@example.com',
            password='artistpass123'
        )
        self.artist = Artist.objects.create(
            user=self.user,
            name='김작가',
            gender='남자',
            birthday=date(1990, 1, 1),
            email='artist@example.com',
            phone_number='010-1234-5678'
        )
        self.artwork1 = Artwork.objects.create(
            artist=self.artist,
            title='작품1',
            price=1000000,
            size_number=50
        )
        self.artwork2 = Artwork.objects.create(
            artist=self.artist,
            title='작품2',
            price=2000000,
            size_number=100
        )
    
    def test_exhibition_creation(self):
        """전시 생성 테스트"""
        exhibition = Exhibition.objects.create(
            artist=self.artist,
            title='테스트 전시',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30)
        )
        
        self.assertEqual(exhibition.title, '테스트 전시')
        self.assertEqual(exhibition.artist, self.artist)
        self.assertEqual(str(exhibition), '테스트 전시 - 김작가')
    
    def test_exhibition_ordering(self):
        """전시 정렬 테스트 (최신순)"""
        exhibition1 = Exhibition.objects.create(
            artist=self.artist,
            title='첫번째 전시',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30)
        )
        
        exhibition2 = Exhibition.objects.create(
            artist=self.artist,
            title='두번째 전시',
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=40)
        )
        
        exhibitions = Exhibition.objects.all()
        self.assertEqual(exhibitions[0], exhibition2)  # 최신이 먼저
        self.assertEqual(exhibitions[1], exhibition1)


class ExhibitionArtworkModelTest(TestCase):
    """ExhibitionArtwork 모델에 대한 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='artist',
            email='artist@example.com',
            password='artistpass123'
        )
        self.artist = Artist.objects.create(
            user=self.user,
            name='김작가',
            gender='남자',
            birthday=date(1990, 1, 1),
            email='artist@example.com',
            phone_number='010-1234-5678'
        )
        self.artwork = Artwork.objects.create(
            artist=self.artist,
            title='작품1',
            price=1000000,
            size_number=50
        )
        self.exhibition = Exhibition.objects.create(
            artist=self.artist,
            title='테스트 전시',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30)
        )
    
    def test_exhibition_artwork_creation(self):
        """전시-작품 연결 테스트"""
        exhibition_artwork = ExhibitionArtwork.objects.create(
            exhibition=self.exhibition,
            artwork=self.artwork
        )
        
        self.assertEqual(exhibition_artwork.exhibition, self.exhibition)
        self.assertEqual(exhibition_artwork.artwork, self.artwork)


class ExhibitionViewTest(TestCase):
    """Exhibition 뷰에 대한 테스트"""
    
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
        self.artwork1 = Artwork.objects.create(
            artist=self.artist,
            title='작품1',
            price=1000000,
            size_number=50
        )
        self.artwork2 = Artwork.objects.create(
            artist=self.artist,
            title='작품2',
            price=2000000,
            size_number=100
        )
        self.exhibition = Exhibition.objects.create(
            artist=self.artist,
            title='테스트 전시',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30)
        )
    
    def test_exhibition_list_view(self):
        """전시 목록 조회 테스트"""
        response = self.client.get(reverse('exhibitions:exhibition_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 전시')


class ExhibitionIntegrationTest(TestCase):
    """전시 관련 통합 테스트"""
    
    def setUp(self):
        self.client = Client()
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
    
    def test_exhibition_creation_workflow(self):
        """전시 생성 전체 워크플로우 테스트"""
        # 1. 먼저 작품들을 생성
        artwork1 = Artwork.objects.create(
            artist=self.artist,
            title='전시용 작품1',
            price=3000000,
            size_number=150
        )
        artwork2 = Artwork.objects.create(
            artist=self.artist,
            title='전시용 작품2',
            price=4000000,
            size_number=200
        )
        
        # 2. 전시 생성
        start_date = date.today() + timedelta(days=15)
        end_date = date.today() + timedelta(days=45)
        
        exhibition = Exhibition.objects.create(
            artist=self.artist,
            title='워크플로우 테스트 전시',
            start_date=start_date,
            end_date=end_date
        )
        
        # 3. 작품들을 전시에 연결
        ExhibitionArtwork.objects.create(exhibition=exhibition, artwork=artwork1)
        ExhibitionArtwork.objects.create(exhibition=exhibition, artwork=artwork2)
        
        # 4. 전시가 데이터베이스에 저장되었는지 확인
        self.assertEqual(exhibition.artist, self.artist)
        self.assertEqual(exhibition.start_date, start_date)
        self.assertEqual(exhibition.end_date, end_date)
        
        # 5. 작품들이 올바르게 연결되었는지 확인
        self.assertEqual(exhibition.artworks.count(), 2)
        self.assertIn(artwork1, exhibition.artworks.all())
        self.assertIn(artwork2, exhibition.artworks.all())
        
        # 6. ExhibitionArtwork 중간 테이블 확인
        self.assertEqual(ExhibitionArtwork.objects.filter(exhibition=exhibition).count(), 2)
        
        # 7. 전시 목록에서 확인 가능한지 테스트
        response = self.client.get(reverse('exhibitions:exhibition_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '워크플로우 테스트 전시')
    
    def test_multiple_exhibitions(self):
        """여러 전시 테스트"""
        # 여러 전시 생성
        exhibition1 = Exhibition.objects.create(
            artist=self.artist,
            title='첫번째 전시',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30)
        )
        
        exhibition2 = Exhibition.objects.create(
            artist=self.artist,
            title='두번째 전시',
            start_date=date.today() + timedelta(days=40),
            end_date=date.today() + timedelta(days=70)
        )
        
        # 전시 목록에서 모두 확인
        response = self.client.get(reverse('exhibitions:exhibition_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '첫번째 전시')
        self.assertContains(response, '두번째 전시')
        
        # 정렬 확인 (최신순)
        exhibitions = Exhibition.objects.all()
        self.assertEqual(exhibitions[0], exhibition2)
        self.assertEqual(exhibitions[1], exhibition1)
