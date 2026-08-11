// ─── Demo Users ───────────────────────────────────────────────
const USERS = {
  admin: { password: "admin123", accountNumber: "001-234", balance: 1000.00 },
  john:  { password: "john456",  accountNumber: "002-567", balance: 500.00  },
  jane:  { password: "jane789",  accountNumber: "003-890", balance: 2500.00 },
};

// ─── App State ────────────────────────────────────────────────
let currentUser = null;
let transactions = [];
let transactionCount = 0;

// ─── Helpers ──────────────────────────────────────────────────
function formatCurrency(amount) {
  return `$${parseFloat(amount).toFixed(2)}`;
}

function formatDate() {
  return new Date().toLocaleString();
}

function showMessage(elementId, message, type) {
  const el = document.getElementById(elementId);
  el.textContent = message;
  el.className = type; // 'success' or 'error'
  el.classList.remove('hidden');
}

function clearMessage(elementId) {
  const el = document.getElementById(elementId);
  el.textContent = '';
  el.classList.add('hidden');
}

function updateBalanceDisplay() {
  document.getElementById('balance-display').textContent =
    formatCurrency(USERS[currentUser].balance);
}

// ─── Login ────────────────────────────────────────────────────
function login() {
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();

  if (!username || !password) {
    showMessage('login-error', 'Please enter username and password.', 'error');
    return;
  }

  if (USERS[username] && USERS[username].password === password) {
    currentUser = username;
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('dashboard-section').classList.remove('hidden');
    document.getElementById('welcome-msg').textContent = `Welcome, ${username}!`;
    document.getElementById('account-number').textContent =
      `Account: #${USERS[username].accountNumber}`;
    updateBalanceDisplay();
    clearMessage('login-error');
  } else {
    showMessage('login-error', 'Invalid username or password.', 'error');
  }
}

// Allow pressing Enter to login
document.getElementById('password').addEventListener('keydown', function (e) {
  if (e.key === 'Enter') login();
});

// ─── Logout ───────────────────────────────────────────────────
function logout() {
  currentUser = null;
  transactions = [];
  transactionCount = 0;

  document.getElementById('username').value = '';
  document.getElementById('password').value = '';
  document.getElementById('transaction-body').innerHTML =
    '<tr id="no-transactions"><td colspan="6">No transactions yet.</td></tr>';

  document.getElementById('dashboard-section').classList.add('hidden');
  document.getElementById('login-section').classList.remove('hidden');
}

// ─── Add Transaction Row ──────────────────────────────────────
function addTransactionRow(type, amount, balanceAfter, status) {
  transactionCount++;

  const noTx = document.getElementById('no-transactions');
  if (noTx) noTx.remove();

  const tbody = document.getElementById('transaction-body');
  const row = document.createElement('tr');
  row.id = `transaction-row-${transactionCount}`;

  row.innerHTML = `
    <td>${transactionCount}</td>
    <td>${type}</td>
    <td>${formatCurrency(amount)}</td>
    <td>${formatCurrency(balanceAfter)}</td>
    <td>${formatDate()}</td>
    <td class="${status === 'Success' ? 'status-success' : 'status-failed'}">${status}</td>
  `;

  tbody.prepend(row);
}

// ─── Deposit ──────────────────────────────────────────────────
function deposit() {
  clearMessage('deposit-msg');
  const input = document.getElementById('deposit-amount');
  const amount = parseFloat(input.value);

  if (!amount || amount <= 0) {
    showMessage('deposit-msg', 'Please enter a valid amount.', 'error');
    addTransactionRow('Deposit', amount || 0, USERS[currentUser].balance, 'Failed');
    return;
  }

  if (amount > 100000) {
    showMessage('deposit-msg', 'Maximum deposit limit is $100,000.', 'error');
    addTransactionRow('Deposit', amount, USERS[currentUser].balance, 'Failed');
    return;
  }

  USERS[currentUser].balance += amount;
  updateBalanceDisplay();
  showMessage('deposit-msg', `Successfully deposited ${formatCurrency(amount)}.`, 'success');
  addTransactionRow('Deposit', amount, USERS[currentUser].balance, 'Success');
  input.value = '';
}

// ─── Withdraw ─────────────────────────────────────────────────
function withdraw() {
  clearMessage('withdraw-msg');
  const input = document.getElementById('withdraw-amount');
  const amount = parseFloat(input.value);

  if (!amount || amount <= 0) {
    showMessage('withdraw-msg', 'Please enter a valid amount.', 'error');
    addTransactionRow('Withdrawal', amount || 0, USERS[currentUser].balance, 'Failed');
    return;
  }

  if (amount > USERS[currentUser].balance) {
    showMessage('withdraw-msg', 'Insufficient funds.', 'error');
    addTransactionRow('Withdrawal', amount, USERS[currentUser].balance, 'Failed');
    return;
  }

  if (amount > 10000) {
    showMessage('withdraw-msg', 'Maximum withdrawal limit is $10,000.', 'error');
    addTransactionRow('Withdrawal', amount, USERS[currentUser].balance, 'Failed');
    return;
  }

  USERS[currentUser].balance -= amount;
  updateBalanceDisplay();
  showMessage('withdraw-msg', `Successfully withdrew ${formatCurrency(amount)}.`, 'success');
  addTransactionRow('Withdrawal', amount, USERS[currentUser].balance, 'Success');
  input.value = '';
}