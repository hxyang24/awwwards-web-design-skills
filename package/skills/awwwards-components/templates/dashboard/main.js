import {setupNavigation} from './assets/common.js';setupNavigation();
const input=document.getElementById('search-records');const rows=[...document.querySelectorAll('#record-body tr')];const status=document.getElementById('record-status');
input.addEventListener('input',()=>{
 const query=input.value.trim().toLocaleLowerCase();let count=0;
 for(const row of rows){ const keep=row.textContent.toLocaleLowerCase().includes(query);row.hidden=!keep;if(keep)count++; }
 status.textContent=count?`当前显示 ${count} 条演示记录。`:'没有符合条件的演示记录。请修改关键词。';
});
