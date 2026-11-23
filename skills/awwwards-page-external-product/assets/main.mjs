import {parseProduct,formatMoney,createLocalQuoteAdapter} from './product-model.mjs';
const $=selector=>document.querySelector(selector),all=selector=>[...document.querySelectorAll(selector)];
const form=$('#product-form'),configuration=$('#configuration'),viewer=$('#viewer'),reviewDialog=$('#review-dialog'),figures=all('#view-stage figure'),views=['Front view','Side view','Surface detail'];
let product,adapter,quote,request,dataRequest,requestNumber=0,view=0,phase='loading_data',disposed=false,dataTimer;
const listeners=[];
function on(el,type,fn){el.addEventListener(type,fn);listeners.push(()=>el.removeEventListener(type,fn));}
const selection=()=>({color:form.elements.color.value,size:form.elements.size.value,quantity:form.elements.quantity.value,express:form.elements.express.checked});
const tell=text=>{$('#selection-status').textContent=text;};
function rows(target,values){target.replaceChildren();for(const [term,value]of values){const group=document.createElement('div'),dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=term;dd.textContent=value;group.append(dt,dd);target.append(group);}}
function values(q){return[['Finish',q.colorLabel],['Size',q.sizeLabel],['Quantity',String(q.quantity)],['Product amount',formatMoney(q.subtotal_cents)],['Express preparation',formatMoney(q.express_fee_cents)],['Known estimate',formatMoney(q.known_total_cents)+' USD'],['Preparation',q.lead]];}
function paintGallery(){
 const color=product?.colors.find(c=>c.id===selection().color)||{label:'Sand',hex:'#c9aa83'};document.documentElement.style.setProperty('--lamp',color.hex);
 figures.forEach((figure,i)=>{figure.hidden=i!==view;figure.querySelector('[role=img]').setAttribute('aria-label','Original illustration of the '+color.label+' Arc lamp, '+views[i].toLowerCase());figure.querySelector('figcaption').textContent=views[i]+' · '+color.label;});
 all('[data-show]').forEach(button=>button.setAttribute('aria-pressed',String(Number(button.dataset.show)===view)));
 $('#gallery-status').textContent='View '+(view+1)+' of 3 · '+views[view]+'. No automatic rotation.';
 if(viewer.open){const art=figures[view].querySelector('.art').cloneNode(true);$('#enlarged-art').replaceChildren(art);$('#viewer-caption').textContent=views[view]+' · '+color.label+' · '+(view+1)+' of 3';}
}
function showView(index){view=(index+figures.length)%figures.length;paintGallery();}
function invalidate(){
 request?.abort();request=null;requestNumber++;quote=null;phase='editing';$('#review').disabled=true;$('#calculate').disabled=false;$('#estimate').hidden=true;form.elements.quantity.removeAttribute('aria-invalid');
 if(reviewDialog.open)reviewDialog.close();tell('Selection changed. Calculate a new local estimate.');
 const c=product.colors.find(c=>c.id===selection().color),stock=c?.stock[selection().size];$('#color-name').textContent=c?.label||'Unknown';
 $('#availability').textContent=stock===null?'Availability is unknown in this sample.':stock===0?'Unavailable in this sample.':stock+' available in the fictional stock sample.';paintGallery();
}
async function calculate(event){
 event?.preventDefault();if(disposed||!adapter)return;request?.abort();const controller=new AbortController(),number=++requestNumber;request=controller;quote=null;phase='loading';$('#estimate').hidden=true;$('#calculate').disabled=true;$('#review').disabled=true;tell('Calculating a local estimate…');
 try{
  const result=await adapter.quote(selection(),{signal:controller.signal});if(disposed||number!==requestNumber)return;
  if(!result.ok){phase='invalid';tell(result.message);if(result.code==='quantity')form.elements.quantity.setAttribute('aria-invalid','true');$('#selection-status').focus();return;}
  quote=result;phase='estimated';rows($('#estimate-values'),values(quote));$('#estimate').hidden=false;$('#review').disabled=false;
  const base=product.sizes.find(s=>s.id===quote.size).unit_cents;tell((quote.unit_cents!==base?'The local sample price was updated. ':'')+'Known estimate ready. Tax, delivery and final payable total remain unknown.');
 }catch(e){if(e.name==='AbortError'||disposed||number!==requestNumber)return;phase='error';tell(e.message);$('#selection-status').focus();}
 finally{if(!disposed&&number===requestNumber){$('#calculate').disabled=false;request=null;}}
}
async function loadProduct(){
 if(disposed)return;dataRequest?.abort();const controller=new AbortController();dataRequest=controller;phase='loading_data';$('#retry-data').hidden=true;$('#enhancement-status').textContent='Loading optional local selection controls…';dataTimer=setTimeout(()=>controller.abort(),7000);
 try{const response=await fetch('./product.json',{signal:controller.signal});if(!response.ok)throw Error('Product data request failed');const value=parseProduct(await response.json());if(disposed)return;
  product=value;adapter=createLocalQuoteAdapter(product);$('#product-title').textContent=product.title;document.body.classList.add('enhanced');configuration.disabled=false;all('[data-show],#enlarge').forEach(b=>b.disabled=false);$('#enhancement-status').textContent='Local selection controls ready. Estimates use a fictional stock sample.';
  for(const color of product.colors){const input=form.querySelector('input[name=color][value='+color.id+']');input.parentElement.querySelector('span:last-child').textContent=color.label;input.parentElement.querySelector('.swatch').style.backgroundColor=color.hex;}
  for(const size of product.sizes)form.querySelector('option[value='+size.id+']').textContent=size.label;
  invalidate();phase='ready';tell('Choose your options, then calculate a local estimate.');
 }catch(e){if(disposed)return;phase='data_error';configuration.disabled=true;document.body.classList.remove('enhanced');figures.forEach(f=>f.hidden=false);all('[data-show],#enlarge').forEach(b=>b.disabled=true);$('#enhancement-status').textContent='Selection controls could not load. All original views, specifications and example prices remain readable.';$('#retry-data').hidden=false;}
 finally{clearTimeout(dataTimer);if(dataRequest===controller)dataRequest=null;}
}
on(form,'submit',calculate);
const changed=()=>{if(product&&!disposed)invalidate();};on(form,'input',changed);on(form,'change',changed);
all('[data-show]').forEach(button=>on(button,'click',()=>showView(Number(button.dataset.show))));
on($('#enlarge'),'click',()=>{viewer.showModal();paintGallery();});on($('#close-viewer'),'click',()=>viewer.close());
on($('#previous-view'),'click',()=>showView(view-1));on($('#next-view'),'click',()=>showView(view+1));
on(viewer,'keydown',event=>{if(event.key==='ArrowRight'||event.key==='ArrowLeft'){event.preventDefault();showView(view+(event.key==='ArrowRight'?1:-1));}});
on($('#review'),'click',()=>{if(!quote||disposed)return;rows($('#review-values'),values(quote));reviewDialog.showModal();phase='review';});
on($('#close-review'),'click',()=>reviewDialog.close());on(reviewDialog,'close',()=>{if(!disposed&&quote&&phase==='review')phase='estimated';});
on($('#save-selection'),'click',()=>{if(!quote||disposed)return;reviewDialog.close();phase='saved';tell('Local selection saved in this page only. No order, reservation or payment was created.');$('#selection-status').focus();});
on($('#retry-data'),'click',loadProduct);
function dispose(){
 if(disposed)return;disposed=true;requestNumber++;request?.abort();dataRequest?.abort();clearTimeout(dataTimer);listeners.splice(0).forEach(remove=>remove());
 if(viewer.open)viewer.close();if(reviewDialog.open)reviewDialog.close();configuration.disabled=true;all('[data-show],#enlarge,#retry-data').forEach(b=>b.disabled=true);document.body.classList.remove('enhanced');figures.forEach(f=>f.hidden=false);phase='disposed';$('#enhancement-status').textContent='Interactive controls are closed. All original views and product information remain readable.';tell('No active local estimate.');$('#estimate').hidden=true;
}
window.__pageSkill={id:'external-product',kind:'product',businessMode:'local_preview'};
window.__productStudy={info:()=>({phase,view,selection:selection(),quote:quote?structuredClone(quote):null,disposed}),failNext:()=>adapter?.failNext(),setDelay:ms=>adapter?.setDelay(ms),adjustPrice:cents=>{adapter?.setAdjustment(cents);if(product)invalidate();},dispose};
loadProduct();
