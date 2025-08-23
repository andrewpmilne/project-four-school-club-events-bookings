document.addEventListener('DOMContentLoaded', () => {
    const logoutBtn = document.querySelector('.js-logout');
    const logoutDialog = document.getElementById('logoutDialog');
    const logoutCancelBtn = document.getElementById('logoutCancelBtn');
    const logoutForm = document.getElementById('logoutForm');

    // Open dialog when logout button clicked
    logoutBtn.addEventListener('click', (e) => {
        e.preventDefault();
        logoutDialog.showModal();
    });

    // Close dialog when cancel clicked
    logoutCancelBtn.addEventListener('click', () => {
        logoutDialog.close();
    });
});