import {setupNavigation} from './assets/common.js';
setupNavigation();
const cards=[...document.querySelectorAll('[data-category]')];
const status=document.getElementById('filter-status');
document.querySelectorAll('[data-filter]').forEach(btn => btn.addEventListener('click',()=>{
 const category=btn.dataset.filter;
 document.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===btn)));
 const shown=cards.filter(c=>{const v=category==='all'||c.dataset.category===category;c.hidden=!v;return v;}).length;
 status.textContent=`当前显示 ${shown} 件演示商品。`;
}));
const dialog=document.getElementById('product-dialog');let opener=null;
document.querySelectorAll('[data-view-product]').forEach(b=>b.addEventListener('click',()=>{
 opener=b;const c=b.closest('[data-name]');document.getElementById('dialog-title').textContent=c.dataset.name;
 document.getElementById('dialog-desc').textContent=c.dataset.desc;
 document.getElementById('dialog-price').textContent=c.dataset.price;
 if(typeof dialog.showModal==='function')dialog.showModal();else dialog.setAttribute('open','');
}));
document.getElementById('close-dialog').addEventListener('click',()=>{dialog.close?.();dialog.removeAttribute('open');opener?.focus();});
dialog.addEventListener('close',()=>opener?.focus());
