document.addEventListener('DOMContentLoaded', () => {
    // --- Logout Dialog ---
    const logoutDialog = document.getElementById('logoutDialog');
    const logoutCancelBtn = document.getElementById('logoutCancelBtn');
    const logoutBtn = document.querySelector('.js-logout'); // Navbar logout button

    if (logoutDialog && logoutCancelBtn && logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            logoutDialog.showModal();
        });

        logoutCancelBtn.addEventListener('click', () => {
            logoutDialog.close();
        });
    }

    // --- Enrollment Cancel Dialog ---
    const cancelDialog = document.getElementById('cancelEnrollmentDialog');
    const cancelNoBtn = document.getElementById('cancelNoBtn');
    const cancelYesBtn = document.getElementById('cancelYesBtn');
    let formToSubmit = null;

    if (cancelDialog && cancelNoBtn && cancelYesBtn) {
        document.querySelectorAll('.cancel-enrollment-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                formToSubmit = btn.closest('.cancel-enrollment-form');
                cancelDialog.showModal();
            });
        });

        cancelNoBtn.addEventListener('click', () => {
            formToSubmit = null;
            cancelDialog.close();
        });

        cancelYesBtn.addEventListener('click', () => {
            if (formToSubmit) formToSubmit.submit();
        });
    }
});