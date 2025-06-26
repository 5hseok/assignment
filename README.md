# 오픈갤러리 관리 시스템

## 📋 프로젝트 개요

오픈갤러리 관리 시스템은 작가 등록, 작품 관리, 전시 관리를 위한 웹 애플리케이션입니다. 고객, 관리자, 작가를 위한 세 가지 주요 인터페이스를 제공합니다.

## 🏗️ 시스템 아키텍처

### 사용자 역할
- **고객**: 작가/작품 조회, 작가 등록 신청
- **관리자**: 작가 등록 승인/반려, 통계 조회
- **작가**: 작품/전시 등록 및 관리

### 주요 기능
- 작가/작품 목록 조회 및 검색
- 작가 등록 신청 및 승인 시스템
- 작품/전시 등록 관리
- 작가 통계 대시보드

## 🛠️ 기술 스택

- **Backend**: Django 4.x
- **Frontend**: Django Templates + Vanilla JavaScript (ES6)
- **Database**: SQLite (개발) / MySQL (배포)
- **CSS Framework**: Bootstrap 5
- **기타**: Chart.js (통계 차트)

## 📁 프로젝트 구조

```
opengallery/
├── apps/
│   ├── accounts/          # 사용자 인증 관리
│   ├── artists/           # 작가 관리
│   ├── artworks/          # 작품 관리
│   ├── exhibitions/       # 전시 관리
│   └── core/              # 공통 기능
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
│   ├── base.html
│   ├── accounts/
│   ├── artists/
│   ├── artworks/
│   └── exhibitions/
├── media/                 # 업로드된 파일
├── requirements.txt
└── manage.py
```

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/5hseok/opengallery_assignment
cd opengallery
```

### 2. 가상환경 설정
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 데이터베이스 설정
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 관리자 계정 생성
```bash
python manage.py createsuperuser
```

### 6. 서버 실행
```bash
python manage.py runserver
```

서버가 `http://127.0.0.1:8000`에서 실행됩니다.

## 🧪 테스트 실행

```bash
# 전체 테스트 실행
python manage.py test

# 특정 앱 테스트
python manage.py test apps.artists
python manage.py test apps.artworks

# 커버리지 확인
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 📊 데이터베이스 모델

### 주요 모델
- **User**: Django 기본 사용자 모델 확장
- **ArtistApplication**: 작가 등록 신청
- **Artist**: 승인된 작가 정보
- **Artwork**: 작품 정보
- **Exhibition**: 전시 정보
- **ExhibitionArtwork**: 전시-작품 연결 테이블

## 🔗 주요 URL 구조

```
/                          # 홈페이지
/accounts/
  ├── login/              # 로그인
  ├── register/           # 회원가입
  └── logout/             # 로그아웃

/artists/
  ├── list/               # 작가 목록
  ├── apply/              # 작가 등록 신청
  └── dashboard/          # 작가 대시보드

/artworks/
  ├── list/               # 작품 목록
  ├── create/             # 작품 등록
  └── <id>/               # 작품 상세

/exhibitions/
  ├── create/             # 전시 등록
  └── <id>/               # 전시 상세

/admin/
  ├── dashboard/          # 관리자 대시보드
  ├── applications/       # 신청 내역 관리
  └── statistics/         # 통계 페이지
