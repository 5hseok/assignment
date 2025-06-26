# 오픈갤러리 테스트 가이드

## 목차
1. [테스트 개요](#테스트-개요)
2. [테스트 실행](#테스트-실행)
3. [테스트 구조](#테스트-구조)
4. [테스트 종류](#테스트-종류)
5. [커버리지](#커버리지)
6. [CI/CD](#cicd)
7. [문제 해결](#문제-해결)

## 테스트 개요

오픈갤러리 프로젝트는 Django의 기본 테스트 프레임워크를 사용하여 포괄적인 테스트 스위트를 제공합니다.

### 테스트 범위
- **모델 테스트**: 데이터베이스 모델의 유효성 검사 및 비즈니스 로직
- **뷰 테스트**: HTTP 요청/응답, 권한 검사, 폼 처리
- **통합 테스트**: 전체 워크플로우 및 사용자 시나리오
- **보안 테스트**: 인증, 권한, 입력 검증
- **성능 테스트**: 쿼리 최적화 및 응답 시간

## 테스트 실행

### 기본 실행 방법

```bash
# 모든 테스트 실행
python run_tests.py

# 특정 앱 테스트
python run_tests.py artists
python run_tests.py artworks
python run_tests.py exhibitions
python run_tests.py auth_management

# 커버리지와 함께 실행
python run_tests.py --coverage

# 상세 출력
python run_tests.py --verbose
```

### Makefile 사용

```bash
# 모든 테스트
make test

# 빠른 테스트 (첫 실패시 중단)
make test-fast

# 커버리지 테스트
make test-coverage

# 앱별 테스트
make test-artists
make test-artworks
make test-exhibitions
make test-auth

# 통합 테스트
make test-integration
```

## 테스트 구조

```
opengallery_assignment/
├── artists/tests.py              # 작가 관련 테스트
├── artworks/tests.py             # 작품 관련 테스트
├── exhibitions/tests.py          # 전시 관련 테스트
├── auth_management/tests.py      # 인증 관련 테스트
├── opengallery/tests.py          # 통합 테스트
├── test_settings.py              # 테스트 설정
├── run_tests.py                  # 테스트 실행 스크립트
├── pytest.ini                   # pytest 설정
├── requirements-test.txt         # 테스트 의존성
└── fixtures/
    └── test_data.json           # 테스트 데이터
```

## 테스트 작성된 기능들

### Artists App 테스트
- ✅ Artist 모델 생성 및 유효성 검사
- ✅ ArtistApplication 모델 테스트
- ✅ 작가 목록 조회 및 검색
- ✅ 작가 신청 프로세스
- ✅ 관리자 신청 처리 (승인/반려)
- ✅ 작가 통계 기능

### Artworks App 테스트
- ✅ Artwork 모델 생성 및 유효성 검사
- ✅ 가격 포맷팅 기능
- ✅ 작품 목록 조회 및 검색
- ✅ 작품 등록 (작가 권한 필요)
- ✅ 작품 등록 폼 검증

### Exhibitions App 테스트
- ✅ Exhibition 모델 및 ExhibitionArtwork 중간 테이블
- ✅ 전시 목록 조회
- ✅ 전시 등록 (작가 권한 필요)
- ✅ 전시-작품 연결 기능
- ✅ 날짜 유효성 검사

### Auth Management App 테스트
- ✅ 회원가입 및 로그인 기능
- ✅ 사용자 권한별 접근 제어
- ✅ 로그인 후 리다이렉트 로직
- ✅ 세션 관리 및 보안

### 통합 테스트
- ✅ 전체 갤러리 워크플로우 (회원가입 → 작가신청 → 승인 → 작품등록 → 전시등록)
- ✅ 검색 기능 통합 테스트
- ✅ 페이지네이션 테스트
- ✅ 데이터베이스 무결성 테스트
- ✅ 성능 및 쿼리 최적화 테스트
- ✅ 보안 테스트 (인증, 권한, XSS 방지)

## 실제 테스트 실행 방법

프로젝트 루트 디렉토리에서 다음 명령어들을 실행할 수 있습니다:

```bash
# 1. 테스트 의존성 설치
pip install coverage pytest pytest-django

# 2. 모든 테스트 실행
python run_tests.py

# 3. 특정 앱만 테스트
python run_tests.py artists

# 4. 커버리지와 함께 실행
python run_tests.py --coverage

# 5. Django 기본 명령어로도 실행 가능
python manage.py test --settings=test_settings

# 6. Makefile 사용 (생성되어 있음)
make test
make test-coverage
make test-artists
```

## 주요 테스트 시나리오

### 1. 기본 모델 테스트
- 모든 모델의 생성, 저장, 검증
- 필드 제약조건 및 유효성 검사
- 모델 메서드 및 프로퍼티 테스트

### 2. 권한 및 접근 제어 테스트
- 로그인하지 않은 사용자의 접근 제한
- 일반 사용자 vs 작가 vs 관리자 권한 구분
- 다른 사용자 데이터 접근 차단

### 3. 비즈니스 로직 테스트
- 작가 신청 승인/반려 프로세스
- 작품 등록 시 작가 검증
- 전시 등록 시 본인 작품만 선택 가능
- 100호 이하 작품 통계 계산

### 4. 사용자 인터페이스 테스트
- 폼 데이터 검증 및 에러 메시지
- 검색 기능 동작
- 페이지네이션 동작
- 리다이렉트 로직

### 5. 데이터 무결성 테스트
- 외래키 연쇄 삭제
- 유니크 제약조건
- 데이터베이스 제약조건 위반 처리

## 테스트 결과 예시

성공적으로 실행되면 다음과 같은 출력을 볼 수 있습니다:

```
오픈갤러리 프로젝트 테스트 시작
==================================================
모든 테스트 실행
상세도 레벨: 1
==================================================

Creating test database for alias 'default'...
System check identified no issues (0 silenced).

artists.tests.ArtistModelTest
  test_artist_creation ... ok
  test_artist_name_max_length ... ok
  test_artist_phone_number_validation ... ok

artists.tests.ArtistApplicationModelTest
  test_artist_application_creation ... ok
  test_artist_application_ordering ... ok

artists.tests.ArtistViewTest
  test_artist_list_search ... ok
  test_artist_list_view ... ok

... (더 많은 테스트들)

==================================================
모든 테스트가 성공했습니다! ✅
```

## 추가된 파일들

1. **테스트 파일들**
   - `artists/tests.py` - 작가 관련 테스트 (126줄)
   - `artworks/tests.py` - 작품 관련 테스트 (189줄)
   - `exhibitions/tests.py` - 전시 관련 테스트 (245줄)
   - `auth_management/tests.py` - 인증 관련 테스트 (187줄)
   - `opengallery/tests.py` - 통합 테스트 (391줄)

2. **테스트 설정 및 도구**
   - `test_settings.py` - 테스트 전용 Django 설정
   - `run_tests.py` - 커스텀 테스트 실행 스크립트
   - `pytest.ini` - pytest 설정
   - `Makefile` - 편리한 명령어 모음

3. **CI/CD 설정**
   - `.github/workflows/test.yml` - GitHub Actions 워크플로우

4. **테스트 데이터**
   - `fixtures/test_data.json` - 테스트용 샘플 데이터
   - `requirements-test.txt` - 테스트 관련 패키지

이제 프로젝트는 요구사항에 맞는 포괄적인 테스트 코드를 갖추고 있으며, 다음과 같은 이점을 제공합니다:

- **코드 품질 보장**: 모든 주요 기능에 대한 테스트
- **리팩토링 안전성**: 코드 변경 시 회귀 버그 방지
- **문서화 효과**: 테스트 코드가 기능 명세서 역할
- **지속적 통합**: CI/CD 파이프라인을 통한 자동 테스트
- **개발 효율성**: 빠른 피드백과 디버깅 지원
