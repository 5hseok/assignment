# 오픈갤러리 프로젝트 Makefile

# 변수 설정
PYTHON = python
MANAGE = $(PYTHON) manage.py
TEST_SETTINGS = --settings=test_settings

# 기본 명령어
.PHONY: help
help:
	@echo "오픈갤러리 프로젝트 명령어:"
	@echo ""
	@echo "  Development:"
	@echo "    install       - 의존성 패키지 설치"
	@echo "    migrate       - 데이터베이스 마이그레이션 실행"
	@echo "    makemigrations - 마이그레이션 파일 생성"
	@echo "    runserver     - 개발 서버 시작"
	@echo "    shell         - Django 쉘 시작"
	@echo "    createsuperuser - 슈퍼유저 생성"
	@echo ""
	@echo "  Testing:"
	@echo "    test          - 모든 테스트 실행"
	@echo "    test-fast     - 빠른 테스트 실행 (failfast)"
	@echo "    test-coverage - 커버리지와 함께 테스트 실행"
	@echo "    test-artists  - artists 앱 테스트만 실행"
	@echo "    test-artworks - artworks 앱 테스트만 실행"
	@echo "    test-exhibitions - exhibitions 앱 테스트만 실행"
	@echo "    test-auth     - auth_management 앱 테스트만 실행"
	@echo ""
	@echo "  Code Quality:"
	@echo "    lint          - 코드 스타일 검사"
	@echo "    format        - 코드 포맷팅"
	@echo "    security      - 보안 검사"
	@echo ""
	@echo "  Database:"
	@echo "    reset-db      - 데이터베이스 초기화"
	@echo "    dump-data     - 테스트 데이터 덤프"
	@echo "    load-data     - 테스트 데이터 로드"

# 개발 환경 설정
.PHONY: install
install:
	pip install -r requirements.txt
	pip install -r requirements-test.txt

.PHONY: migrate
migrate:
	$(MANAGE) migrate

.PHONY: makemigrations
makemigrations:
	$(MANAGE) makemigrations

.PHONY: runserver
runserver:
	$(MANAGE) runserver

.PHONY: shell
shell:
	$(MANAGE) shell

.PHONY: createsuperuser
createsuperuser:
	$(MANAGE) createsuperuser

# 테스트 명령어
.PHONY: test
test:
	$(PYTHON) run_tests.py --verbose

.PHONY: test-fast
test-fast:
	$(PYTHON) run_tests.py --failfast --verbose

.PHONY: test-coverage
test-coverage:
	$(PYTHON) run_tests.py --coverage --verbose

.PHONY: test-artists
test-artists:
	$(PYTHON) run_tests.py artists --verbose

.PHONY: test-artworks
test-artworks:
	$(PYTHON) run_tests.py artworks --verbose

.PHONY: test-exhibitions
test-exhibitions:
	$(PYTHON) run_tests.py exhibitions --verbose

.PHONY: test-auth
test-auth:
	$(PYTHON) run_tests.py auth_management --verbose

.PHONY: test-integration
test-integration:
	$(PYTHON) run_tests.py opengallery --verbose

# 코드 품질 검사
.PHONY: lint
lint:
	flake8 --max-line-length=100 --exclude=migrations,venv,env .
	black --check --diff --line-length=100 .
	isort --check-only --diff --line-length=100 .

.PHONY: format
format:
	black --line-length=100 .
	isort --line-length=100 .

.PHONY: security
security:
	bandit -r . -x /venv/,/env/,/migrations/
	safety check

# 데이터베이스 관리
.PHONY: reset-db
reset-db:
	rm -f db.sqlite3
	$(MANAGE) migrate
	@echo "데이터베이스가 초기화되었습니다."

.PHONY: dump-data
dump-data:
	$(MANAGE) dumpdata --natural-foreign --natural-primary \
		--exclude=contenttypes --exclude=auth.Permission \
		--exclude=sessions --exclude=admin.logentry \
		--indent=2 > fixtures/test_data.json
	@echo "테스트 데이터가 fixtures/test_data.json에 저장되었습니다."

.PHONY: load-data
load-data:
	$(MANAGE) loaddata fixtures/test_data.json
	@echo "테스트 데이터가 로드되었습니다."

# 정적 파일 관리
.PHONY: collectstatic
collectstatic:
	$(MANAGE) collectstatic --noinput

# 프로덕션 준비
.PHONY: check
check:
	$(MANAGE) check --deploy

.PHONY: check-migrations
check-migrations:
	$(MANAGE) makemigrations --check --dry-run

# 클린업
.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf htmlcov/
	rm -f .coverage
	rm -f coverage.xml
	@echo "임시 파일들이 정리되었습니다."

# 전체 CI/CD 파이프라인 시뮬레이션
.PHONY: ci
ci: lint security test-coverage
	@echo "CI/CD 파이프라인이 성공적으로 완료되었습니다!"

# 개발 환경 초기 설정
.PHONY: setup
setup: install migrate createsuperuser
	@echo "개발 환경 설정이 완료되었습니다."
	@echo "python manage.py runserver 명령어로 서버를 시작할 수 있습니다."
