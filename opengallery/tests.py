from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.management import call_command
from django.db import transaction
from datetime import date, timedelta
from artists.models import Artist, ArtistApplication
from artworks.models import Artwork
from exhibitions.models import Exhibition, ExhibitionArtwork
import io
import sys


class ProjectIntegrationTest(TestCase):
    """프로젝트 전체 통합 테스트"""
    
    def setUp(self):
        self.client = Client()
        # 일반 사용자
        self.user = User.objects.create_user(
            username='customer',
            email='customer@example.com',
            password='customerpass123'
        )
        # 작가 사용자
        self.artist_user = User.objects.create_user(
            username='artist',
            email='artist@example.com',
            password='artistpass123'
        )
        # 관리자 사용자
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
    
    def test_basic_page_access(self):
        """기본 페이지 접근 테스트"""
        # 홈페이지
        response = self.client.get('/')
        self.assertIn(response.status_code, [200, 302])
        
        # 작가 목록
        response = self.client.get(reverse('artists:artist_list'))
        self.assertEqual(response.status_code, 200)
        
        # 작품 목록
        response = self.client.get(reverse('artworks:artwork_list'))
        self.assertEqual(response.status_code, 200)
        
        # 전시 목록
        response = self.client.get(reverse('exhibitions:exhibition_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_search_functionality(self):
        """검색 기능 통합 테스트"""
        # 테스트 데이터 생성
        artist = Artist.objects.create(
            user=self.artist_user,
            name='검색테스트작가',
            gender='여자',
            birthday=date(1988, 3, 20),
            email='searchtest@example.com',
            phone_number='010-7777-8888'
        )
        
        artwork = Artwork.objects.create(
            artist=artist,
            title='검색테스트작품',
            price=2500000,
            size_number=80
        )
        
        # 작가 검색
        response = self.client.get(reverse('artists:artist_list'), {'search': '검색테스트'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '검색테스트작가')
        
        # 작품 검색
        response = self.client.get(reverse('artworks:artwork_list'), {'search': '검색테스트'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '검색테스트작품')
        
        # 없는 키워드 검색
        response = self.client.get(reverse('artists:artist_list'), {'search': '없는키워드'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '검색테스트작가')


class DatabaseIntegrityTest(TestCase):
    """데이터베이스 무결성 테스트"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.artist = Artist.objects.create(
            user=self.user,
            name='테스트작가',
            gender='남자',
            birthday=date(1990, 1, 1),
            email='test@example.com',
            phone_number='010-1234-5678'
        )
    
    def test_cascade_deletion(self):
        """연쇄 삭제 테스트"""
        # 작품 생성
        artwork = Artwork.objects.create(
            artist=self.artist,
            title='테스트 작품',
            price=1000000,
            size_number=50
        )
        
        # 전시 생성
        exhibition = Exhibition.objects.create(
            artist=self.artist,
            title='테스트 전시',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30)
        )
        
        # 전시-작품 연결
        ExhibitionArtwork.objects.create(
            exhibition=exhibition,
            artwork=artwork
        )
        
        # 사용자 삭제 시 모든 관련 데이터가 삭제되는지 확인
        user_id = self.user.id
        artwork_id = artwork.id
        exhibition_id = exhibition.id
        
        self.user.delete()
        
        # 관련 객체들이 모두 삭제되었는지 확인
        self.assertFalse(Artist.objects.filter(user_id=user_id).exists())
        self.assertFalse(Artwork.objects.filter(id=artwork_id).exists())
        self.assertFalse(Exhibition.objects.filter(id=exhibition_id).exists())
        self.assertFalse(ExhibitionArtwork.objects.filter(artwork_id=artwork_id).exists())
    
    def test_foreign_key_constraints(self):
        """외래키 제약조건 테스트"""
        artwork = Artwork.objects.create(
            artist=self.artist,
            title='테스트 작품',
            price=1000000,
            size_number=50
        )
        
        # 작가를 삭제하면 작품도 함께 삭제되어야 함
        artist_id = self.artist.id
        artwork_id = artwork.id
        
        self.artist.delete()
        
        self.assertFalse(Artwork.objects.filter(id=artwork_id).exists())


class PerformanceTest(TestCase):
    """성능 테스트"""
    
    def setUp(self):
        # 테스트용 데이터 생성
        self.users = []
        self.artists = []
        
        for i in range(5):
            user = User.objects.create_user(
                username=f'perftest{i}',
                email=f'perftest{i}@example.com',
                password='pass123'
            )
            artist = Artist.objects.create(
                user=user,
                name=f'성능테스트작가{i}',
                gender='남자' if i % 2 == 0 else '여자',
                birthday=date(1980 + i, 1, 1),
                email=f'perftest{i}@example.com',
                phone_number=f'010-{1000+i:04d}-{2000+i:04d}'
            )
            self.users.append(user)
            self.artists.append(artist)
            
            # 각 작가당 3개의 작품 생성
            for j in range(3):
                Artwork.objects.create(
                    artist=artist,
                    title=f'작가{i}_작품{j}',
                    price=(j + 1) * 1000000,
                    size_number=(j + 1) * 20
                )
    
    def test_query_performance(self):
        """쿼리 성능 테스트"""
        # 작가 목록 조회
        response = self.client.get(reverse('artists:artist_list'))
        self.assertEqual(response.status_code, 200)
        
        # 작품 목록 조회
        response = self.client.get(reverse('artworks:artwork_list'))
        self.assertEqual(response.status_code, 200)
        
        # 전시 목록 조회
        response = self.client.get(reverse('exhibitions:exhibition_list'))
        self.assertEqual(response.status_code, 200)


class ErrorHandlingTest(TestCase):
    """에러 처리 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.artist = Artist.objects.create(
            user=self.user,
            name='테스트작가',
            gender='남자',
            birthday=date(1990, 1, 1),
            email='test@example.com',
            phone_number='010-1234-5678'
        )
    
    def test_404_handling(self):
        """404 에러 처리 테스트"""
        # 존재하지 않는 페이지 조회
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)
    
    def test_permission_denied_handling(self):
        """권한 거부 처리 테스트"""
        # 로그인하지 않고 보호된 페이지 접근
        response = self.client.get('/admin/dashboard/')
        self.assertIn(response.status_code, [302, 404])


class SecurityTest(TestCase):
    """보안 테스트"""
    
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
            name='테스트작가',
            gender='남자',
            birthday=date(1990, 1, 1),
            email='artist@example.com',
            phone_number='010-1234-5678'
        )
    
    def test_user_isolation(self):
        """사용자 격리 테스트"""
        # 작가A의 작품
        artwork_a = Artwork.objects.create(
            artist=self.artist,
            title='작가A의 작품',
            price=1000000,
            size_number=50
        )
        
        # 다른 사용자로 로그인
        self.client.login(username='testuser', password='testpass123')
        
        # 다른 사용자는 작가A의 작품을 수정할 수 없어야 함
        response = self.client.get(f'/artworks/{artwork_a.id}/edit/')
        self.assertIn(response.status_code, [403, 404])
    
    def test_authentication_required(self):
        """인증 필요 테스트"""
        # 로그인 페이지 접근은 가능
        response = self.client.get(reverse('auth_management:login'))
        self.assertEqual(response.status_code, 200)
        
        # 회원가입 페이지 접근은 가능
        response = self.client.get(reverse('auth_management:signup'))
        self.assertEqual(response.status_code, 200)


class APIConsistencyTest(TestCase):
    """API 일관성 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_url_patterns(self):
        """URL 패턴 일관성 테스트"""
        # 모든 주요 URL이 올바르게 작동하는지 확인
        urls_to_test = [
            reverse('artists:artist_list'),
            reverse('artworks:artwork_list'),
            reverse('exhibitions:exhibition_list'),
            reverse('auth_management:login'),
            reverse('auth_management:signup'),
        ]
        
        for url in urls_to_test:
            response = self.client.get(url)
            # 200 (정상) 또는 302 (리다이렉트)여야 함
            self.assertIn(response.status_code, [200, 302], 
                         f"URL {url}에서 예상치 못한 상태 코드: {response.status_code}")
    
    def test_response_formats(self):
        """응답 형식 일관성 테스트"""
        # HTML 응답이 올바른 형식인지 확인
        response = self.client.get(reverse('artists:artist_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
    
    def test_error_response_consistency(self):
        """에러 응답 일관성 테스트"""
        # 404 에러 페이지
        response = self.client.get('/nonexistent-page/')
        self.assertEqual(response.status_code, 404)


class MigrationTest(TestCase):
    """마이그레이션 테스트"""
    
    def test_migration_status(self):
        """마이그레이션 상태 확인"""
        from django.core.management import call_command
        from io import StringIO
        
        # 마이그레이션 상태 확인
        out = StringIO()
        call_command('showmigrations', '--list', stdout=out)
        output = out.getvalue()
        
        # 출력이 있는지 확인 (마이그레이션이 존재함)
        self.assertTrue(len(output) > 0)
