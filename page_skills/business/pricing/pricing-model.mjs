// Original demonstration tariff. No provider prices or source billing code.
export const tariff=Object.freeze({version:'field-demo-1',currency:'USD',cpuMicroPerSecond:5,memoryMicroPerSecond:2,storageCentsPerGBMonth:4,freeStorageGB:10});
export const hardware=Object.freeze({cpu:{label:'CPU only',microPerSecond:0},aster:{label:'Aster / fictional accelerator',microPerSecond:200},orion:{label:'Orion / fictional accelerator',microPerSecond:350}});
export const plans=Object.freeze({seed:{label:'Seed',baseCents:0},studio:{label:'Studio',baseCents:2400},custom:{label:'Custom',baseCents:null}});
const own=(o,k)=>Object.prototype.hasOwnProperty.call(o,k);
const rules={requests:[0,10000000,0,'Enter a whole request count from 0 to 10,000,000.'],runtime:[0,3600,3,'Enter seconds from 0 to 3,600, with at most three decimal places.'],gpus:[1,8,0,'Choose 1 to 8 accelerators.'],cpus:[1,64,0,'Enter 1 to 64 whole vCPUs.'],memory:[1,256,0,'Enter 1 to 256 whole GB of memory.'],storage:[0,100000,2,'Enter 0 to 100,000 GB, with at most two decimal places.']};
function parse(value,rule){const [min,max,digits]=rule,s=String(value??'').trim(),pattern=digits?new RegExp('^\\d+(?:\\.\\d{1,'+digits+'})?$'):/^\d+$/;if(s.length>20||!pattern.test(s))return null;const [a,b='']=s.split('.'),scale=10n**BigInt(digits),v=BigInt(a)*scale+BigInt(b.padEnd(digits,'0')||'0');return v<BigInt(min)*scale||v>BigInt(max)*scale?null:v;}
export function estimate(input){const errors={},values={};for(const key of ['plan','hardware'])if(!own(key==='plan'?plans:hardware,input[key]))errors[key]='Choose an available '+key+'.';
 for(const [key,rule] of Object.entries(rules)){if(key==='gpus'&&input.hardware==='cpu'){values.gpus=0n;continue;}const value=parse(input[key],rule);if(value===null)errors[key]=rule[3];else values[key]=value;}
 if(Object.keys(errors).length)return{ok:false,errors};
 // Round each aggregate monthly component once, half up to cents. Never round
 // a displayed per-second price and multiply that rounded display value.
 const duration=values.requests*values.runtime,rounded=(n,d)=>(n+d/2n)/d;
 const gpu=rounded(duration*BigInt(hardware[input.hardware].microPerSecond)*values.gpus,10000000n),cpu=rounded(duration*BigInt(tariff.cpuMicroPerSecond)*values.cpus,10000000n),memory=rounded(duration*BigInt(tariff.memoryMicroPerSecond)*values.memory,10000000n),billable=values.storage-BigInt(tariff.freeStorageGB)*100n,storage=rounded((billable>0n?billable:0n)*BigInt(tariff.storageCentsPerGBMonth),100n),usage=gpu+cpu+memory+storage,base=plans[input.plan].baseCents;
 return{ok:true,errors:{},version:tariff.version,plan:input.plan,hardware:input.hardware,components:{gpu,cpu,memory,storage},usage,base:base===null?null:BigInt(base),total:base===null?null:usage+BigInt(base),runtimeMilliseconds:values.runtime,requests:values.requests};
}
export function money(cents){if(cents===null)return'Custom quote required';if(typeof cents!=='bigint'||cents<0n)throw Error('Nonnegative integer cents required');return'$'+(cents/100n).toLocaleString('en-US')+'.'+String(cents%100n).padStart(2,'0');}
export function rate(microPerSecond,basis){if(!Number.isSafeInteger(microPerSecond)||microPerSecond<0||!['second','hour'].includes(basis))throw Error('Invalid rate basis');const value=BigInt(microPerSecond)*BigInt(basis==='hour'?3600:1),digits=String(value%1000000n).padStart(6,'0').replace(/0+$/,'')||'00';return'$'+(value/1000000n)+'.'+digits+'/'+(basis==='hour'?'h':'s');}
