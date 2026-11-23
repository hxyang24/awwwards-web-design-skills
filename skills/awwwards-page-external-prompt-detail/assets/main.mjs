import {start} from './runtime.mjs';
const response=await fetch('./contract.json');if(!response.ok)throw Error('Missing prompt contract');start(await response.json());
