const menuButton = document.querySelector('.nav-toggle');
const menu = document.getElementById('site-nav');
menuButton?.addEventListener('click', () => {
  const expanded = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(expanded));
  menu.classList.toggle('is-open', expanded);
});
menu?.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => {
  menuButton?.setAttribute('aria-expanded', 'false');
  menu.classList.remove('is-open');
}));
if (document.body.dataset.page === 'about') document.querySelector('[data-nav="about"]')?.setAttribute('aria-current', 'page');
if (['billing', 'console', 'education'].includes(document.body.dataset.page)) document.querySelector('[data-nav="projects"]')?.setAttribute('aria-current', 'page');

const imageDialog = document.querySelector('.image-dialog');
let lastImageButton = null;
document.querySelectorAll('[data-zoom]').forEach((button) => button.addEventListener('click', () => {
  lastImageButton = button;
  const image = document.getElementById('dialog-image');
  image.src = button.dataset.zoom;
  image.alt = button.dataset.caption || '';
  document.getElementById('image-caption').textContent = image.alt;
  imageDialog.showModal();
}));
const closeImage = () => imageDialog?.close();
document.querySelector('.close-dialog')?.addEventListener('click', closeImage);
imageDialog?.addEventListener('click', (event) => { if (event.target === imageDialog) closeImage(); });
imageDialog?.addEventListener('close', () => lastImageButton?.focus());

document.querySelectorAll('[data-document-tab]').forEach((button) => button.addEventListener('click', () => {
  document.querySelectorAll('[data-document-tab]').forEach((tab) => {
    const active = tab === button;
    tab.setAttribute('aria-selected', String(active));
    document.getElementById(tab.getAttribute('aria-controls')).hidden = !active;
  });
}));
document.querySelector('[role="tablist"]')?.addEventListener('keydown', (event) => {
  const tabs = [...event.currentTarget.querySelectorAll('[role="tab"]')];
  let index = tabs.indexOf(document.activeElement);
  if (event.key === 'ArrowRight') index = (index + 1) % tabs.length;
  else if (event.key === 'ArrowLeft') index = (index - 1 + tabs.length) % tabs.length;
  else if (event.key === 'Home') index = 0;
  else if (event.key === 'End') index = tabs.length - 1;
  else return;
  event.preventDefault(); tabs[index].focus(); tabs[index].click();
});
const travelToggle = document.getElementById('travel-toggle');
travelToggle?.addEventListener('change', () => {
  const active = travelToggle.checked;
  document.querySelector('.timeline-demo')?.classList.toggle('without-travel', !active);
  document.getElementById('claim-count').textContent = active ? '3' : '2';
  document.querySelector('.time-segment.after.first span').innerHTML = active ? '10–18일<br>새 처방' : '10–31일<br>새 처방';
  document.getElementById('timeline-explanation').textContent = active
    ? '처방 변경과 해외 체류를 함께 반영하면 세 개의 국내 청구 구간이 생깁니다. 여행 전후 구간은 같은 처방·SR 근거를 공유할 수 있습니다.'
    : '여행 기록이 없을 때는 처방 변경일을 기준으로 두 구간으로 나뉩니다. 월 전체를 관리하는 BillingCycle은 그대로 한 건입니다.';
});
document.querySelectorAll('[data-print]').forEach((button) => button.addEventListener('click', () => window.print()));

const readingSections = [...document.querySelectorAll('.case-section[id]')];
if ('IntersectionObserver' in window && readingSections.length) {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      document.querySelectorAll('.case-nav a').forEach((a) => a.classList.toggle('active', a.hash === '#' + entry.target.id));
    });
  }, { rootMargin: '-10% 0px -65% 0px' });
  readingSections.forEach((s) => observer.observe(s));
}
