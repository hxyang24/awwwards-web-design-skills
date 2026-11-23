// Resolve a previously inspected source control without choosing an ambiguous
// first match. The returned Locator stays strict if the DOM changes later.
const cssString=value=>Array.from(value).map(c=>/[a-zA-Z0-9/_\-.?=#%:&]/.test(c)?c:'\\'+c.codePointAt(0).toString(16)+' ').join('');
export async function resolveSourceTarget(page,action,{timeout=7000}={}){
 if(!['button','link','tab','textbox','summary','selector'].includes(action.role)||typeof action.name!=='string'||!action.name||action.name.length>80)throw Error('Name a previously inspected source control');
 const selector=action.role==='selector'||action.role==='textbox'&&action.selector;
 if(selector&&(typeof action.selector!=='string'||!action.selector||action.selector.length>120))throw Error('A bounded inspected selector is required');
 let candidates=(selector?page.locator(action.selector):action.role==='summary'?page.locator('summary').filter({hasText:action.name}):page.getByRole(action.role,{name:action.name,exact:true})).filter({visible:true});
 // first() is used only to await availability, never as the returned target.
 await candidates.first().waitFor({state:'visible',timeout});const before=await candidates.count();if(before>50)throw Error('Too many source-control candidates; inspect a narrower selector');
 let method=selector?'inspected_selector':'role_and_name';
 if(action.expected_href!==undefined){
  if(typeof action.expected_href!=='string'||!action.expected_href||action.expected_href.length>2048)throw Error('Expected href must be a bounded inspected URL');
  const expected=new URL(action.expected_href,page.url());if(!['http:','https:'].includes(expected.protocol)||expected.username||expected.password)throw Error('Expected href must be credential-free HTTP(S)');
  const matches=await candidates.evaluateAll((els,url)=>els.filter(el=>el instanceof HTMLAnchorElement&&el.href===url).map(el=>el.getAttribute('href')),expected.href);
  if(matches.length!==1||matches[0]===null||matches[0].includes('\0'))throw Error('Expected href did not identify one visible source link');
  candidates=candidates.and(page.locator('[href="'+cssString(matches[0])+'"]'));method+='_and_expected_href';
 }
 const count=await candidates.count();if(count!==1)throw Error('Ambiguous source control: '+count+' visible matches; provide an inspected unique selector or expected href');
 return{locator:candidates,method,visible_candidates_before_href:before,visible_candidates_resolved:count};
}
