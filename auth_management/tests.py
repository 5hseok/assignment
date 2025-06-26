from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate
from artists.models import Artist
from datetime import date


class AuthViewTest(TestCase):
    """인증 관련 뷰 테스트"""
    
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
    
    def test_signup_view_get(self):
        """회원가입 페이지 GET 요청 테스트"""
        response = self.client.get(reverse('auth_management:signup'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '회원가입')
    
    def test_login_view_get(self):
        """로그인 페이지 GET 요청 테스트"""
        response = self.client.get(reverse('auth_management:login'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '로그인')
    
    def test_login_view_post_valid(self):
        """로그인 POST 요청 성공 테스트"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(reverse('auth_management:login'), data)
        
        # 로그인 성공 시 리다이렉트
        self.assertEqual(response.status_code, 302)
        
        # 로그인이 되었는지 확인
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)
    
    def test_login_view_post_invalid(self):
        """로그인 POST 요청 실패 테스트"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(reverse('auth_management:login'), data)
        
        # 로그인 실패 시 다시 페이지 렌더링
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '사용자명 또는 비밀번호가 잘못되었습니다')
    
    def test_logout_view(self):
        """로그아웃 테스트"""
        # 먼저 로그인
        self.client.login(username='testuser', password='testpass123')
        
        # 로그아웃
        response = self.client.get(reverse('auth_management:logout'))
        
        # 로그아웃 후 리다이렉트
        self.assertEqual(response.status_code, 302)
        
        # 세션에서 사용자 정보가 삭제되었는지 확인
        self.assertNotIn('_auth_user_id', self.client.session)


class AuthIntegrationTest(TestCase):
    """인증 관련 통합 테스트"""
    
    def setUp(self):
        self.client = Client()
    
    def test_signup_and_login_workflow(self):
        """회원가입과 로그인 전체 워크플로우 테스트"""
        # 1. 회원가입
        signup_data = {
            'username': 'workflow_user',
            'email': 'workflow@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        
        response = self.client.post(reverse('auth_management:signup'), signup_data)
        self.assertEqual(response.status_code, 302)
        
        # 2. 사용자가 생성되었는지 확인
        user = User.objects.get(username='workflow_user')
        self.assertIsNotNone(user)
        
        # 3. 로그인
        login_data = {
            'username': 'workflow_user',
            'password': 'complexpass123'
        }
        
        response = self.client.post(reverse('auth_management:login'), login_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)


class UserPermissionTest(TestCase):
    """사용자 권한 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='regularpass123'
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
    
    def test_regular_user_permissions(self):
        """일반 사용자 권한 테스트"""
        self.client.login(username='regular', password='regularpass123')
        
        # 일반 사용자는 작품 목록, 작가 목록 조회 가능
        response = self.client.get(reverse('artworks:artwork_list'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('artists:artist_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_artist_permissions(self):
        """작가 권한 테스트"""
        self.client.login(username='artist', password='artistpass123')
        
        # 작가는 작품 목록 조회 가능
        response = self.client.get(reverse('artworks:artwork_list'))
        self.assertEqual(response.status_code, 200)
        
        # 작가는 전시 목록 조회 가능
        response = self.client.get(reverse('exhibitions:exhibition_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_permissions(self):
        """관리자 권한 테스트"""
        self.client.login(username='admin', password='adminpass123')
        
        # 관리자는 모든 페이지 접근 가능
        response = self.client.get(reverse('artists:artist_list'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('artworks:artwork_list'))
        self.assertEqual(response.status_code, 200)


class AuthSecurityTest(TestCase):
    """인증 보안 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_password_authentication(self):
        """비밀번호 인증 테스트"""
        # 올바른 비밀번호
        user = authenticate(username='testuser', password='testpass123')
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)
        
        # 잘못된 비밀번호
        user = authenticate(username='testuser', password='wrongpassword')
        self.assertIsNone(user)
    
    def test_session_security(self):
        """세션 보안 테스트"""
        # 로그인
        self.client.login(username='testuser', password='testpass123')
        
        # 세션에 사용자 ID가 저장되었는지 확��
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)
        
        # 로그아웃 후 세션 정리 확인
        self.client.logout()
        self.assertNotIn('_auth_user_id', self.client.session)
        self.client = Client()
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='regularpass123'
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
    
    def test_regular_user_permissions(self):
        """일반 사용자 권한 테스트"""
        self.client.login(username='regular', password='regularpass123')
        
        # 일반 사용자는 작품 목록, 작가 목록 조회 가능
        response = self.client.get(reverse('artworks:artwork_list'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('artists:artist_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_artist_permissions(self):
        """작가 권한 테스트"""
        self.client.login(username='artist', password='artistpass123')
        
        # 작가는 작품 목록 조회 가능
        response = self.client.get(reverse('artworks:artwork_list'))
        self.assertEqual(response.status_code, 200)
        
        # 작가는 전시 목록 조회 가능
        response = self.client.get(reverse('exhibitions:exhibition_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_admin_permissions(self):
        """관리자 권한 테스트"""
        self.client.login(username='admin', password='adminpass123')
        
        # 관리자는 모든 페이지 접근 가능
        response = self.client.get(reverse('artists:artist_list'))
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(reverse('artworks:artwork_list'))
        self.assertEqual(response.status_code, 200)


class AuthSecurityTest(TestCase):
    """인증 보안 테스트"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_password_authentication(self):
        """비밀번호 인증 테스트"""
        # 올바른 비밀번호
        user = authenticate(username='testuser', password='testpass123')
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)
        
        # 잘못된 비밀번호
        user = authenticate(username='testuser', password='wrongpassword')
        self.assertIsNone(user)
    
    def test_session_security(self):
        """세션 보안 테스트"""
        # 로그인
        self.client.login(username='testuser', password='testpass123')
        
        # 세션에 사용자 ID가 저장되었는지 확인
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)
        
        # 로그아웃 후 세션 정리 확인
        self.client.logout()
        self.assertNotIn('_auth_user_id', self.client.session)
