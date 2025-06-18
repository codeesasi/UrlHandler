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
            // Redirect to main page after successful login
            window.location.href = '/';
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
