import{panels,panelLabels,parseProduct,defaults,readRoute,route,dimension,metric,plan,brief}from'./model.mjs';
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const ownedDownloads=new Map();
let product,state,controller,disposed=false,ready=false,generation=0,returnFocus,briefURL=null;
const original=$('.information').innerHTML,originalElevation=$('#elevation').outerHTML,originalCaption=$('#caption').textContent;
const listeners=[];function on(target,event,fn){target.addEventListener(event,fn);listeners.push(()=>target.removeEventListener(event,fn));}
function revoke(){if(briefURL){URL.revokeObjectURL(briefURL);briefURL=null;}$('#brief-download').removeAttribute('href');$('#brief-download').hidden=true;}
function invalidate(){revoke();$('#brief-preview').hidden=true;$('#brief-preview').textContent='';$('#brief-status').textContent='Enter or edit the project details, then prepare a new local brief.';}
function close(){if($('#brief-dialog').open)$('#brief-dialog').close();}
function sync({focus=false,historyMode=null}={}){
 const active=panels.includes(state.tab)?state.tab:'specification';
 for(const a of $$('[data-tab]')){const yes=a.dataset.tab===active;a.setAttribute('aria-selected',String(yes));a.tabIndex=yes?0:-1;$('#technical-'+a.dataset.tab).hidden=!yes;}
 for(const name of ['finish','layout'])for(const radio of $$('input[name='+name+']'))radio.checked=radio.value===state[name];$('#unit').value=state.unit;
 for(const dd of $$('[data-dimension]'))dd.textContent=dimension(product.dimensions[dd.dataset.dimension],state.unit);
 const finish=product.finishes.find(x=>x.id===state.finish),layout=product.layouts.find(x=>x.id===state.layout),elevation=$('#elevation');
 elevation.style.setProperty('--finish',finish.color);elevation.classList.toggle('corner',layout.turn===90);elevation.replaceChildren(...Array.from({length:layout.panels},()=>document.createElement('span')));elevation.setAttribute('aria-label','Original illustration: '+finish.label+' · '+layout.label);
 $('#caption').textContent=finish.label+' · '+layout.label+' · symbolic illustration';
 const svg=$('#plan'),g=document.createElementNS('http://www.w3.org/2000/svg','g');g.setAttribute('stroke','currentColor');g.setAttribute('stroke-width','7');
 for(const line of plan(layout)){const el=document.createElementNS(svg.namespaceURI,'line');for(const[k,v]of Object.entries(line))el.setAttribute(k,v);g.append(el);}svg.replaceChildren(g);svg.setAttribute('aria-label','Original '+layout.label+' plan, not to scale');$('#plan-caption').textContent=layout.label+' · not to scale';
 if(historyMode)history[historyMode+'State'](null,'',route(state));
 if(focus)document.querySelector('[data-tab="'+active+'"]').focus();
}
function selectTab(tab,{focus=true,historyMode='push'}={}){state={...state,tab};sync({focus,historyMode});}
function navigate(){if(!ready||disposed)return;const parsed=readRoute(product,location.search,location.hash,{fallbackTab:state.tab});state=parsed.state;const hiddenFocus=$('.panel:not([hidden])')?.contains(document.activeElement);close();invalidate();sync({focus:hiddenFocus});$('#status').textContent=parsed.warnings.join(' ')||'Information panel and study selections restored from this link.';}
function triggerDownload(text,name){const url=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();const timer=setTimeout(()=>{URL.revokeObjectURL(url);ownedDownloads.delete(url);},1000);ownedDownloads.set(url,timer);}
function enhance(){
 const nav=$('#panel-nav');nav.setAttribute('role','tablist');nav.setAttribute('aria-label','Product information');
 for(const a of $$('[data-tab]')){a.id='tab-'+a.dataset.tab;a.setAttribute('role','tab');a.setAttribute('aria-controls','technical-'+a.dataset.tab);const panel=$('#technical-'+a.dataset.tab);panel.setAttribute('role','tabpanel');panel.setAttribute('aria-labelledby',a.id);}
 for(const input of $$('.information input,.information select'))input.disabled=false;$('#review').disabled=false;
 on(nav,'click',e=>{const a=e.target.closest('[data-tab]');if(!a||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;e.preventDefault();selectTab(a.dataset.tab);});
 on(nav,'keydown',e=>{const a=e.target.closest('[data-tab]');if(!a)return;let i=panels.indexOf(a.dataset.tab);if(e.key==='ArrowRight')i=(i+1)%4;else if(e.key==='ArrowLeft')i=(i+3)%4;else if(e.key==='Home')i=0;else if(e.key==='End')i=3;else if(e.key===' '){e.preventDefault();selectTab(a.dataset.tab);return;}else return;e.preventDefault();selectTab(panels[i],{historyMode:'replace'});});
 on($('.information'),'change',e=>{const t=e.target,key=t.name==='finish'?'finish':t.name==='layout'?'layout':t.id==='unit'?'unit':null;if(!key)return;state={...state,[key]:t.value};invalidate();sync({historyMode:'replace'});$('#status').textContent='Local study updated. Performance evidence and unknown values are unchanged.';});
 on($('#review'),'click',()=>{returnFocus=document.activeElement;invalidate();$('#brief-dialog').showModal();$('#project').focus();});
 on($('#close-brief'),'click',close);on($('#brief-dialog'),'close',()=>{if(returnFocus?.isConnected&&!disposed)returnFocus.focus();});
 on($('#brief-form'),'input',invalidate);
 on($('#brief-form'),'submit',e=>{e.preventDefault();if(!$('#brief-form').reportValidity()||!$('#project').value.trim()){$('#brief-status').textContent='Enter a project name.';$('#project').focus();return;}invalidate();const text=brief(product,state,{project:$('#project').value,notes:$('#notes').value});$('#brief-preview').textContent=text;$('#brief-preview').hidden=false;briefURL=URL.createObjectURL(new Blob([text],{type:'text/plain;charset=utf-8'}));$('#brief-download').href=briefURL;$('#brief-download').hidden=false;$('#brief-status').textContent='Brief prepared on this device. No message or quote request was sent.';});
 on($('#sheet'),'click',e=>{if(!ready||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;e.preventDefault();triggerDownload(brief(product,state),'folio-concept-sheet.txt');});
 on(window,'popstate',navigate);on(window,'hashchange',navigate);
}
async function start(){
 const run=++generation;controller?.abort();controller=new AbortController();$('#status').textContent='All original information remains available below while optional controls load.';$('#retry').hidden=true;
 try{const response=await fetch('product.json',{signal:controller.signal});if(!response.ok)throw Error('Data unavailable');if(Number(response.headers.get('content-length'))>1048576)throw Error('Data too large');const text=await response.text();if(text.length>1048576)throw Error('Data too large');const sha=[...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(text)))].map(x=>x.toString(16).padStart(2,'0')).join('');if(sha!==$('meta[name=study-data-sha256]').content)throw Error('Regenerate static content');const parsed=parseProduct(JSON.parse(text));if(disposed||run!==generation)return;
 product=parsed;const restored=readRoute(product,location.search,location.hash);state=restored.state;
 // The static renderer owns the content. Refuse a drifted schema rather than hiding missing sections.
 if(product.finishes.some(x=>!$$('[name=finish]').some(el=>el.value===x.id))||product.layouts.some(x=>!$$('[name=layout]').some(el=>el.value===x.id))||product.performance.some(x=>!document.querySelector('[data-metric="'+x.id+'"]')))throw Error('Regenerate the static sections after data edits');
 $('#title').textContent=product.title;$('#summary').textContent=product.summary;
 for(const x of product.performance)$('[data-metric="'+x.id+'"]').textContent=metric(x);
 ready=true;enhance();sync();window.__pageSkill={id:'external-technical-product',dispose};$('#status').textContent=restored.warnings.join(' ')||'Choose an information panel. Selections and downloads stay on this device.';
 }catch(error){if(disposed||run!==generation||error.name==='AbortError')return;ready=false;$('#status').textContent='Optional controls are unavailable. Read all four sections and download the static sheet below. Retry after checking data and regenerating static content.';$('#retry').hidden=false;}
}
on($('#retry'),'click',start);
export function dispose(){if(disposed)return;disposed=true;ready=false;generation++;controller?.abort();close();revoke();for(const[url,timer]of ownedDownloads){clearTimeout(timer);URL.revokeObjectURL(url);}ownedDownloads.clear();for(const off of listeners.splice(0))off();$('.information').innerHTML=original;$('#elevation').outerHTML=originalElevation;$('#caption').textContent=originalCaption;$('#review').disabled=true;}
window.folioStudy={dispose};start();
