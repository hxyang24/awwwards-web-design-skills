/** Progressive navigation; in the absence of JavaScript, all links remain visible. */
export function setupNavigation(root = document) {
 const toggle = root.getElementById('menu-toggle');
 const nav = root.getElementById('primary-nav');
 if (!toggle || !nav) return () => {};
 if (nav.dataset.bound === 'true') return () => {};
 nav.dataset.bound = 'true';
 const mobile = window.matchMedia('(max-width: 720px)');
 let isOpen = false;
 const apply = () => {
   if (!mobile.matches) {
     nav.hidden = false; nav.removeAttribute('data-enhanced'); toggle.classList.remove('is-enhanced');
     toggle.hidden = true;toggle.setAttribute('aria-expanded','false');isOpen = false;
     if(nav.contains(document.activeElement))document.activeElement.blur();
   } else {
     toggle.hidden = false;toggle.classList.add('is-enhanced');nav.dataset.enhanced = 'true';nav.hidden = !isOpen;
     toggle.setAttribute('aria-expanded', String(isOpen));
     if (!isOpen && nav.contains(document.activeElement)) toggle.focus();
   }
 };
 const toggleClick = () => { isOpen = !isOpen; apply(); if (isOpen) nav.querySelector('a')?.focus(); };
 const keydown = e => { if (e.key === 'Escape' && mobile.matches && isOpen) {isOpen=false;apply();toggle.focus();} };
 const navClick = e => { if (e.target.closest('a') && mobile.matches) {isOpen=false;apply();} };
 toggle.addEventListener('click',toggleClick); nav.addEventListener('click',navClick);document.addEventListener('keydown',keydown);mobile.addEventListener?.('change',apply);apply();
 return () => { toggle.removeEventListener('click',toggleClick);nav.removeEventListener('click',navClick);document.removeEventListener('keydown',keydown);mobile.removeEventListener?.('change',apply);delete nav.dataset.bound;delete nav.dataset.enhanced;nav.hidden=false;toggle.hidden=true;toggle.classList.remove('is-enhanced'); };
}
/** Explicitly a local UI preview: does not transmit or persist personal data. */
export function setupPreviewForm(root = document) {
 const form=root.getElementById('contact-form');const notice=root.getElementById('form-status');
 if (!form || !notice) return () => {};
 const edit=()=>{notice.textContent='';};
 const submit=(event)=>{event.preventDefault();notice.textContent='';if (!form.reportValidity()) {notice.textContent='请填写有效的信息后再试。';return;}notice.textContent='演示完成：当前为本地预览，未发送申请，也未保存个人资料。';};
 form.addEventListener('input',edit); form.addEventListener('change',edit);form.addEventListener('submit',submit);
 return ()=>{form.removeEventListener('input',edit);form.removeEventListener('change',edit);form.removeEventListener('submit',submit);};
}
