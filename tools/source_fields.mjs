// Observe native fields together with visible associated labels. An invisible
// native field is not evidence that its user-facing affordance is absent.
export async function observeSourceFields(page,{limit=80}={}){
 if(!Number.isInteger(limit)||limit<1||limit>200)throw Error('Field limit must be 1–200');
 return page.evaluate(max=>{
  const visible=el=>{const r=el.getBoundingClientRect(),s=getComputedStyle(el);return r.width>0&&r.height>0&&s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity)>0&&(!el.checkVisibility||el.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}));};
  const fields=[...document.querySelectorAll('input:not([type=hidden]),select,textarea')],trim=s=>(s||'').trim().replace(/\s+/g,' ').slice(0,160);
  return{observed_native_fields:fields.length,truncated:fields.length>max,not_claimed:'A visible associated label does not prove enabled, unobscured, unique or working interaction; inspect it before use',fields:fields.slice(0,max).map(el=>{
   const labels=[...el.labels||[]].slice(0,8).map(label=>({text:trim(label.textContent),visible:visible(label),for:label.htmlFor||null}));
   return{tag:el.tagName.toLowerCase(),id:el.id.slice(0,120),name:el.name.slice(0,120),type:el.type,disabled:el.disabled,native_visible:visible(el),associated_labels:labels,visible_label_affordance:labels.some(l=>l.visible),checked:['checkbox','radio'].includes(el.type)?el.checked:undefined,options:el instanceof HTMLSelectElement?[...el.options].slice(0,40).map(o=>({text:trim(o.text),disabled:o.disabled,selected:o.selected})):undefined};
  })};
 },limit);
}
