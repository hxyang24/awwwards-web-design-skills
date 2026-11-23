import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {PNG} from 'pngjs';
import pixelmatch from 'pixelmatch';
export function readPNG(file){if(fs.statSync(file).size>32*1024*1024)throw Error('PNG exceeds 32 MiB');const b=fs.readFileSync(file);if(b.length<24||b.readUInt32BE(0)!==0x89504e47||b.readUInt32BE(4)!==0x0d0a1a0a)throw Error('Not a PNG');const w=b.readUInt32BE(16),h=b.readUInt32BE(20);if(!w||!h||w*h>16000000)throw Error('PNG exceeds 16 million pixels');return PNG.sync.read(b);}
const boundedRatio=(x,label)=>{if(!Number.isFinite(x)||x<0||x>1)throw Error('Invalid '+label);};
export function compare(a,b,config={}){
 if(a.width!==b.width||a.height!==b.height)throw Error('Image dimensions differ; resizing is not permitted');
 const {width:w,height:h}=a,max=config.max_ratio??0.005,threshold=config.pixel_threshold??0.1;boundedRatio(max,'max_ratio');boundedRatio(threshold,'pixel_threshold');
 const regions=config.regions||[],masks=config.masks||[];
 const rect=(r)=>{if(!['x','y','width','height'].every(k=>Number.isInteger(r[k]))||r.x<0||r.y<0||r.width<=0||r.height<=0||r.x+r.width>w||r.y+r.height>h)throw Error('Invalid or out-of-bounds rectangle');};
 for(const r of regions){rect(r);if(!r.id)throw Error('Region id is required');boundedRatio(r.max_ratio??max,'region max_ratio');}
 for(const m of masks){rect(m);if(!m.reason?.trim())throw Error('Mask reason is required');for(const r of regions)if(r.critical!==false&&m.x<r.x+r.width&&m.x+m.width>r.x&&m.y<r.y+r.height&&m.y+m.height>r.y)throw Error('Mask overlaps a critical region');}
 const aa=Buffer.from(a.data),bb=Buffer.from(b.data),excluded=new Uint8Array(w*h),diff=new PNG({width:w,height:h});
 for(const m of masks)for(let y=m.y;y<m.y+m.height;y++)for(let x=m.x;x<m.x+m.width;x++){const i=y*w+x;excluded[i]=1;aa.fill(0,i*4,i*4+4);bb.fill(0,i*4,i*4+4);}
 const eligible=excluded.reduce((n,v)=>n+(v?0:1),0);if(!eligible)throw Error('All pixels are masked');
 const changed=pixelmatch(aa,bb,diff.data,w,h,{threshold,includeAA:true,diffMask:true});let mae=0;for(let i=0;i<w*h;i++)if(!excluded[i])for(let c=0;c<3;c++)mae+=Math.abs(a.data[i*4+c]-b.data[i*4+c]);
 const regionResults=regions.map(r=>{const xA=new PNG({width:r.width,height:r.height}),xB=new PNG({width:r.width,height:r.height});let n=0;for(let y=0;y<r.height;y++)for(let x=0;x<r.width;x++){const source=(r.y+y)*w+r.x+x,dest=y*r.width+x;aa.copy(xA.data,dest*4,source*4,source*4+4);bb.copy(xB.data,dest*4,source*4,source*4+4);if(!excluded[source])n++;}if(!n)throw Error('Region is fully masked');const count=pixelmatch(xA.data,xB.data,null,r.width,r.height,{threshold,includeAA:true});return {id:r.id,changed:count,eligible:n,ratio:count/n,max_ratio:r.max_ratio??max,passed:count/n<=(r.max_ratio??max)};});
 return {report:{status:changed/eligible<=max&&regionResults.every(r=>r.passed)?'passed':'failed',width:w,height:h,changed,eligible,ratio:changed/eligible,mean_absolute_rgb_error:mae/(eligible*3),max_ratio:max,pixel_threshold:threshold,masks,regions:regionResults},diff};
}
if(process.argv[1]===fileURLToPath(import.meta.url)){
 const [reference,candidate,prefix,configFile]=process.argv.slice(2);try{if(!prefix)throw Error('Usage: node visual_diff.mjs reference.png candidate.png output-prefix [config.json]');const result=compare(readPNG(reference),readPNG(candidate),configFile?JSON.parse(fs.readFileSync(configFile,'utf8')):{});fs.mkdirSync(path.dirname(prefix),{recursive:true});fs.writeFileSync(prefix+'.diff.png',PNG.sync.write(result.diff));fs.writeFileSync(prefix+'.json',JSON.stringify({...result.report,reference,candidate,reference_sha256:createHash('sha256').update(fs.readFileSync(reference)).digest('hex'),candidate_sha256:createHash('sha256').update(fs.readFileSync(candidate)).digest('hex'),environment:'PNG pixel comparison; not a semantic or business acceptance result'},null,2));console.log(JSON.stringify(result.report));process.exitCode=result.report.status==='passed'?0:1;}catch(err){console.error(err.message);process.exitCode=2;}
}
