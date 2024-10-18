document.getElementById('edit-details-button').addEventListener('click', function() {
    document.getElementById('edit-details-form').style.display = 'block';
    document.getElementById('change-password-form').style.display = 'none';
});

document.getElementById('change-password-button').addEventListener('click', function() {
    document.getElementById('edit-details-form').style.display = 'none';
    document.getElementById('change-password-form').style.display = 'block';
});

document.addEventListener('DOMContentLoaded', function () {
    const nameField = document.getElementById('name');
    const addressField = document.getElementById('address');
    const phoneField = document.getElementById('phone');
    const passwordField = document.getElementById('password');
    const confirmPasswordField = document.getElementById('confirmPassword');

    const nameError = document.getElementById('nameError');
    const addressError = document.getElementById('addressError');
    const phoneError = document.getElementById('phoneError');
    const passwordError = document.getElementById('passwordError');
    const confirmPasswordError = document.getElementById('confirmPasswordError');

    const namePattern = /^[A-Z][a-zA-Z\s.]*$/;
    const phonePattern = /^[6-9][0-9]{9,13}$/;
    const addressPattern = /^[a-zA-Z0-9.,\s]+$/;
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    function validateName() {
        const nameValue = nameField.value.trim();
        if (!namePattern.test(nameValue) || /\s{2,}/.test(nameValue) || /^\s/.test(nameValue)) {
            nameError.textContent = "Invalid name. Start with a capital letter";
            return false;
        }
        nameError.textContent = "";
        return true;
    }

    function validateAddress() {
        if (!addressPattern.test(addressField.value.trim()) || /\s{2,}/.test(addressField.value)) {
            addressError.textContent = "Invalid address. No leading/trailing spaces.";
            return false;
        }
        addressError.textContent = "";
        return true;
    }

    function validatePhone() {
        if (!phonePattern.test(phoneField.value) || /^(.)\1*$/.test(phoneField.value)) {
            phoneError.textContent = "Invalid phone number. Follow the standard format.";
            return false;
        }
        phoneError.textContent = "";
        return true;
    }

    function validatePassword() {
        if (!passwordPattern.test(passwordField.value)) {
            passwordError.textContent = "Include at least one capital letter, one small letter, one number, and one special character.";
            return false;
        }
        passwordError.textContent = "";
        return true;
    }

    function validateConfirmPassword() {
        if (confirmPasswordField.value !== passwordField.value) {
            confirmPasswordError.textContent = "Passwords do not match.";
            return false;
        }
        confirmPasswordError.textContent = "";
        return true;
    }

    function clearErrorMessages() {
        nameError.textContent = "";
        addressError.textContent = "";
        phoneError.textContent = "";
        passwordError.textContent = "";
        confirmPasswordError.textContent = "";
    }

    nameField.addEventListener('input', validateName);
    addressField.addEventListener('input', validateAddress);
    phoneField.addEventListener('input', validatePhone);
    passwordField.addEventListener('input', validatePassword);
    confirmPasswordField.addEventListener('input', validateConfirmPassword);

    nameField.addEventListener('focus', clearErrorMessages);
    addressField.addEventListener('focus', clearErrorMessages);
    phoneField.addEventListener('focus', clearErrorMessages);
    passwordField.addEventListener('focus', clearErrorMessages);
    confirmPasswordField.addEventListener('focus', clearErrorMessages);

    document.getElementById('editDetailsForm').addEventListener('submit', function (event) {
        if (!validateName() || !validateAddress() || !validatePhone()) {
            event.preventDefault();
        }
    });

    document.getElementById('changePasswordForm').addEventListener('submit', function (event) {
        if (!validatePassword() || !validateConfirmPassword()) {
            event.preventDefault();
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const returnButtons = document.querySelectorAll('.return-button');

    returnButtons.forEach(button => {
        button.addEventListener('click', function () {
            const orderId = this.getAttribute('data-order-id');
            const modalHtml = `
                <div class="modal" id="damageModal">
                    <h2>Is there any damage to the product?</h2>
                    <button id="noDamageButton">No</button>
                    <button id="damageButton">Yes</button>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHtml);

            document.getElementById('noDamageButton').addEventListener('click', function () {
                fetch(`/process-return/${orderId}/?action=no_damages`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.status === 'collected') {
                            button.textContent = 'Collected';
                            document.getElementById('damageModal').remove();
                        }
                    });
            });

            document.getElementById('damageButton').addEventListener('click', function () {
                window.location.href = `/process-return/${orderId}/?action=damages`;
            });
        });
    });
});
