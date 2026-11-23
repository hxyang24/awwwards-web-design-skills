import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {readPNG} from './visual_diff.mjs';
export function inspect(png){const colors=new Map();let samples=0;const stride=Math.max(1,Math.floor(Math.sqrt(png.width*png.height/200000)));
 for(let y=0;y<png.height;y+=stride)for(let x=0;x<png.width;x+=stride){const i=(y*png.width+x)*4;if(png.data[i+3]<128)continue;const rgb=[0,1,2].map(c=>Math.min(255,Math.round(png.data[i+c]/16)*16)),key=rgb.join(',');colors.set(key,(colors.get(key)||0)+1);samples++;}
 return {width:png.width,height:png.height,samples,quantization_step:16,palette:[...colors].sort((a,b)=>b[1]-a[1]).slice(0,12).map(([rgb,n])=>({rgb:rgb.split(',').map(Number),fraction:n/samples})),limitations:['No OCR, font identity, semantic layout or hidden interaction inference']};}
if(process.argv[1]===fileURLToPath(import.meta.url)){try{const result=inspect(readPNG(process.argv[2]));if(!process.argv[3])throw Error('Usage: inspect_image.mjs input.png output.json');fs.writeFileSync(process.argv[3],JSON.stringify(result,null,2));console.log(JSON.stringify(result));}catch(err){console.error(err.message);process.exitCode=2;}}
