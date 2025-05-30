document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signupForm');
    const usernameInput = document.getElementById('username');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password_hash');
    const roleInput = document.getElementById('role');
    const togglePasswordBtn = document.querySelector('.toggle-password');
    const passwordStrengthBar = document.getElementById('passwordStrength');
    const passwordStrengthText = document.getElementById('passwordStrengthText');
    const toast = document.getElementById('toast');

    // Check if current user is admin (placeholder - actual implementation would check JWT)
    const isAdmin = false; // This would normally come from a secure source

    // If not admin, remove the admin option from role dropdown
    if (!isAdmin) {
        const adminOption = roleInput.querySelector('option[value="admin"]');
        if (adminOption) {
            adminOption.remove();
        }
    }

    // Toggle password visibility
    togglePasswordBtn.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        this.setAttribute('aria-label', type === 'password' ? 'Show password' : 'Hide password');
    });

    // Password strength indicator
    passwordInput.addEventListener('input', function() {
        const strength = calculatePasswordStrength(this.value);
        passwordStrengthBar.value = strength;
        
        switch(strength) {
            case 0:
            case 1:
                passwordStrengthText.textContent = 'Weak';
                passwordStrengthBar.style.setProperty('--progress-color', '#e74c3c');
                break;
            case 2:
                passwordStrengthText.textContent = 'Fair';
                passwordStrengthBar.style.setProperty('--progress-color', '#f39c12');
                break;
            case 3:
                passwordStrengthText.textContent = 'Good';
                passwordStrengthBar.style.setProperty('--progress-color', '#f1c40f');
                break;
            case 4:
                passwordStrengthText.textContent = 'Strong';
                passwordStrengthBar.style.setProperty('--progress-color', '#2ecc71');
                break;
        }
    });

    // Form validation
    signupForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Reset error messages
        clearErrors();
        
        // Validate inputs
        let isValid = true;
        
        // Username validation
        if (!usernameInput.value.trim()) {
            showError('usernameError', 'Username is required');
            isValid = false;
        } else if (usernameInput.value.trim().length < 3) {
            showError('usernameError', 'Username must be at least 3 characters');
            isValid = false;
        }
        
        // Email validation
        if (!emailInput.value.trim()) {
            showError('emailError', 'Email is required');
            isValid = false;
        } else if (!validateEmail(emailInput.value.trim())) {
            showError('emailError', 'Please enter a valid email address');
            isValid = false;
        }
        
        // Password validation
        if (!passwordInput.value) {
            showError('passwordError', 'Password is required');
            isValid = false;
        } else if (passwordInput.value.length < 8) {
            showError('passwordError', 'Password must be at least 8 characters');
            isValid = false;
        }
        
        // Role validation
        if (!roleInput.value) {
            showError('roleError', 'Please select a role');
            isValid = false;
        }
        
        if (isValid) {
            await submitForm();
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

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function calculatePasswordStrength(password) {
        let strength = 0;
        
        // Length >= 8
        if (password.length >= 8) strength++;
        
        // Contains lowercase
        if (/[a-z]/.test(password)) strength++;
        
        // Contains uppercase
        if (/[A-Z]/.test(password)) strength++;
        
        // Contains number or special char
        if (/[0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) strength++;
        
        return strength;
    }

    function showToast(message, isSuccess = true) {
        toast.textContent = message;
        toast.style.backgroundColor = isSuccess ? '#2ecc71' : '#e74c3c';
        toast.classList.add('show');
        
        setTimeout(() => {
            toast.classList.remove('show');
        }, 5000);
    }

    async function submitForm() {
        const submitBtn = signupForm.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        
        try {
            const formData = {
                username: usernameInput.value.trim(),
                email: emailInput.value.trim(),
                password_hash: passwordInput.value,
                role: roleInput.value
            };
            
            const response = await fetch('/auth/signup', {
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
                throw new Error(data.message || 'Signup failed');
            }
            
            // On success
            showToast('Account created successfully! Redirecting to login...');
            
            // Redirect to login after 3 seconds
            setTimeout(() => {
                window.location.href = '/login';
            }, 3000);
            
        } catch (error) {
            console.error('Signup error:', error);
            
            if (error.message.includes('username')) {
                showError('usernameError', error.message);
            } else if (error.message.includes('email')) {
                showError('emailError', error.message);
            } else {
                showToast(error.message || 'An error occurred during signup', false);
            }
        } finally {
            submitBtn.disabled = false;
        }
    }
});