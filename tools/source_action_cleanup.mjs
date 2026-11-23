// Escape is page input: never send it merely because a source action finished.
export async function cleanupSourceAction(page,before,after,explicitEscape=false,{preserveOpen=false}={}){
 if(typeof preserveOpen!=='boolean')throw Error('preserveOpen must be an explicit boolean');
 // Preservation is opt-in for an inspected, dependent sequence. An explicit
 // close still takes precedence. Default isolated-action behavior is retained.
 if(preserveOpen&&!explicitEscape)return{key_sent:false,reason:'preserved_for_next_action'};
 if(!explicitEscape&&!(Number.isInteger(before.dialogs)&&Number.isInteger(after.dialogs)&&after.dialogs>before.dialogs))return{key_sent:false};
 await page.keyboard.press('Escape');await page.waitForTimeout(220);
 const visible=await page.evaluate(()=>[...document.querySelectorAll('dialog,[role=dialog]')].filter(el=>{const r=el.getBoundingClientRect(),s=getComputedStyle(el);return r.width>0&&r.height>0&&s.visibility!=='hidden'&&s.display!=='none'&&(!el.checkVisibility||el.checkVisibility({checkOpacity:true,checkVisibilityCSS:true}));}).length);
 return{key_sent:true,url_after:page.url(),reason:explicitEscape?'explicit_plan':'newly_opened_dialog',visible_dialogs_after:visible,dialog_count_decreased:Number.isInteger(after.dialogs)?visible<after.dialogs:null};
}
