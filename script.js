// --- CONFIG ---
const API_URL = '/api/rate-username';

// --- UI Elements ---
const form = document.getElementById('rateForm');
const usernameInput = document.getElementById('username');
const output = document.getElementById('output');
const typing = document.getElementById('typing');
const dots = document.getElementById('dots');

// --- Typing Animation ---
let typingInterval;
function startTypingAnim() {
  typing.style.display = 'block';
  let dotCount = 0;
  dots.textContent = '';
  typingInterval = setInterval(() => {
    dotCount = (dotCount + 1) % 4;
    dots.textContent = '.'.repeat(dotCount);
  }, 400);
}
function stopTypingAnim() {
  typing.style.display = 'none';
  clearInterval(typingInterval);
}

// --- Render Output ---
function renderResult(data) {
  const rating = data.rating || '<span style="color:var(--muted)">N/A</span>';
  const roast = data.roast || '<span style="color:var(--muted)">N/A</span>';
  const vibe = data.vibe || '<span style="color:var(--muted)">N/A</span>';
  const suggestions = data.suggestions && Array.isArray(data.suggestions)
    ? data.suggestions.map(s => `<span class="suggestion">${s}</span>`).join('')
    : '<span style="color:var(--muted)">N/A</span>';

  output.innerHTML = `
    <div class="result-block">
      <div class="result-title">⭐ Rating</div>
      <div class="result-content">${rating}</div>
    </div>
    <div class="result-block">
      <div class="result-title">🔥 Roast</div>
      <div class="result-content">${roast}</div>
    </div>
    <div class="result-block">
      <div class="result-title">🎭 Vibe Tag</div>
      <div class="result-content">${vibe}</div>
    </div>
    <div class="result-block">
      <div class="result-title">💡 Suggestions</div>
      <div class="suggestions">${suggestions}</div>
    </div>
  `;
}

// --- Form Handler ---
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = usernameInput.value.trim().replace(/^@/, '');
  if (!username) return;

  output.innerHTML = '';
  startTypingAnim();

  try {
    const res = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username })
    });

    const data = await res.json();
    stopTypingAnim();

    if (!res.ok || data.error) {
      output.innerHTML = `
        <div style="color:var(--fail);text-align:center;font-weight:700;">
          ${data.error || 'API request failed'}
          ${data.raw ? `<pre style="white-space:pre-wrap;font-size:0.9em;">${data.raw}</pre>` : ''}
        </div>
      `;
      return;
    }

    renderResult(data);
  } catch (err) {
    stopTypingAnim();
    output.innerHTML = `
      <div style="color:var(--fail);text-align:center;font-weight:700;">
        Error: ${err.message || 'Could not rate username.'}
      </div>
    `;
  }
});
