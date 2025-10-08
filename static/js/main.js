// static/js/main.js

$(document).ready(function() {
    // Set the date input on the main form to today's date by default
    const today = new Date().toISOString().split('T')[0];
    $('#date').val(today);

    // --- Frontend Form Validation for ADDING expenses ---
    $('#expense-form').on('submit', function(event) {
        if (!validateForm('#expense-form')) {
            event.preventDefault(); // Stop form submission if validation fails
        }
    });

    // --- Frontend Form Validation for EDITING expenses ---
    $('#edit-expense-form').on('submit', function(event) {
        if (!validateForm('#edit-expense-form')) {
            event.preventDefault(); // Stop form submission if validation fails
        }
    });

    // --- Confirmation for Delete ---
    $('.delete-form').on('submit', function(event) {
        if (!confirm('Are you sure you want to delete this expense? This action cannot be undone.')) {
            event.preventDefault();
        }
    });

    // --- Edit button click handler ---
    $('.edit-btn').on('click', function() {
        const expenseId = $(this).data('id');

        // Fetch expense data from the server
        $.ajax({
            url: `/expense/${expenseId}`,
            type: 'GET',
            success: function(expense) {
                // Populate the modal form with the fetched data
                $('#edit-id').val(expense.id);
                $('#edit-description').val(expense.description);
                $('#edit-category').val(expense.category);
                $('#edit-amount').val(expense.amount);
                $('#edit-date').val(expense.date);
                $('#edit-payment_method').val(expense.payment_method);

                // Set the form's action attribute dynamically
                $('#edit-expense-form').attr('action', `/edit/${expense.id}`);
            },
            error: function(error) {
                console.error("Error fetching expense data:", error);
                showAlert('Could not retrieve expense details. Please try again.', 'danger');
            }
        });
    });

    // --- Reusable form validation function ---
    function validateForm(formId) {
        let isValid = true;
        let message = '';

        const description = $(`${formId} input[name='description']`).val().trim();
        const category = $(`${formId} select[name='category']`).val();
        const amount = $(`${formId} input[name='amount']`).val();
        const date = $(`${formId} input[name='date']`).val();
        const paymentMethod = $(`${formId} select[name='payment_method']`).val();

        if (description === '') {
            isValid = false;
            message = 'Description cannot be empty.';
        } else if (category === null) {
            isValid = false;
            message = 'Please select a category.';
        } else if (paymentMethod === null) {
            isValid = false;
            message = 'Please select a payment method.';
        } else if (amount <= 0) {
            isValid = false;
            message = 'Amount must be a positive number.';
        } else if (date === '') {
            isValid = false;
            message = 'Please select a date.';
        }

        if (!isValid) {
            showAlert(message, 'warning');
        }
        return isValid;
    }

    // --- Helper function to show alerts ---
    function showAlert(message, type) {
        // Clear previous alerts
        $('#alert-container').empty();

        const alertHtml = `
            <div class="alert alert-${type} alert-dismissible fade show shadow-sm" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>`;
        $('#alert-container').html(alertHtml);

        // Auto-dismiss the alert after 5 seconds
        setTimeout(function() {
            $('#alert-container .alert').alert('close');
        }, 5000);
    }
});