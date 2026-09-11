(() => {
  const screens = [...document.querySelectorAll('.screen')];
  let current = 0;
  const show = (index) => {
    current = Math.max(0, Math.min(screens.length - 1, index));
    screens.forEach((s, i) => s.classList.toggle('active', i === current));
    const id = screens[current]?.dataset.screen;
    if (id && location.hash !== `#${id}`) history.replaceState(null, '', `#${id}`);
  };
  const fromHash = () => {
    const id = location.hash.replace('#', '');
    const idx = screens.findIndex(s => s.dataset.screen === id);
    show(idx >= 0 ? idx : 0);
  };
  addEventListener('keydown', (e) => {
    if (['ArrowRight','ArrowDown','PageDown',' '].includes(e.key)) show(current + 1);
    if (['ArrowLeft','ArrowUp','PageUp'].includes(e.key)) show(current - 1);
  });
  addEventListener('hashchange', fromHash);
  fromHash();
})();
