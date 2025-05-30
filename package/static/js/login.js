document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password_hash');
    const togglePasswordBtn = document.querySelector('.toggle-password');
    const toast = document.getElementById('toast');
    const submitBtn = loginForm.querySelector('button[type="submit"]');

    // Toggle password visibility
    togglePasswordBtn.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password_hash';
        passwordInput.setAttribute('type', type);
        this.setAttribute('aria-label', type === 'password' ? 'Show password' : 'Hide password');
    });

    // Form validation and submission
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Reset error messages
        clearErrors();
        
        // Validate inputs
        let isValid = true;
        
        if (!emailInput.value.trim()) {
            showError('emailError', 'Email is required');
            isValid = false;
        }
        
        if (!passwordInput.value) {
            showError('passwordError', 'Password is required');
            isValid = false;
        }
        
        if (isValid) {
            await submitLogin();
        }
    });

    // Helper functions
    function showError(elementId, message) {
        const element = document.getElementById(elementId);
        element.textContent = message;
        element.setAttribute('aria-invalid', 'true');
    }

    function clearErrors() {
        const errorElements = document.querySelectorAll('.error-message');
        errorElements.forEach(element => {
            element.textContent = '';
            element.removeAttribute('aria-invalid');
        });
    }

    function showToast(message, isSuccess = true) {
        toast.textContent = message;
        toast.style.backgroundColor = isSuccess ? 'var(--success-color)' : 'var(--error-color)';
        toast.classList.add('show');
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 5000);
    }

    async function submitLogin() {
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Logging In <span class="loading-spinner"></span>';
        
        try {
            const formData = {
                email: emailInput.value.trim(),
                password_hash: passwordInput.value
            };
            
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(formData),
                credentials: 'include'
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.message || 'Login failed');
            }
            
            // On successful login
            showToast('Login successful! Redirecting...');
            
            
            // Redirect based on user role (would come from JWT in your actual implementation)
            setTimeout(() => {
                window.location.href = '/dashboard'; // Or role-based redirect
            }, 1500);
            
        } catch (error) {
            console.error('Login error:', error);
            
            if (error.message.toLowerCase().includes('email')) {
                showError('emailError', error.message);
            } else if (error.message.toLowerCase().includes('password_hash')) {
                showError('passwordError', error.message);
            } else {
                showToast(error.message || 'An error occurred during login', false);
            }
            
            // Reset form state
            submitBtn.disabled = false;
            submitBtn.textContent = 'Log In';
        }
    }


});