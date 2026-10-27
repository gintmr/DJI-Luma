import { initHeaderNav } from '../ui/nav.js';
// A fixed project palette. No storage, telemetry, network calls or visitor modules.
document.documentElement.setAttribute('data-gintmr_ui-js', '');
initHeaderNav();
document.querySelector('[data-copy]')?.addEventListener('click', async event => {
  const source = document.getElementById(event.currentTarget.dataset.copy);
  const status = document.getElementById('copy-status');
  try {
    await navigator.clipboard.writeText(source.textContent);
    status.textContent = document.documentElement.lang === 'en' ? 'Copied. Add your device details and share with your Agent.' : '已复制，可补全设备信息后发给 Agent。';
  } catch {
    source.hidden = false;
    source.focus();
    const range = document.createRange();
    range.selectNodeContents(source);
    const selection = window.getSelection();
    selection.removeAllRanges(); selection.addRange(range);
    status.textContent = document.documentElement.lang === 'en' ? 'Text selected. Copy it or download the Markdown file.' : '已选中文本，请手动复制，或下载 Markdown。';
  }
});
