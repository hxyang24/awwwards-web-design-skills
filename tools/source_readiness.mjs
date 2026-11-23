// Runs inside an anonymous source page. Returns bounded state hints, never code.
export function sourceReadiness(){
 const inView=r=>r.width>0&&r.height>0&&r.right>0&&r.bottom>0&&r.left<innerWidth&&r.top<innerHeight;
 const shown=el=>{const s=getComputedStyle(el);if(s.display==='none'||s.visibility==='hidden'||Number(s.opacity)<.02)return false;if(el.checkVisibility&&!el.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}))return false;return inView(el.getBoundingClientRect());};
 const unoccluded=el=>{const r=el.getBoundingClientRect(),x=Math.max(0,Math.min(innerWidth-1,r.x+r.width/2)),y=Math.max(0,Math.min(innerHeight-1,r.y+r.height/2)),hit=document.elementFromPoint(x,y);return !!hit&&(el===hit||el.contains(hit)||hit.contains(el));};
 const headings=[...document.querySelectorAll('h1,h2,[role=alert]')].filter(shown),clear=headings.filter(unoccluded);const normalize=s=>s.toLowerCase().replace(/[‘’]/g,"'").replace(/\s+/g,' ').trim();
 const texts=[document.title,...clear.map(e=>e.textContent.slice(0,300))].map(normalize);
 const loaders=[...document.querySelectorAll('[class*="loader" i],[id*="loader" i],[class*="loading" i],[aria-busy=true]')].filter(shown).filter(el=>{const s=getComputedStyle(el),r=el.getBoundingClientRect();return ['fixed','absolute'].includes(s.position)&&r.width>=innerWidth*.6&&r.height>=innerHeight*.5&&unoccluded(el);});
 const canvases=[...document.querySelectorAll('canvas')].filter(shown).slice(0,4).map(e=>{const r=e.getBoundingClientRect();return{x:Math.round(r.x),y:Math.round(r.y),width:Math.round(r.width),height:Math.round(r.height)};});
 let state='rendered_content_signals_observed';
 if(loaders.length)state='loading_incomplete';
 else if(texts.some(t=>/^(?:404(?:\s*[-|:]|$)|(?:this |the )?page (?:not found|doesn'?t exist|does not exist)|not found(?:\s*[-|:]|$))/.test(t)))state='rendered_not_found';
 else if(texts.some(t=>/^(?:(?:this |the )?page (?:couldn'?t|cannot|can'?t) load|application error|something went wrong)/.test(t)))state='rendered_error_in_observation_environment';
 else if(texts.some(t=>/^(?:(?:your |this )?browser (?:is )?not supported|unsupported browser|webgl (?:is )?not supported)/.test(t)))state='compatibility_fallback_observed';
 else if(!clear.length&&canvases.length)state='graphics_requires_visual_review';
 else if(!clear.length)state='insufficient_visible_content';
 return{state,requires_visual_review:true,title_heading_state_hint_only:true,visible_unoccluded_heading_count:clear.length,displayed_heading_count:headings.length,loading_overlay_count:loaders.length,visible_canvases:canvases,not_claimed:'Readiness hints do not certify source interaction, graphics correctness or all page states'};
}
