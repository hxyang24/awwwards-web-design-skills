export function moneyToCents(value){
  if(!/^\d{1,9}(\.\d{1,2})?$/.test(String(value)))throw Error('Use a positive amount with at most two decimals');
  const [whole,frac='']=String(value).split('.');return Number(whole)*100+Number(frac.padEnd(2,'0'));
}
export const money=cents=>new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(cents/100);
export const products=[{id:'lamp',name:'Arc desk lamp',category:'Lighting',price:12800,stock:8,color:'#d96836'},{id:'chair',name:'Field chair',category:'Furniture',price:24900,stock:3,color:'#6c8065'},{id:'tray',name:'Stone tray',category:'Objects',price:4900,stock:12,color:'#a89580'},{id:'clock',name:'Dial clock',category:'Objects',price:7900,stock:0,color:'#c7ae6b'}];
export function setQuantity(cart,id,quantity){const p=products.find(p=>p.id===id);if(!p||!Number.isInteger(quantity)||quantity<0||quantity>p.stock)throw Error('Quantity exceeds available stock');const next={...cart};if(quantity===0)delete next[id];else next[id]=quantity;return next;}
export function totals(cart){let subtotal=0;for(const[id,n]of Object.entries(cart)){setQuantity({},id,n);subtotal+=products.find(p=>p.id===id).price*n;}const shipping=subtotal===0||subtotal>=20000?0:1200;const tax=Math.round(subtotal*0.08);return {subtotal,shipping,tax,total:subtotal+shipping+tax};}
export function checkout(cart,email,address){if(!Object.keys(cart).length)throw Error('Your bag is empty');if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)||address.trim().length<8)throw Error('Enter a valid email and complete address');return {id:'LOCAL-1001',items:{...cart},...totals(cart),status:'preview',email,address};}
export function validateTrade({quantity,price,balance=10000000,quoteAge=0,riskAccepted=false}){
  const q=Number(quantity);if(!Number.isSafeInteger(q)||q<1||q>10000)throw Error('Quantity must be 1–10,000 whole shares');
  if(!Number.isFinite(quoteAge)||quoteAge<0||!Number.isSafeInteger(balance)||balance<0)throw Error('Invalid quote age or buying power');
  if(quoteAge>15000)throw Error('Quote is stale. Refresh the quote');
  const cents=moneyToCents(price);if(cents<1)throw Error('Price must be positive');const notional=q*cents,fee=Math.max(100,Math.round(notional*0.001));
  if(notional+fee>balance)throw Error('Insufficient buying power');if(!riskAccepted)throw Error('Acknowledge the simulation risk');return {quantity:q,price:cents,notional,fee,total:notional+fee};
}
export function confirmTrade(review,current){if(review.price!==moneyToCents(current.price)||review.quantity!==Number(current.quantity)||current.quoteAge>15000||!current.riskAccepted)throw Error('Order changed. Review again');return {...review,id:'SIM-1001',status:'open',simulation:true};}
export const can=(role,action)=>role==='admin'||(role==='editor'&&action==='edit');
export function editRecord(records,id,patch,role,expectedVersion){if(!can(role,'edit'))throw Error('This role cannot edit');const old=records.find(r=>r.id===id);if(!old||old.version!==expectedVersion)throw Error('Record changed. Reload before saving');if(!patch.name?.trim()||!['Active','Review','Paused'].includes(patch.status))throw Error('Name and status are required');return records.map(r=>r.id===id?{...r,name:patch.name.trim(),status:patch.status,version:r.version+1}:r);}
export function workflowOrder(nodes,edges){const ids=new Set(nodes);if(ids.size!==nodes.length)throw Error('Duplicate node');const indegree=Object.fromEntries(nodes.map(n=>[n,0]));for(const[a,b]of edges){if(!ids.has(a)||!ids.has(b))throw Error('Unknown node');indegree[b]++;}const queue=nodes.filter(n=>!indegree[n]),result=[];while(queue.length){const n=queue.shift();result.push(n);for(const[a,b]of edges)if(a===n&&!--indegree[b])queue.push(b);}if(result.length!==nodes.length)throw Error('Workflow contains a cycle');return result;}
export function agentTransition(state,event){const allowed={idle:{start:'running'},running:{tool:'awaiting_approval',stop:'stopped',error:'failed',complete:'completed'},awaiting_approval:{approve:'running',deny:'stopped',stop:'stopped'},failed:{retry:'running'},stopped:{start:'running'},completed:{start:'running'}};const next=allowed[state]?.[event];if(!next)throw Error('Invalid agent transition: '+state+'/'+event);return next;}
export function escapeHTML(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
