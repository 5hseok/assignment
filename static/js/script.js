// 전역 유틸리티 함수들

// 숫자에 천 단위 콤마 추가
function addCommas(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// 콤마 제거
function removeCommas(str) {
    return str.replace(/,/g, "");
}

// 전화번호 포맷팅
function formatPhoneNumber(phoneNumber) {
    const cleaned = phoneNumber.replace(/\D/g, "");
    if (cleaned.length === 11) {
        return cleaned.replace(/(\d{3})(\d{4})(\d{4})/, "$1-$2-$3");
    }
    return phoneNumber;
}

// 이메일 유효성 검사
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// 전화번호 유효성 검사
function validatePhoneNumber(phoneNumber) {
    const re = /^\d{3}-\d{4}-\d{4}$/;
    return re.test(phoneNumber);
}

// 날짜 유효성 검사
function validateDate(dateString) {
    const date = new Date(dateString);
    return date instanceof Date && !isNaN(date);
}

// CSRF 토큰 가져오기
function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

// AJAX 요청 헬퍼
function makeAjaxRequest(url, data, method = 'POST') {
    const formData = new FormData();
    
    if (method === 'POST') {
        formData.append('csrfmiddlewaretoken', getCSRFToken());
    }
    
    for (const [key, value] of Object.entries(data)) {
        if (Array.isArray(value)) {
            value.forEach(item => formData.append(key, item));
        } else {
            formData.append(key, value);
        }
    }
    
    return fetch(url, {
        method: method,
        body: formData
    });
}

// 로딩 스피너 표시/숨김
function showLoading(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>처리 중...';
    button.disabled = true;
    return originalText;
}

function hideLoading(button, originalText) {
    button.innerHTML = originalText;
    button.disabled = false;
}

// 성공/에러 메시지 표시
function showMessage(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('main.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // 3초 후 자동 제거
        setTimeout(() => {
            alertDiv.remove();
        }, 3000);
    }
}

// 확인 다이얼로그
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', function() {
    // 모든 알림을 3초 후 자동 제거
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 3000);
    });
    
    // 페이드인 애니메이션 적용
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in');
        }, index * 100);
    });
    
    // 뒤로 가기 버튼 이벤트
    const backButtons = document.querySelectorAll('[data-back]');
    backButtons.forEach(button => {
        button.addEventListener('click', () => {
            history.back();
        });
    });
    
    // 외부 링크 새 창에서 열기
    const externalLinks = document.querySelectorAll('a[href^="http"]:not([href*="' + window.location.hostname + '"])');
    externalLinks.forEach(link => {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
    });
});

// 가격 입력 필드 자동 포맷팅
function setupPriceFormatting() {
    const priceInputs = document.querySelectorAll('input[type="text"][data-price]');
    priceInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = removeCommas(e.target.value);
            if (!isNaN(value) && value !== '') {
                e.target.value = addCommas(parseInt(value));
            }
        });
    });
}

// 전화번호 입력 필드 자동 포맷팅
function setupPhoneFormatting() {
    const phoneInputs = document.querySelectorAll('input[type="text"][data-phone]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            e.target.value = formatPhoneNumber(e.target.value);
        });
    });
}

// 폼 유효성 검사 헬퍼
function validateForm(formElement, rules) {
    let isValid = true;
    const errors = [];
    
    for (const [fieldName, fieldRules] of Object.entries(rules)) {
        const field = formElement.querySelector(`[name="${fieldName}"]`);
        if (!field) continue;
        
        const value = field.value.trim();
        
        if (fieldRules.required && !value) {
            errors.push(`${fieldRules.label}을(를) 입력해주세요.`);
            isValid = false;
            field.classList.add('is-invalid');
            continue;
        }
        
        if (value && fieldRules.maxLength && value.length > fieldRules.maxLength) {
            errors.push(`${fieldRules.label}은(는) ${fieldRules.maxLength}자 이하여야 합니다.`);
            isValid = false;
            field.classList.add('is-invalid');
            continue;
        }
        
        if (value && fieldRules.pattern && !fieldRules.pattern.test(value)) {
            errors.push(fieldRules.message || `${fieldRules.label} 형식이 올바르지 않습니다.`);
            isValid = false;
            field.classList.add('is-invalid');
            continue;
        }
        
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    }
    
    if (!isValid) {
        showMessage(errors.join('<br>'), 'danger');
    }
    
    return isValid;
}

// 테이블 정렬 기능
function setupTableSorting() {
    const tables = document.querySelectorAll('table[data-sortable]');
    tables.forEach(table => {
        const headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                sortTable(table, header.dataset.sort);
            });
        });
    });
}

function sortTable(table, column) {
    // 테이블 정렬 로직 구현
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const columnIndex = [...table.querySelectorAll('th')].findIndex(th => th.dataset.sort === column);
    
    if (columnIndex === -1) return;
    
    const isAscending = table.dataset.sortOrder !== 'asc';
    table.dataset.sortOrder = isAscending ? 'asc' : 'desc';
    
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        const comparison = aValue.localeCompare(bValue, 'ko', { numeric: true });
        return isAscending ? comparison : -comparison;
    });
    
    rows.forEach(row => tbody.appendChild(row));
}

// 검색 기능 개선
function setupSearchEnhancements() {
    const searchInputs = document.querySelectorAll('input[type="text"][data-search]');
    searchInputs.forEach(input => {
        let timeout;
        input.addEventListener('input', function() {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                // 실시간 검색 구현 (필요시)
            }, 500);
        });
    });
}

// 무한 스크롤 (필요시 사용)
function setupInfiniteScroll(loadMoreCallback) {
    let loading = false;
    
    window.addEventListener('scroll', () => {
        if (loading) return;
        
        const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
        
        if (scrollTop + clientHeight >= scrollHeight - 5) {
            loading = true;
            loadMoreCallback().finally(() => {
                loading = false;
            });
        }
    });
}

// 로컬 스토리지 헬퍼
const Storage = {
    set(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (e) {
            console.warn('로컬 스토리지 저장 실패:', e);
        }
    },
    
    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (e) {
            console.warn('로컬 스토리지 읽기 실패:', e);
            return defaultValue;
        }
    },
    
    remove(key) {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.warn('로컬 스토리지 삭제 실패:', e);
        }
    }
};

// 페이지 성능 모니터링
if (typeof window.performance !== 'undefined') {
    window.addEventListener('load', () => {
        const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
        console.log(`페이지 로드 시간: ${loadTime}ms`);
    });
}
