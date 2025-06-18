function showNotification(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="toast-header bg-${type === 'success' ? 'success' : 'danger'} text-white">
            <strong class="me-auto">${type === 'success' ? 'Success' : 'Error'}</strong>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">${message}</div>
    `;
    document.querySelector('.toast-container').appendChild(toast);
    const bsToast = new bootstrap.Toast(toast, { delay: 3000 });
    bsToast.show();
}

function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.querySelector('.password-toggle');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

function toggleSignupPassword() {
    const passwordInput = document.getElementById('signupPassword');
    const toggleIcon = passwordInput.parentElement.querySelector('.password-toggle');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordInput.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

function toggleForms(formType) {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    const title = document.getElementById('formTitle');
    const subtitle = document.getElementById('formSubtitle');
    const buttons = document.querySelectorAll('.btn-group .btn');

    if (formType === 'login') {
        loginForm.classList.remove('d-none');
        signupForm.classList.add('d-none');
        title.textContent = 'Welcome Back!';
        subtitle.textContent = 'Please login to continue';
        buttons[0].classList.add('active');
        buttons[1].classList.remove('active');
    } else {
        loginForm.classList.add('d-none');
        signupForm.classList.remove('d-none');
        title.textContent = 'Create Account';
        subtitle.textContent = 'Please fill in your details';
        buttons[0].classList.remove('active');
        buttons[1].classList.add('active');
    }
}

async function handleLogin(event) {
    event.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const rememberMe = document.getElementById('rememberMe').checked;
    
    const button = event.target.querySelector('button');
    const buttonText = button.querySelector('.login-text');
    const spinner = button.querySelector('.spinner-border');
    
    // Show loading state
    button.disabled = true;
    buttonText.style.opacity = '0';
    spinner.classList.remove('d-none');
    
    try {
        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password, rememberMe })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification('Login successful');
            // Add returnUrl handling
            const params = new URLSearchParams(window.location.search);
            const returnUrl = params.get('next') || '/';
            window.location.href = returnUrl;
        } else {
            throw new Error(data.message || 'Login failed');
        }
    } catch (error) {
        showNotification(error.message, 'error');
    } finally {
        // Reset button state
        button.disabled = false;
        buttonText.style.opacity = '1';
        spinner.classList.add('d-none');
    }
}

async function handleSignup(event) {
    event.preventDefault();
    
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        showNotification('Passwords do not match', 'error');
        return;
    }

    const button = event.target.querySelector('button');
    const buttonText = button.querySelector('.login-text');
    const spinner = button.querySelector('.spinner-border');
    
    button.disabled = true;
    buttonText.style.opacity = '0';
    spinner.classList.remove('d-none');
    
    try {
        const response = await fetch('/api/auth/signup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification('Account created successfully');
            toggleForms('login');
        } else {
            throw new Error(data.message || 'Signup failed');
        }
    } catch (error) {
        showNotification(error.message, 'error');
    } finally {
        button.disabled = false;
        buttonText.style.opacity = '1';
        spinner.classList.add('d-none');
    }
}

// Add function to check auth status on page load
function checkAuthStatus() {
    fetch('/api/auth/check-auth')
        .then(response => {
            if (!response.ok && window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        })
        .catch(() => {
            if (window.location.pathname !== '/login') {
                window.location.href = '/login';
            }
        });
}

// Add event listener for page load
document.addEventListener('DOMContentLoaded', checkAuthStatus);
