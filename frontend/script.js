// ── CONFIG ──
const API = 'https://resume-analyzer-ufff.onrender.com';

// ── AUTH GUARD ──
function guardAuth(requiredRole) {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');
  if (!token || (requiredRole && role !== requiredRole)) {
    window.location.href = 'login.html';
  }
}

function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  window.location.href = 'index.html';
}

// ── AUTH FETCH ──
async function authFetch(url, options = {}) {
  const token = localStorage.getItem('token');
  const res = await fetch(url, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      ...(options.headers || {})
    }
  });
  if (res.status === 401 || res.status === 403) {
    logout();
    return;
  }
  return res.json();
}

// ── UI HELPERS ──
function show(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = '';
}
function hide(id) {
  const el = document.getElementById(id);
  if (el) el.style.display = 'none';
}

function setLoading(btnId, textId, spinnerId, isLoading, label) {
  const btn = document.getElementById(btnId);
  const txt = document.getElementById(textId);
  const spin = document.getElementById(spinnerId);
  if (!btn) return;
  btn.disabled = isLoading;
  if (txt) txt.textContent = label;
  if (spin) spin.style.display = isLoading ? 'block' : 'none';
}

function renderTags(containerId, items, color) {
  const el = document.getElementById(containerId);
  if (!el) return;
  if (!items || items.length === 0) {
    el.innerHTML = '<span class="muted-text">None detected</span>';
    return;
  }
  el.innerHTML = items.map(i =>
    `<span class="tag" ${color ? `style="background:${color}20;color:${color}"` : ''}>${escHtml(String(i))}</span>`
  ).join('');
}

function escHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}