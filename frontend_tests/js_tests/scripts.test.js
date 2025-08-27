document.body.innerHTML = `
  <dialog id="logoutDialog"></dialog>
  <button id="logoutCancelBtn">Cancel</button>
  <button class="js-logout">Logout</button>

  <dialog id="cancelEnrollmentDialog"></dialog>
  <button id="cancelNoBtn">No</button>
  <button id="cancelYesBtn">Yes</button>
  <form class="cancel-enrollment-form">
    <button class="cancel-enrollment-btn">Cancel Enrollment</button>
  </form>
`;

require('../../static/js/script.js');

describe('Logout Dialog', () => {
  let logoutDialog, logoutBtn, logoutCancelBtn;

  beforeEach(() => {
    logoutDialog = document.getElementById('logoutDialog');
    logoutBtn = document.querySelector('.js-logout');
    logoutCancelBtn = document.getElementById('logoutCancelBtn');

    // Mock dialog methods
    logoutDialog.showModal = jest.fn();
    logoutDialog.close = jest.fn();

    // Fire DOMContentLoaded so event listeners attach
    document.dispatchEvent(new Event('DOMContentLoaded'));
  });

  test('Clicking logout shows logout dialog', () => {
    logoutBtn.click();
    expect(logoutDialog.showModal).toHaveBeenCalled();
  });

  test('Clicking cancel closes logout dialog', () => {
    logoutCancelBtn.click();
    expect(logoutDialog.close).toHaveBeenCalled();
  });
});

describe('Cancel Enrollment Dialog', () => {
  let cancelDialog, cancelNoBtn, cancelYesBtn, cancelBtn, form;

  beforeEach(() => {
    cancelDialog = document.getElementById('cancelEnrollmentDialog');
    cancelNoBtn = document.getElementById('cancelNoBtn');
    cancelYesBtn = document.getElementById('cancelYesBtn');
    cancelBtn = document.querySelector('.cancel-enrollment-btn');
    form = document.querySelector('.cancel-enrollment-form');

    cancelDialog.showModal = jest.fn();
    cancelDialog.close = jest.fn();
    form.submit = jest.fn();

    document.dispatchEvent(new Event('DOMContentLoaded'));
  });

  test('Clicking cancel-enrollment button shows dialog', () => {
    cancelBtn.click();
    expect(cancelDialog.showModal).toHaveBeenCalled();
  });

  test('Clicking No clears formToSubmit and closes dialog', () => {
    cancelBtn.click(); // select form
    cancelNoBtn.click();
    expect(cancelDialog.close).toHaveBeenCalled();
  });

  test('Clicking Yes submits the form', () => {
    cancelBtn.click(); // select form
    cancelYesBtn.click();
    expect(form.submit).toHaveBeenCalled();
  });
});