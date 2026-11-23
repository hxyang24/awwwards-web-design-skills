const id=x=>typeof x==='string'&&/^[a-z][a-z0-9-]{0,39}$/.test(x),text=(x,n=160)=>typeof x==='string'&&x.trim().length>0&&x.length<=n;
export function hex(value){if(typeof value!=='string'||!/^#[0-9a-f]{6}$/i.test(value.trim()))throw Error('Use an opaque six-digit color such as #3D2630. Names, shorthand and alpha are not evaluated.');return value.trim().toUpperCase();}
export function parseGuide(d){
 if(!d||d.schema_version!==1||!id(d.id)||!text(d.title)||!text(d.summary,700)||!/^[A-Za-z0-9._-]{1,30}$/.test(d.version)||d.origin!=='original_fictional_study')throw Error('Invalid original guide');
 for(const k of['palette','symbols','motion'])if(!Array.isArray(d[k])||d[k].length<2||d[k].length>32)throw Error('Bounded guide records required');
 const palette=d.palette.map(x=>{if(!id(x.id)||!text(x.name,80))throw Error('Invalid color token');return{id:x.id,name:x.name,hex:hex(x.hex)};});
 const symbols=d.symbols.map(x=>{if(!id(x.id)||!text(x.name,80)||!['orbit','window','steps','cross'].includes(x.shape))throw Error('Use original supported symbols');return{id:x.id,name:x.name,shape:x.shape};});
 const motion=d.motion.map(x=>{if(!id(x.id)||!text(x.name,80)||!Number.isInteger(x.duration_ms)||x.duration_ms<100||x.duration_ms>1800||!['linear','cubic-bezier(0.2, 0.8, 0.2, 1)'].includes(x.easing))throw Error('Review motion inputs');return{id:x.id,name:x.name,duration_ms:x.duration_ms,easing:x.easing};});
 for(const a of[palette,symbols,motion])if(new Set(a.map(x=>x.id)).size!==a.length)throw Error('Duplicate guide identity');
 return{id:d.id,title:d.title,summary:d.summary,version:d.version,origin:d.origin,palette,symbols,motion};
}
export function luminance(value){const c=hex(value).slice(1).match(/../g).map(x=>parseInt(x,16)/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4);return .2126*c[0]+.7152*c[1]+.0722*c[2];}
export function contrast(foreground,background){const fg=hex(foreground),bg=hex(background),a=luminance(fg),b=luminance(bg),ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);return{foreground:fg,background:bg,ratio,normal_text_ratio_met:ratio>=4.5,large_text_ratio_met:ratio>=3,scope:'Opaque sRGB ratio only; not a complete WCAG conformance determination'};}
export function displayRatio(ratio){if(!Number.isFinite(ratio)||ratio<1||ratio>21.000001)throw Error('Invalid contrast result');return(Math.floor(ratio*100)/100).toFixed(2)+':1';}
export function paletteCSS(guide){return'/* Original fictional '+guide.id+' palette / MIT / version '+guide.version+' */\n:root {\n'+guide.palette.map(x=>'  --color-'+x.id+': '+x.hex+';').join('\n')+'\n}\n';}
export function paletteJSON(guide){return JSON.stringify({schema_version:1,id:guide.id,version:guide.version,license:'MIT',origin:guide.origin,colors:Object.fromEntries(guide.palette.map(x=>[x.id,x.hex]))},null,2)+'\n';}
export function arrangement(guide,count,step){if(!Number.isInteger(count)||count<2||count>Math.min(4,guide.symbols.length)||!Number.isSafeInteger(step)||step<0)throw Error('Invalid bounded symbol arrangement');const list=guide.symbols.slice(0,count);return list.map((_,i)=>list[(i+step%count)%count]);}
export function contrastReport(guide,pair){const result=contrast(pair.foreground,pair.background);return JSON.stringify({schema_version:1,guide_id:guide.id,guide_version:guide.version,...result,reference:'https://www.w3.org/TR/WCAG22/#dfn-relative-luminance'},null,2)+'\n';}
