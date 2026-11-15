const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#navigation');
if (toggle && nav) {
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  });
  nav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    toggle.setAttribute('aria-expanded', 'false');
    nav.classList.remove('is-open');
  }));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      toggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
      toggle.focus();
    }
  });
}

// Keep the current section when moving between translations. Plain links also
// work without JavaScript; both languages share the same section identifiers.
const languageLinks = document.querySelectorAll('[data-language-link]');
function updateLanguageLinks() {
  languageLinks.forEach(link => {
    const target = new URL(link.href);
    target.hash = window.location.hash;
    link.href = target.href;
  });
}
updateLanguageLinks();
window.addEventListener('hashchange', updateLanguageLinks);
