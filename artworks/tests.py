from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from datetime import date
from artists.models import Artist
from .models import Artwork


class ArtworkModelTest(TestCase):
    """Artwork 모델에 대한 테스트"""
    
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
    
    def test_artwork_creation(self):
        """작품 생성 테스트"""
        artwork = Artwork.objects.create(
            artist=self.artist,
            title='테스트 작품',
            price=1000000,
            size_number=50
        )
        
        self.assertEqual(artwork.title, '테스트 작품')
        self.assertEqual(artwork.price, 1000000)
        self.assertEqual(artwork.size_number, 50)
        self.assertEqual(artwork.artist, self.artist)
        self.assertEqual(str(artwork), '테스트 작품 - 김작가')
    
    def test_artwork_formatted_price(self):
        """작품 가격 포맷팅 테스트"""
        artwork = Artwork.objects.create(
            artist=self.artist,
            title='테스트 작품',
            price=1234567,
            size_number=50
        )
        
        self.assertEqual(artwork.formatted_price(), '1,234,567')
    
    def test_artwork_size_number_validation(self):
        """작품 호수 유효성 검사 테스트"""
        # 0호는 불가능
        artwork = Artwork(
            artist=self.artist,
            title='테스트 작품',
            price=1000000,
            size_number=0
        )
        
        with self.assertRaises(ValidationError):
            artwork.full_clean()
        
        # 500호 초과는 불가능
        artwork.size_number = 501
        with self.assertRaises(ValidationError):
            artwork.full_clean()
    
    def test_artwork_ordering(self):
        """작품 정렬 테스트 (최신순)"""
        artwork1 = Artwork.objects.create(
            artist=self.artist,
            title='첫번째 작품',
            price=1000000,
            size_number=50
        )
        
        artwork2 = Artwork.objects.create(
            artist=self.artist,
            title='두번째 작품',
            price=2000000,
            size_number=100
        )
        
        artworks = Artwork.objects.all()
        self.assertEqual(artworks[0], artwork2)  # 최신이 먼저
        self.assertEqual(artworks[1], artwork1)


class ArtworkViewTest(TestCase):
    """Artwork 뷰에 대한 테스트"""
    
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
        self.artwork = Artwork.objects.create(
            artist=self.artist,
            title='테스트 작품',
            price=1000000,
            size_number=50
        )
    
    def test_artwork_list_view(self):
        """작품 목록 조회 테스트"""
        response = self.client.get(reverse('artworks:artwork_list'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 작품')
    
    def test_artwork_list_search(self):
        """작품 목록 검색 기능 테스트"""
        response = self.client.get(reverse('artworks:artwork_list'), {'search': '테스트'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '테스트 작품')
        
        # 없는 제목으로 검색
        response = self.client.get(reverse('artworks:artwork_list'), {'search': '없는작품'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '테스트 작품')


class ArtworkIntegrationTest(TestCase):
    """작품 관련 통합 테스트"""
    
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
    
    def test_artwork_creation_and_listing_workflow(self):
        """작품 생성과 목록 조회 워크플로우 테스트"""
        # 1. 작품 생성
        artwork = Artwork.objects.create(
            artist=self.artist,
            title='워크플로우 테스트 작품',
            price=5000000,
            size_number=200
        )
        
        # 2. 작품이 데이터베이스에 저장되었는지 확인
        self.assertEqual(artwork.price, 5000000)
        self.assertEqual(artwork.size_number, 200)
        self.assertEqual(artwork.artist, self.artist)
        
        # 3. 작품 목록에서 확인 가능한지 테스트
        response = self.client.get(reverse('artworks:artwork_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '워크플로우 테스트 작품')
        
        # 4. 검색 기능 테스트
        response = self.client.get(reverse('artworks:artwork_list'), {'search': '워크플로우'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '워크플로우 테스트 작품')
    
    def test_multiple_artists_artworks(self):
        """여러 작가의 작품 테스트"""
        # 두 번째 작가 생성
        artist2_user = User.objects.create_user(
            username='artist2',
            email='artist2@example.com',
            password='artist2pass123'
        )
        artist2 = Artist.objects.create(
            user=artist2_user,
            name='박작가',
            gender='여자',
            birthday=date(1985, 3, 15),
            email='artist2@example.com',
            phone_number='010-9876-5432'
        )
        
        # 첫 번째 작가의 작품
        artwork1 = Artwork.objects.create(
            artist=self.artist,
            title='김작가의 작품',
            price=1000000,
            size_number=50
        )
        
        # 두 번째 작가의 작품
        artwork2 = Artwork.objects.create(
            artist=artist2,
            title='박작가의 작품',
            price=2000000,
            size_number=100
        )
        
        # 두 작품 모두 목록에 표시되는지 확인
        response = self.client.get(reverse('artworks:artwork_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '김작가의 작품')
        self.assertContains(response, '박작가의 작품')
        
        # 각 작품이 올바른 작가에게 속하는지 확인
        self.assertEqual(artwork1.artist, self.artist)
        self.assertEqual(artwork2.artist, artist2)
