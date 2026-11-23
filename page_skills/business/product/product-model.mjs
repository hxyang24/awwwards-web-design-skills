const ids=(items,allowed)=>Array.isArray(items)&&items.length===allowed.length&&new Set(items.map(x=>x.id)).size===items.length&&allowed.every(id=>items.some(x=>x.id===id));
const text=x=>typeof x==='string'&&x.length>0&&x.length<=240;
const cents=x=>Number.isSafeInteger(x)&&x>=0&&x<=10000000;
export function parseProduct(value){
 if(!value||value.schema_version!==1||value.id!=='arc-lamp'||value.currency!=='USD'||!text(value.title)||!text(value.notice)||!text(value.standard_lead)||!text(value.express_lead)||!cents(value.express_fee_cents)||!ids(value.colors,['sand','chalk','ink'])||!ids(value.sizes,['small','regular']))throw Error('Product data is unavailable or unsupported');
 for(const s of value.sizes)if(!text(s.label)||!cents(s.unit_cents))throw Error('Invalid size data');
 for(const c of value.colors)if(!text(c.label)||!/^#[0-9a-f]{6}$/i.test(c.hex)||!c.stock||!value.sizes.every(s=>c.stock[s.id]===null||Number.isSafeInteger(c.stock[s.id])&&c.stock[s.id]>=0&&c.stock[s.id]<=10000))throw Error('Invalid color or availability data');
 return structuredClone(value);
}
export function estimate(product,{color,size,quantity,express},{adjustmentCents=0}={}){
 const c=product.colors.find(x=>x.id===color),s=product.sizes.find(x=>x.id===size);
 if(!c||!s||typeof express!=='boolean')return{ok:false,code:'selection',message:'Choose an available color and size.'};
 // Do not coerce empty, exponential, decimal or signed text into a quantity.
 if(typeof quantity!=='string'||!/^\d$/.test(quantity)||Number(quantity)<1||Number(quantity)>5)return{ok:false,code:'quantity',message:'Enter a whole quantity from 1 to 5.'};
 if(!Number.isSafeInteger(adjustmentCents)||Math.abs(adjustmentCents)>1000000||s.unit_cents+adjustmentCents<0)throw Error('Invalid preview price adjustment');
 const q=Number(quantity),stock=c.stock[size];
 if(stock===null)return{ok:false,code:'unknown_stock',message:'Availability is unknown. Choose Sand to continue the local estimate.'};
 if(stock===0)return{ok:false,code:'sold_out',message:'This selection is unavailable. Choose Sand to continue the local estimate.'};
 if(q>stock)return{ok:false,code:'insufficient_stock',message:'Only '+stock+' are available in the fictional stock sample.'};
 const unit=s.unit_cents+adjustmentCents,subtotal=unit*q,expressFee=express?product.express_fee_cents:0;
 return{ok:true,color:c.id,colorLabel:c.label,size:s.id,sizeLabel:s.label,quantity:q,express,unit_cents:unit,subtotal_cents:subtotal,express_fee_cents:expressFee,known_total_cents:subtotal+expressFee,tax_cents:null,delivery_cents:null,final_total_cents:null,lead:express?product.express_lead:product.standard_lead,currency:product.currency};
}
export function formatMoney(cents){if(!Number.isSafeInteger(cents)||cents<0)throw Error('Money requires nonnegative integer cents');return '$'+(cents/100).toFixed(2);}
export function createLocalQuoteAdapter(product){
 let delay=120,fail=false,adjustmentCents=0;
 return{setDelay(ms){if(!Number.isInteger(ms)||ms<0||ms>10000)throw Error('Invalid delay');delay=ms;},failNext(){fail=true;},setAdjustment(cents){if(!Number.isSafeInteger(cents)||Math.abs(cents)>1000000)throw Error('Invalid adjustment');adjustmentCents=cents;},quote(selection,{signal}={}){
  const shouldFail=fail;fail=false;const change=adjustmentCents;
  return new Promise((resolve,reject)=>{
   if(signal?.aborted){reject(new DOMException('Aborted','AbortError'));return;}
   let timer;const aborted=()=>{clearTimeout(timer);reject(new DOMException('Aborted','AbortError'));};signal?.addEventListener('abort',aborted,{once:true});
   timer=setTimeout(()=>{signal?.removeEventListener('abort',aborted);if(shouldFail){reject(Error('Local estimate could not load. Try again with your selection preserved.'));return;}try{resolve(estimate(product,selection,{adjustmentCents:change}));}catch(e){reject(e);}},delay);
  });
 }};
}
