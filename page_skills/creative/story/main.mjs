import {start} from './runtime.mjs';
const response=await fetch('./contract.json');if(!response.ok)throw Error('Missing story contract');start(await response.json());
