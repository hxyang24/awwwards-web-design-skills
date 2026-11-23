/** Original no-dependency progressive disclosure; never hides content before JS. */
export function setupReveal(root = document) {
  const nodes = [...root.querySelectorAll('[data-reveal]')];
  const media = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (!('IntersectionObserver' in window) || media.matches) {
    nodes.forEach((node) => node.classList.add('reveal-visible'));
    return () => {};
  }
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });
  nodes.forEach((node) => observer.observe(node));
  const stop = () => { observer.disconnect(); nodes.forEach((node) => node.classList.add('reveal-visible')); };
  const onchange = () => { if (media.matches) stop(); };
  media.addEventListener?.('change', onchange);
  return () => { stop(); media.removeEventListener?.('change', onchange); };
}
