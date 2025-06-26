from opengallery.settings import *

# 테스트용 데이터베이스 설정
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # 메모리 데이터베이스 사용으로 빠른 테스트
    }
}

# 테스트 시 미디어 파일 처리
MEDIA_ROOT = '/tmp/test_media/'

# 테스트 시 이메일 백엔드
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# 테스트 시 캐시 비활성화
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# 테스트 시 로깅 레벨 조정
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
    },
}

# 패스워드 검증 비활성화 (테스트 속도 향상)
AUTH_PASSWORD_VALIDATORS = []

# 테스트 시 디버그 모드
DEBUG = True

# 테스트용 비밀키
SECRET_KEY = 'test-secret-key-for-testing-only'
