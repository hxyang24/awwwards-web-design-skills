// Adapt a distinct standalone pattern to the page-skill contract without
// replacing the pattern's interface with a generic wireframe.
import './runtime.mjs';
const contract=await fetch('./contract.json').then(response=>{if(!response.ok)throw Error('Page contract unavailable');return response.json();});
document.body.dataset.kind=contract.kind;
window.__pageSkill={id:contract.id,kind:contract.kind,mode:'local_original_pattern_variant'};
