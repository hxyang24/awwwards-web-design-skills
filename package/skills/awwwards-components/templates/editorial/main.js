import {setupNavigation} from './assets/common.js';setupNavigation();
const bar=document.getElementById('reading-progress');
if(bar){let ticking=false;const update=()=>{const max=Math.max(1,document.documentElement.scrollHeight-window.innerHeight);bar.style.width=`${Math.min(100,Math.max(0,window.scrollY/max*100))}%`;ticking=false;};window.addEventListener('scroll',()=>{if(!ticking){ticking=true;requestAnimationFrame(update);}}, {passive:true});update();}
