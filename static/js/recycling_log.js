document.addEventListener('DOMContentLoaded', function () {
    const recyclingForm = document.getElementById('recycling-log-form');
    const logResult = document.getElementById('log-result');

    if (recyclingForm) {
        recyclingForm.addEventListener('submit', function (e) {
            e.preventDefault();
            const material = document.getElementById('material').value;
            const weight = parseFloat(document.getElementById('weight').value);

            fetch('/log_recycling', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ material: material, weight: weight }),
                credentials: 'include'
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        logResult.textContent = 'Recycling logged successfully!';
                        recyclingForm.reset();
                    } else {
                        logResult.textContent = 'Failed to log recycling: ' + data.message;
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    logResult.textContent = 'An error occurred. Please try again.';
                });
        });
    }
});