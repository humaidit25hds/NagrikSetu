document.addEventListener('DOMContentLoaded', () => {
  const body = document.body;
  const navToggle = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('.nav-links');
  const toast = document.querySelector('.toast');
  const showToast = (message) => {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.add('show');
    window.setTimeout(() => toast.classList.remove('show'), 2800);
  };
  navToggle?.addEventListener('click', () => nav?.classList.toggle('open'));
  document.querySelectorAll('[data-senior-mode]').forEach((button) => {
    button.addEventListener('click', () => {
      body.classList.toggle('senior-mode');
      const enabled = body.classList.contains('senior-mode');
      document.querySelectorAll('[data-senior-mode]').forEach((item) => item.textContent = enabled ? 'Disable Senior Citizen Mode' : 'Enable Senior Citizen Mode');
      showToast(enabled ? 'Senior Citizen Mode enabled' : 'Senior Citizen Mode disabled');
    });
  });
  document.querySelectorAll('[data-ask]').forEach((button) => button.addEventListener('click', () => {
    const question = button.dataset.ask || 'Tell me what you need help with.';
    localStorage.setItem('setu-question', question);
    window.location.href = 'chat-page.html';
  }));
  document.querySelectorAll('[data-detail]').forEach((button) => button.addEventListener('click', () => {
    document.querySelectorAll('.detail').forEach((panel) => panel.classList.remove('open'));
    document.getElementById(button.dataset.detail)?.classList.add('open');
    document.getElementById(button.dataset.detail)?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }));
  document.querySelectorAll('[data-filter-group]').forEach((group) => {
    const buttons = group.querySelectorAll('.filter');
    buttons.forEach((button) => button.addEventListener('click', () => {
      buttons.forEach((item) => item.classList.remove('active'));
      button.classList.add('active');
      const value = button.dataset.filter;
      document.querySelectorAll(`[data-filter-item="${group.dataset.filterGroup}"]`).forEach((item) => {
        item.hidden = value !== 'all' && item.dataset.category !== value;
      });
    }));
  });
  const serviceSearch = document.querySelector('[data-service-search]');
  serviceSearch?.addEventListener('input', () => {
    const query = serviceSearch.value.toLowerCase();
    document.querySelectorAll('[data-service-item]').forEach((item) => {
      item.hidden = !item.textContent.toLowerCase().includes(query);
    });
  });
  const chatForm = document.querySelector('[data-chat-form]');
  const messages = document.querySelector('[data-messages]');
  const chatInput = document.querySelector('[data-chat-input]');
  const addMessage = (text, type) => {
    const message = document.createElement('div');
    message.className = `message ${type}`;
    message.innerHTML = `<p>${text}</p>`;
    messages?.appendChild(message);
    messages?.scrollTo({ top: messages.scrollHeight, behavior: 'smooth' });
  };
  const savedQuestion = localStorage.getItem('setu-question');
  if (savedQuestion && chatInput) { chatInput.value = savedQuestion; localStorage.removeItem('setu-question'); }
  chatForm?.addEventListener('submit', (event) => {
    event.preventDefault();
    const value = chatInput?.value.trim();
    if (!value) return;
    addMessage(value, 'user');
    chatInput.value = '';
    window.setTimeout(() => addMessage('I can help you find the right service. Which state should I check, and what outcome do you need?', 'assistant'), 450);
  });
  document.querySelectorAll('[data-suggestion]').forEach((button) => button.addEventListener('click', () => {
    if (chatInput) { chatInput.value = button.dataset.suggestion; chatForm?.requestSubmit(); }
  }));
  document.querySelectorAll('[data-tab]').forEach((button) => button.addEventListener('click', () => {
    document.querySelectorAll('[data-tab]').forEach((item) => item.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach((item) => item.classList.remove('active'));
    button.classList.add('active');
    document.getElementById(button.dataset.tab)?.classList.add('active');
  }));
  document.querySelectorAll('[data-speak]').forEach((button) => button.addEventListener('click', () => showToast('Voice mode is ready. Speak your question clearly.')));
});
