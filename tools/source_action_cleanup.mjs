// Escape is page input: never send it merely because a source action finished.
export async function cleanupSourceAction(page,before,after,explicitEscape=false){
 if(!explicitEscape&&!(Number.isInteger(before.dialogs)&&Number.isInteger(after.dialogs)&&after.dialogs>before.dialogs))return{key_sent:false};
 await page.keyboard.press('Escape');await page.waitForTimeout(220);return{key_sent:true,url_after:page.url(),reason:explicitEscape?'explicit_plan':'newly_opened_dialog'};
}
