/* ============================================================================
   gintmr-ui · 顶栏菜单原语
   关闭逻辑是完整的一套：按钮、Esc、点击外部、点击链接、断点变化。
   面板状态写在导航自身的 data-gintmr_ui-open 上，CSS 只读这个属性。
   ========================================================================= */

const MOBILE_QUERY = '(min-width: 721px)';

/** 是否已经绑定过全局监听。客户端路由换页时元素会重建，
 *  但 document/window 级监听不能重复绑定，所以这里只绑一次，
 *  事件到来时再按当前 DOM 解析目标。 */
let navBound = false;

function navFor(toggle) {
  const id = toggle.getAttribute('aria-controls');
  return (id && document.getElementById(id)) || toggle.closest('.gintmr_ui-header-shell')?.querySelector('.gintmr_ui-nav');
}

const stateOf = toggle => ({ toggle, nav: navFor(toggle) });

function openMenu({ toggle, nav }) {
  nav?.setAttribute('data-gintmr_ui-open', 'true');
  toggle.setAttribute('aria-expanded', 'true');
  toggle.setAttribute('aria-label', 'Close navigation');
  nav?.querySelector('a')?.focus();
}

function shutMenu({ toggle, nav }, { restoreFocus = false } = {}) {
  nav?.setAttribute('data-gintmr_ui-open', 'false');
  toggle.setAttribute('aria-expanded', 'false');
  toggle.setAttribute('aria-label', 'Open navigation');
  if (restoreFocus) toggle.focus();
}

export function closeAllMenus() {
  document.querySelectorAll('.gintmr_ui-menu-toggle').forEach(toggle => shutMenu(stateOf(toggle)));
}

export function initHeaderNav() {
  document.querySelectorAll('.gintmr_ui-menu-toggle').forEach(toggle => {
    if (toggle.dataset.gintmr_uiReady === 'true') return;
    toggle.dataset.gintmr_uiReady = 'true';
    toggle.addEventListener('click', () => {
      const state = stateOf(toggle);
      if (toggle.getAttribute('aria-expanded') === 'true') shutMenu(state);
      else openMenu(state);
    });
  });

  if (navBound) return;
  navBound = true;

  const openToggles = () => [...document.querySelectorAll('.gintmr_ui-menu-toggle')]
    .filter(toggle => toggle.getAttribute('aria-expanded') === 'true')
    .map(stateOf);

  document.addEventListener('keydown', event => {
    if (event.key !== 'Escape') return;
    openToggles().forEach(state => shutMenu(state, { restoreFocus: true }));
  });
  document.addEventListener('click', event => {
    if (event.target.closest('.gintmr_ui-header-shell')) return;
    openToggles().forEach(state => shutMenu(state));
  });
  document.addEventListener('click', event => {
    const link = event.target.closest('.gintmr_ui-nav a');
    if (!link) return;
    const state = openToggles().find(item => item.nav?.contains(link));
    if (state) shutMenu(state);
  });
  matchMedia(MOBILE_QUERY).addEventListener('change', () => closeAllMenus());
  // 其它浮层（例如目录面板）打开时，菜单自己让位
  document.addEventListener('gintmr_ui:closeoverlays', () => closeAllMenus());
}