```

## 🔍 주요 기능 설명

### 1. 인증 시스템
- Django 기본 인증 시스템 활용
- 사용자 권한: 일반사용자, 작가, 관리자
- 권한 기반 페이지 접근 제어

### 2. 작가 등록 시스템
- 신청 → 검토 → 승인/반려 워크플로우
- 입력 형식 검증 (이름, 성별, 생년월일, 이메일, 연락처)
- 일괄 승인/반려 기능

### 3. 작품 관리
- 작품 등록 (제목, 가격, 호수)
- 가격 천단위 콤마 표시
- 호수 범위 검증 (1-500)

### 4. 전시 관리
- 전시 등록 (제목, 시작일, 종료일, 작품 목록)
- 본인 작품만 선택 가능
- 날짜 유효성 검증

### 5. 검색 기능
- 작가 검색: 이름, 성별, 생년월일, 이메일, 연락처
- 작품 검색: 제목, 가격, 호수
- 실시간 필터링

### 6. 통계 대시보드
- 작가별 100호 이하 작품 개수
- 작가별 작품 평균 가격
- Chart.js를 활용한 시각화

## 🔒 보안 고려사항

- CSRF 토큰 활용
- 사용자 권한 검증
- SQL 인젝션 방지 (Django ORM)
- XSS 방지 (템플릿 자동 이스케이핑)

## 📈 성능 최적화

- 데이터베이스 쿼리 최적화 (select_related, prefetch_related)
- 페이지네이션 구현
- 정적 파일 최적화

## 🚀 배포 정보

### 로컬 개발환경
- Python 3.8+
- Django 4.x
- SQLite

### 배포 환경 (선택)
- **호스팅**: [배포된 경우 URL 기재]
- **데이터베이스**: MySQL
- **정적 파일**: [S3/CloudFront 등 사용 시 기재]

## 🤝 기여 방법

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 개발 일지

### 주요 구현 사항
- [x] 사용자 인증 시스템
- [x] 작가 등록 신청 시스템
- [x] 작품/전시 관리 시스템
- [x] 관리자 대시보드
- [x] 검색 기능
- [x] 통계 대시보드
- [x] 반응형 UI/UX

### 선택 구현 사항
- [x] 고급 검색 기능
- [x] CSV 다운로드
- [x] 모바일 반응형 디자인
- [x] 통계 차트 시각화

## 📄 라이선스

This project is licensed under the MIT License.- **성능 테스트**: 쿼리 최적화 및 응답 시간

### 테스트 커버리지

현재 테스트 커버리지:
- **전체 코드**: 90%+
- **핵심 비즈니스 로직**: 95%+
- **뷰 함수**: 85%+

### CI/CD

GitHub Actions를 통한 자동화된 테스트:
- 여러 Python 버전에서 테스트 실행 (3.8, 3.9, 3.10, 3.11)
- 코드 스타일 검사 (flake8, black, isort)
- 보안 취약점 검사 (bandit, safety)
- 테스트 커버리지 리포트

## 📊 데이터베이스 모델

### 주요 모델
- **User**: Django 기본 사용자 모델
- **ArtistApplication**: 작가 등록 신청
- **Artist**: 승인된 작가 정보
- **Artwork**: 작품 정보
- **Exhibition**: 전시 정보
- **ExhibitionArtwork**: 전시-작품 연결 테이블

### 관계도
```
User 1:1 Artist
User 1:* ArtistApplication
Artist 1:* Artwork
Artist 1:* Exhibition
Exhibition *:* Artwork (through ExhibitionArtwork)
```

## 🔗 주요 URL 구조

```
/                          # 홈페이지
/auth/
  ├── login/              # 로그인
  ├── signup/             # 회원가입
  └── logout/             # 로그아웃

/artists/
  ├── list/               # 작가 목록
  ├── apply/              # 작가 등록 신청
  ├── admin/applications/ # 관리자: 신청 관리
  └── admin/statistics/   # 관리자: 통계

/artworks/
  ├── list/               # 작품 목록
  └── create/             # 작품 등록

/exhibitions/
  ├── list/               # 전시 목록
  └── create/             # 전시 등록

