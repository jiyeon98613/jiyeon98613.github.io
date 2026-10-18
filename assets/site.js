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

// Each tablist controls its own panels; arrow keys follow the selected tab.
document.querySelectorAll('[role="tablist"]').forEach((group) => {
  const tabs = [...group.querySelectorAll('[role="tab"]')];
  const select = (button) => tabs.forEach((tab) => {
    const active = tab === button;
    tab.setAttribute('aria-selected', String(active));
    tab.tabIndex = active ? 0 : -1;
    const panel = document.getElementById(tab.getAttribute('aria-controls'));
    if (panel) panel.hidden = !active;
  });
  tabs.forEach((tab) => tab.addEventListener('click', () => select(tab)));
  if (tabs.length) select(tabs.find((tab) => tab.getAttribute('aria-selected') === 'true') || tabs[0]);
  group.addEventListener('keydown', (event) => {
    let index = tabs.indexOf(document.activeElement);
    if (index < 0) return;
    if (event.key === 'ArrowRight') index = (index + 1) % tabs.length;
    else if (event.key === 'ArrowLeft') index = (index - 1 + tabs.length) % tabs.length;
    else if (event.key === 'Home') index = 0;
    else if (event.key === 'End') index = tabs.length - 1;
    else return;
    event.preventDefault(); tabs[index].focus(); select(tabs[index]);
  });
});
const revealLinkedTab = () => {
  const target = document.getElementById(decodeURIComponent(location.hash.slice(1)));
  const panel = target?.closest('[role="tabpanel"]');
  if (!panel?.hidden) return;
  const button = [...document.querySelectorAll('[role="tab"]')].find((tab) => tab.getAttribute('aria-controls') === panel.id);
  button?.click();
  if (button) requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
};
revealLinkedTab();
window.addEventListener('hashchange', revealLinkedTab);

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

// Fixed fictional values explain the lifecycle; no billing calculation or API call.
const statementExamples = {
  issued: { source: '17,800원', hash: 'H₁', snapshot: '17,800원', revision: '개정 1 · ISSUED', message: '검토한 자료 H₁로 개정 1을 발행했습니다. 발행 당시 금액은 payload_snapshot에 보존됩니다.' },
  changed: { source: '20,800원', hash: 'H₂', snapshot: '17,800원', revision: '개정 1 · ISSUED 유지', message: '원천 금액이 20,800원으로 바뀌어도 기존 발행본은 17,800원입니다. 이전 source_hash로 새 발행을 진행하지 않고 변경된 자료를 다시 검토합니다.' },
  reissued: { source: '20,800원', hash: 'H₂', snapshot: '20,800원', revision: '개정 2 · ISSUED', message: '변경된 자료 H₂를 검토해 개정 2를 발행했습니다. 개정 1의 payload_snapshot과 17,800원 기록은 그대로 보존됩니다.' },
};
document.querySelectorAll('[data-statement-example]').forEach((button) => button.addEventListener('click', () => {
  const example = statementExamples[button.dataset.statementExample];
  document.querySelectorAll('[data-statement-example]').forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
  document.getElementById('statement-source-amount').textContent = example.source;
  document.getElementById('statement-source-hash').textContent = example.hash;
  document.getElementById('statement-snapshot-amount').textContent = example.snapshot;
  document.getElementById('statement-snapshot-revision').textContent = example.revision;
  document.getElementById('statement-example-result').textContent = example.message;
}));

document.querySelectorAll('[data-mask-example]').forEach((button) => button.addEventListener('click', () => {
  const missing = button.dataset.maskExample === 'missing';
  document.querySelectorAll('[data-mask-example]').forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
  document.querySelector('#mask-example-status code').textContent = `mask_ok = ${!missing}`;
  document.getElementById('mask-example-anchors').textContent = missing ? '하단 안내문을 찾지 못함' : '제목 · 진료과목 · 하단 안내문 확인';
  document.getElementById('mask-example-action').textContent = missing ? '전송 차단' : '관리자 검토·승인 대기';
  document.getElementById('mask-example-result').textContent = missing
    ? '마스킹 기준이 불완전하므로 추출 대상에서 제외합니다. 마스킹하지 않은 원본으로 대체 전송하지 않습니다.'
    : '마스킹 결과를 관리자가 확인하고 전송을 승인한 자료만 외부 추출 대상으로 사용합니다.';
  document.getElementById('mask-gate-demo').classList.toggle('example-blocked', missing);
}));

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
