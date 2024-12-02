document.addEventListener('DOMContentLoaded', () => {
    // Form Validation
    const form = document.querySelector('#create-recipe-form');
    const titleInput = document.querySelector('#title');
    const descriptionInput = document.querySelector('#description');
    const ingredientsInput = document.querySelector('#ingredients');
    const categorySelect = document.querySelector('#category_id');
    const imageInput = document.querySelector('#image');

    if (form) {
        form.addEventListener('submit', (e) => {
            let isValid = true;
            clearErrors();

            // Validate Title
            if (!validateLength(titleInput, 5, 50, 'Title')) isValid = false;

            // Validate Description
            if (!validateLength(descriptionInput, 10, 200, 'Description')) isValid = false;

            // Validate Ingredients
            if (!validateLength(ingredientsInput, 10, 300, 'Ingredients')) isValid = false;

            // Validate Category
            if (categorySelect.value === '') {
                showError(categorySelect, 'Please select a category.');
                isValid = false;
            }

            // Validate Image
            if (imageInput.files.length === 0) {
                showError(imageInput, 'Please upload an image.');
                isValid = false;
            } else {
                const file = imageInput.files[0];
                const validExtensions = ['image/jpeg', 'image/png', 'image/gif'];
                if (!validExtensions.includes(file.type)) {
                    showError(imageInput, 'Only JPEG, PNG, or GIF files are allowed.');
                    isValid = false;
                }
                if (file.size > 2 * 1024 * 1024) { // 2MB limit
                    showError(imageInput, 'Image size cannot exceed 2MB.');
                    isValid = false;
                }
            }

            // Prevent Submission if Invalid
            if (!isValid) {
                e.preventDefault();
            }
        });

        // Clear error messages
        function clearErrors() {
            document.querySelectorAll('.error-message').forEach(msg => msg.remove());
            document.querySelectorAll('.error').forEach(field => field.classList.remove('error'));
        }

        // Show error message
        function showError(input, message) {
            const error = document.createElement('div');
            error.className = 'error-message';
            error.textContent = message;
            input.classList.add('error');
            const parent = input.closest('.form-group') || input.parentElement; // Adjust for your layout
            parent.appendChild(error);
        }

        // Validate Input Length
        function validateLength(input, min, max, fieldName) {
            const value = input.value.trim();
            if (value === '') {
                showError(input, `${fieldName} is required.`);
                return false;
            } else if (value.length < min) {
                showError(input, `${fieldName} must be at least ${min} characters long.`);
                return false;
            } else if (value.length > max) {
                showError(input, `${fieldName} cannot exceed ${max} characters.`);
                return false;
            }
            return true;
        }
    }

    // Delete Confirmation
    const deleteButtons = document.querySelectorAll('.delete-btn');
    if (deleteButtons) {
        deleteButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const recipeId = button.getAttribute('data-id');

                showConfirmationDialog(
                    'Are you sure you want to delete this recipe?',
                    () => deleteRecipe(recipeId) // Pass the recipe ID to deleteRecipe
                );
            });
        });
    }

    // Confirmation Dialog for the delete - Are you sure you want to Delete 
    // this message will pop up as a dialog box
    function showConfirmationDialog(message, onConfirm) {
        const overlay = document.createElement('div');
        overlay.classList.add('confirmation-overlay');

        const dialog = document.createElement('div');
        dialog.classList.add('confirmation-dialog');

        const dialogMessage = document.createElement('p');
        dialogMessage.textContent = message;

        const confirmButton = document.createElement('button');
        confirmButton.textContent = 'Yes';
        confirmButton.classList.add('btn', 'confirm-btn');
        confirmButton.addEventListener('click', () => {
            onConfirm();
            closeDialog();
        });

        const cancelButton = document.createElement('button');
        cancelButton.textContent = 'Cancel';
        cancelButton.classList.add('btn', 'cancel-btn');
        cancelButton.addEventListener('click', closeDialog);

        dialog.appendChild(dialogMessage);
        dialog.appendChild(confirmButton);
        dialog.appendChild(cancelButton);
        overlay.appendChild(dialog);
        document.body.appendChild(overlay);
    }

    function closeDialog() {
        document.querySelector('.confirmation-overlay')?.remove();
    }

    // Delete Recipe
    function deleteRecipe(recipeId) {
        fetch(`/delete_recipe/${recipeId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/recipes'; // Redirect to recipes page
                } else {
                    alert('Failed to delete recipe.');
                }
            })
            .catch(error => {
                console.error('Error deleting recipe:', error);
                alert('An error occurred.');
            });
    }
});
