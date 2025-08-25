document.addEventListener('DOMContentLoaded', () => {

    const logoutDialog = document.getElementById('logoutDialog');
    const logoutCancelBtn = document.getElementById('logoutCancelBtn');

    // Logout buttons (can be navbar or dashboard)
    const logoutButtons = [
        document.querySelector('.js-logout'), // Navbar
        document.getElementById('parentDashboardLogoutBtn'), // Parent dashboard
        document.getElementById('teacherDashboardLogoutBtn') // Teacher dashboard
    ].filter(btn => btn !== null);

    if (logoutDialog && logoutCancelBtn) {
        // Attach click event to all logout buttons
        logoutButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                logoutDialog.showModal();
            });
        });

        logoutCancelBtn.addEventListener('click', () => {
            logoutDialog.close();
        });
    }
});


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
};