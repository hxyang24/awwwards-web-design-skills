import {start} from './runtime.mjs';
try{const responses=await Promise.all([fetch('./contract.json'),fetch('./story-data.json')]);if(responses.some(r=>!r.ok))throw Error('Reader resources unavailable');start(await responses[0].json(),await responses[1].json());}
catch{document.querySelector('#reader-enhancement-status').textContent='Interactive reader unavailable. All chapters remain readable below.';}
