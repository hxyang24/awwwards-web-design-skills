import {escapeHTML as e} from './domain.mjs';
export {e};
export const head=(kicker,title,description,action='')=>`<section class="pagehead"><div><div class="eyebrow">${e(kicker)}</div><h1 tabindex="-1">${e(title)}</h1><p>${e(description)}</p></div>${action}</section>`;
export const empty=text=>`<div class="empty">${e(text)}</div>`;
export function mount(config){
 document.body.className=config.theme||'';
 let current='';const app={route:()=>decodeURIComponent(location.hash.slice(1)||config.nav[0][0]),notice:(message,error=false)=>{const el=document.querySelector('#status');el.hidden=false;el.className='notice'+(error?' error':'');el.textContent=message;},draw:()=>{
  config.cleanup?.();const route=app.route();document.title=config.brand+' · '+(config.nav.find(([id])=>id===route)?.[1]||route);
  document.querySelector('#app').innerHTML=`<div class="preview">LOCAL DEMO · Fictional data · No external actions or live transactions</div><div class="shell"><aside><div><a class="brand" href="../">${e(config.brand)}<span> /</span></a><div class="edition">${e(config.edition||'Design system · V2.0')}</div></div><nav aria-label="Main navigation">${config.nav.map(([id,label])=>`<a href="#${id}" ${route===id?'aria-current="page"':''}>${e(label)}</a>`).join('')}</nav><div class="navfoot">Awwwards Skills V2<br>Original interface laboratory<br><a href="../">All templates ↗</a></div></aside><div class="workspace"><header class="topbar"><span class="crumb">${e(config.breadcrumb||'Workspace')} / ${e(config.nav.find(([id])=>id===route)?.[1]||route)}</span><div class="row"><span class="tiny muted">Local session</span><span class="avatar" aria-label="Demo user">JD</span></div></header><main id="main"><div id="status" role="status" aria-live="polite" hidden></div>${config.render(route,app)}</main></div></div>`;
  config.after?.(route,app);if(current&&current!==route){document.querySelector('h1')?.focus();window.scrollTo(0,0);}current=route;
 }};
 const invoke=(fn,event)=>{try{const result=fn?.(event,app);if(result?.catch)result.catch(err=>app.notice(err.message,true));}catch(err){app.notice(err.message,true);}};
 document.addEventListener('click',event=>{const target=event.target.closest('[data-action]');if(target){event.action=target.dataset.action;event.control=target;invoke(config.click,event);}});
 document.addEventListener('submit',event=>{if(event.target.closest('#app')){event.preventDefault();invoke(config.submit,event);}});
 document.addEventListener('change',event=>invoke(config.change,event));
 window.addEventListener('hashchange',app.draw);app.draw();return app;
}
export function showDialog(id){const d=document.getElementById(id);d.showModal();}
export function closeDialog(id){document.getElementById(id)?.close();}
export const bars=()=>`<div class="bars" role="img" aria-label="Fictional weekly activity chart: rising from 42 to 94"><i style="height:42%"></i><i style="height:60%"></i><i style="height:55%"></i><i style="height:74%"></i><i style="height:62%"></i><i style="height:84%"></i><i style="height:94%"></i></div>`;
