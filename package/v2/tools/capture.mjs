import {chromium} from '@playwright/test';
import fs from 'node:fs';
import path from 'node:path';
const [url,output,width='1440',height='1000',...flags]=process.argv.slice(2);let browser;
try{
 if(!output)throw Error('Usage: capture.mjs URL output.png [width height] [--allow-remote]');const target=new URL(url);
 if(!['http:','https:'].includes(target.protocol)||target.username||target.password)throw Error('Only credential-free HTTP(S) URLs are supported');
 if(!['127.0.0.1','localhost','[::1]'].includes(target.hostname)&&!flags.includes('--allow-remote'))throw Error('Remote capture requires explicit --allow-remote after authorization');
 if(![width,height].every(v=>/^\d+$/.test(v)&&Number(v)>=200&&Number(v)<=4096))throw Error('Viewport dimensions must be 200–4096');
 browser=await chromium.launch({headless:true,executablePath:process.env.PLAYWRIGHT_EXECUTABLE||chromium.executablePath()});
 const page=await browser.newPage({viewport:{width:Number(width),height:Number(height)},deviceScaleFactor:1,reducedMotion:'reduce',locale:'en-US',timezoneId:'UTC'});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(url,{waitUntil:'networkidle',timeout:30000});await page.locator('h1').first().waitFor();await page.evaluate(()=>document.fonts.ready);fs.mkdirSync(path.dirname(output),{recursive:true});await page.screenshot({path:output,fullPage:false,animations:'disabled'});fs.writeFileSync(output+'.json',JSON.stringify({url,viewport:{width:Number(width),height:Number(height)},device_scale_factor:1,reduced_motion:'reduce',browser:browser.version(),captured_at:new Date().toISOString(),errors,full_page:false,scope:'Visible state only; no business or rights acceptance'},null,2));if(errors.length)throw Error('Page errors: '+errors.join('; '));console.log(output);
}catch(err){console.error(err.message);process.exitCode=2;}finally{await browser?.close();}
