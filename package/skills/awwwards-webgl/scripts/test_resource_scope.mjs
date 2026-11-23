import assert from 'node:assert/strict';
import { ResourceScope } from '../assets/resource-scope.mjs';
let n=0;const s=new ResourceScope();s.add({dispose(){n++;}});s.add({dispose(){n++;}});
s.dispose();s.dispose();assert.equal(n,2);assert.equal(s.isDisposed,true);
assert.throws(()=>s.add({dispose(){}}));
const r = new ResourceScope();assert.throws(()=>r.add(null));
console.log('PASS resource scope ownership, once disposal, late add rejection');