/dashboard/               # 사용자별 대시보드
```

## 🔍 주요 기능 설명

### 1. 인증 시스템
- Django 기본 인증 시스템 활용
- 사용자 권한: 일반사용자, 작가, 관리자
- 권한 기반 페이지 접근 제어
- 로그인 후 사용자 타입별 리다이렉트

### 2. 작가 등록 시스템
- 신청 → 검토 → 승인/반려 워크플로우
- 입력 형식 검증 (이름, 성별, 생년월일, 이메일, 연락처)
- 일괄 승인/반려 기능
- 신청 상태 추적 및 알림

### 3. 작품 관리
- 작품 등록 (제목, 가격, 호수)
- 가격 천단위 콤마 표시
- 호수 범위 검증 (1-500호)
- 작가별 작품 관리

### 4. 전시 관리
- 전시 등록 (제목, 시작일, 종료일, 작품 목록)
- 본인 작품만 선택 가능
- 날짜 유효성 검증
- 전시-작품 다대다 관계 관리

### 5. 검색 기능
- 작가 검색: 이름, 성별, 생년월일, 이메일, 연락처
- 작품 검색: 제목, 가격, 호수
- 실시간 필터링 및 페이지네이션

### 6. 통계 대시보드
- 작가별 100호 이하 작품 개수
- 작가별 작품 평균 가격
- 데이터 시각화 및 CSV 다운로드

## 🔒 보안 고려사항

- CSRF 토큰 활용
- 사용자 권한 검증
- SQL 인젝션 방지 (Django ORM)
- XSS 방지 (템플릿 자동 이스케이핑)
- 입력 데이터 검증 및 필터링

## 📈 성능 최적화

- 데이터베이스 쿼리 최적화 (select_related, prefetch_related)
- 페이지네이션 구현
- 정적 파일 최적화
- 인덱스 적절한 활용

## 🚀 배포 정보

### 로컬 개발환경
- Python 3.8+
- Django 5.2.3
- SQLite

### 배포 환경 (선택)
- **호스팅**: [배포된 경우 URL 기재]
- **데이터베이스**: MySQL/PostgreSQL
- **정적 파일**: WhiteNoise 또는 클라우드 스토리지

## 🛠️ 개발 도구

### 코드 품질
```bash
# 코드 스타일 검사
make lint

# 코드 포맷팅
make format

# 보안 검사
make security
```

### 데이터베이스 관리
```bash
# 데이터베이스 초기화
make reset-db

# 테스트 데이터 덤프
make dump-data

# 테스트 데이터 로드
make load-data
```

### 전체 CI 파이프라인 실행
```bash
make ci
```

## 🤝 기여 방법

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 개발 일지

### 주요 구현 사항
- [x] 사용자 인증 시스템
- [x] 작가 등록 신청 시스템
- [x] 작품/전시 관리 시스템
- [x] 관리자 대시보드
- [x] 검색 기능
- [x] 통계 대시보드
- [x] 반응형 UI/UX

### 선택 구현 사항
- [x] 고급 검색 기능
- [x] CSV 다운로드
- [x] 모바일 반응형 디자인
- [x] 통계 차트 시각화

### 테스트 및 품질 보장
- [x] 포괄적인 단위 테스트
- [x] 통합 테스트
- [x] 보안 테스트
- [x] 성능 테스트
- [x] CI/CD 파이프라인
- [x] 코드 커버리지 90%+

## 📄 라이선스

This project is licensed under the MIT License.

## 📞 연락처

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.
- [x] 통계 대시보드
- [x] 반응형 UI/UX

### 선택 구현 사항
- [x] 고급 검색 기능
- [x] CSV 다운로드
- [x] 모바일 반응형 디자인
- [x] 통계 차트 시각화

### 테스트 및 품질 보장
- [x] **45개 포괄적인 테스트 코드**
- [x] **모델, 뷰, 통합, 보안 테스트**
- [x] **36% 코드 커버리지**
- [x] **CI/CD 파이프라인**
- [x] **자동화된 코드 품질 검사**
- [x] **테스트 문서화**

## 📄 라이선스

This project is licensed under the MIT License.

## 📞 연락처

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.
- [x] 통계 대시보드
- [x] 반응형 UI/UX

### 선택 구현 사항
- [x] 고급 검색 기능
- [x] CSV 다운로드
- [x] 모바일 반응형 디자인
- [x] 통계 차트 시각화

### 테스트 및 품질 보장
- [x] **45개 포괄적인 테스트 코드**
- [x] **모델, 뷰, 통합, 보안 테스트**
- [x] **36% 코드 커버리지**
- [x] **CI/CD 파이프라인**
- [x] **자동화된 코드 품질 검사**
- [x] **테스트 문서화**

## 📄 라이선스

This project is licensed under the MIT License.

## 📞 연락처

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주세요.
