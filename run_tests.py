#!/usr/bin/env python
"""
오픈갤러리 프로젝트 테스트 실행 스크립트

사용법:
    python run_tests.py                     # 모든 테스트 실행
    python run_tests.py artists             # artists 앱 테스트만 실행
    python run_tests.py --coverage          # 커버리지와 함께 실행
    python run_tests.py --verbose           # 상세 출력
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner
import argparse


def setup_test_environment():
    """테스트 환경 설정"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')
    django.setup()


def run_tests(test_labels=None, verbosity=1, interactive=False, keepdb=False):
    """테스트 실행"""
    TestRunner = get_runner(settings)
    test_runner = TestRunner(
        verbosity=verbosity,
        interactive=interactive,
        keepdb=keepdb
    )
    
    failures = test_runner.run_tests(test_labels or [])
    return failures


def run_with_coverage(test_labels=None, verbosity=1):
    """커버리지와 함께 테스트 실행"""
    try:
        import coverage
    except ImportError:
        print("커버리지를 사용하려면 coverage 패키지를 설치해야 합니다:")
        print("pip install coverage")
        return 1
    
    # 커버리지 설정
    cov = coverage.Coverage(
        source=['artists', 'artworks', 'exhibitions', 'auth_management', 'opengallery'],
        omit=[
            '*/migrations/*',
            '*/tests.py',
            '*/test_*.py',
            '*/venv/*',
            '*/virtualenv/*',
            'manage.py',
            'test_settings.py',
            'run_tests.py'
        ]
    )
    
    cov.start()
    
    # 테스트 실행
    failures = run_tests(test_labels, verbosity)
    
    cov.stop()
    cov.save()
    
    # 커버리지 리포트 출력
    print("\n" + "="*50)
    print("커버리지 리포트")
    print("="*50)
    cov.report()
    
    # HTML 리포트 생성
    try:
        cov.html_report(directory='htmlcov')
        print(f"\nHTML 커버리지 리포트가 'htmlcov/index.html'에 생성되었습니다.")
    except Exception as e:
        print(f"HTML 리포트 생성 실패: {e}")
    
    return failures


def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='오픈갤러리 테스트 실행')
    parser.add_argument(
        'test_labels',
        nargs='*',
        help='실행할 테스트 앱 또는 테스트 클래스 (예: artists, artists.tests.ArtistModelTest)'
    )
    parser.add_argument(
        '--coverage', '-c',
        action='store_true',
        help='커버리지와 함께 테스트 실행'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='count',
        default=1,
        help='상세 출력 레벨 (최대 3회까지 사용 가능: -v, -vv, -vvv)'
    )
    parser.add_argument(
        '--keepdb', '-k',
        action='store_true',
        help='테스트 데이터베이스 유지 (다음 테스트에서 재사용)'
    )
    parser.add_argument(
        '--failfast', '-f',
        action='store_true',
        help='첫 번째 실패 시 테스트 중단'
    )
    
    args = parser.parse_args()
    
    # 테스트 환경 설정
    setup_test_environment()
    
    # 실패 시 빠른 종료 설정
    if args.failfast:
        os.environ['DJANGO_TEST_FAILFAST'] = '1'
    
    print("오픈갤러리 프로젝트 테스트 시작")
    print("="*50)
    
    if args.test_labels:
        print(f"테스트 대상: {', '.join(args.test_labels)}")
    else:
        print("모든 테스트 실행")
    
    print(f"상세도 레벨: {args.verbose}")
    
    if args.coverage:
        print("커버리지 측정 활성화")
    
    print("="*50)
    
    # 테스트 실행
    if args.coverage:
        failures = run_with_coverage(args.test_labels, args.verbose)
    else:
        failures = run_tests(
            args.test_labels,
            verbosity=args.verbose,
            keepdb=args.keepdb
        )
    
    # 결과 출력
    print("\n" + "="*50)
    if failures:
        print(f"테스트 실패: {failures}개의 테스트가 실패했습니다.")
        sys.exit(1)
    else:
        print("모든 테스트가 성공했습니다! ✅")
        sys.exit(0)


if __name__ == '__main__':
    main()
