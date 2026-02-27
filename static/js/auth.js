// ===================================
// WEll-track Authentication
// ===================================

document.addEventListener('DOMContentLoaded', function() {
    // ========== LOGIN PAGE ==========
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        // Toggle password visibility
        const togglePassword = document.getElementById('togglePassword');
        const passwordInput = document.getElementById('password');
        const eyeIcon = document.getElementById('eyeIcon');

        if (togglePassword) {
            togglePassword.addEventListener('click', function() {
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);
                eyeIcon.classList.toggle('bi-eye');
                eyeIcon.classList.toggle('bi-eye-slash');
            });
        }

        // Handle login form submission
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorMessage = document.getElementById('errorMessage');

            // Simple validation (in real app, this would be backend validation)
            if (!email || !password) {
                errorMessage.textContent = 'Заповніть всі поля';
                errorMessage.classList.remove('d-none');
                return;
            }

            // Mock login - create user session
            const user = {
                id: Date.now(),
                email: email,
                name: email.split('@')[0], // Use email prefix as name
                userType: 'user', // In real app, this comes from backend
                loginDate: new Date().toISOString()
            };

            setCurrentUser(user);

            // ✅ Django route
            window.location.href = '/dashboard/';
        });
    }

    // ========== REGISTRATION PAGE ==========
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        // Get user type from URL
        const urlParams = new URLSearchParams(window.location.search);
        const userType = urlParams.get('type') || 'user';

        // Update UI based on user type
        const userTypeText = document.getElementById('userTypeText');
        if (userTypeText) {
            userTypeText.textContent = userType === 'dietitian' ? 'дієтолог' : 'користувач';
        }

        // Toggle password visibility
        const togglePassword = document.getElementById('togglePassword');
        const passwordInput = document.getElementById('password');
        const eyeIcon = document.getElementById('eyeIcon');

        if (togglePassword) {
            togglePassword.addEventListener('click', function() {
                const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                passwordInput.setAttribute('type', type);
                eyeIcon.classList.toggle('bi-eye');
                eyeIcon.classList.toggle('bi-eye-slash');
            });
        }

        // Toggle confirm password visibility
        const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
        const confirmPasswordInput = document.getElementById('confirmPassword');
        const eyeIconConfirm = document.getElementById('eyeIconConfirm');

        if (toggleConfirmPassword) {
            toggleConfirmPassword.addEventListener('click', function() {
                const type = confirmPasswordInput.getAttribute('type') === 'password' ? 'text' : 'password';
                confirmPasswordInput.setAttribute('type', type);
                eyeIconConfirm.classList.toggle('bi-eye');
                eyeIconConfirm.classList.toggle('bi-eye-slash');
            });
        }

        // Handle registration form submission
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            const nickname = document.getElementById('nickname').value;
            const gender = document.getElementById('gender').value;
            const age = document.getElementById('age').value;
            const errorMessage = document.getElementById('errorMessage');

            // Validation
            if (!email || !password || !confirmPassword || !nickname || !gender || !age) {
                errorMessage.textContent = 'Заповніть всі поля';
                errorMessage.classList.remove('d-none');
                return;
            }

            if (password !== confirmPassword) {
                errorMessage.textContent = 'Паролі не співпадають';
                errorMessage.classList.remove('d-none');
                return;
            }

            if (password.length < 6) {
                errorMessage.textContent = 'Пароль повинен містити мінімум 6 символів';
                errorMessage.classList.remove('d-none');
                return;
            }

            if (parseInt(age) < 10 || parseInt(age) > 120) {
                errorMessage.textContent = 'Вік повинен бути від 10 до 120 років';
                errorMessage.classList.remove('d-none');
                return;
            }

            // Create user
            const user = {
                id: Date.now(),
                email: email,
                name: nickname,
                nickname: nickname,
                gender: gender,
                age: parseInt(age),
                userType: userType,
                registrationDate: new Date().toISOString()
            };

            setCurrentUser(user);

            // ✅ Django route
            window.location.href = '/dashboard/';
        });
    }
});
