// Original bounded circle model. It does not implement or identify source-site code.
const clamp=(n,a,b)=>Math.max(a,Math.min(b,n));
export class PhysicsRoom{
 constructor({width=720,height=600,count=8}={}){if(!Number.isFinite(width)||!Number.isFinite(height)||width<300||height<250||!Number.isInteger(count)||count<1||count>12)throw Error('Invalid room budget');this.width=width;this.height=height;this.count=count;this.gravity=660;this.bounce=.5;this.steps=0;this.disposed=false;this.reset();}
 reset(){if(this.disposed)return;this.drag=null;this.accumulator=0;this.bodies=Array.from({length:this.count},(_,i)=>({id:i,x:this.width*(.14+(i%4)*.24),y:60+(Math.floor(i/4)+.5)*(this.height-120)/Math.ceil(this.count/4),r:40+(i%3)*4,vx:0,vy:0}));for(const b of this.bodies)this.constrain(b);}
 parameters(strength,bounce){if(Number.isFinite(strength))this.gravity=clamp(strength,0,1200);if(Number.isFinite(bounce))this.bounce=clamp(bounce,0,.9);}
 constrain(b){b.x=clamp(b.x,b.r,this.width-b.r);b.y=clamp(b.y,b.r,this.height-b.r);}
 nudge(id,dx,dy){const b=this.bodies.find(x=>x.id===id);if(!b||!Number.isFinite(dx)||!Number.isFinite(dy))return;b.x+=clamp(dx,-80,80);b.y+=clamp(dy,-80,80);b.vx=0;b.vy=0;this.constrain(b);}
 beginDrag(id,x,y){const b=this.bodies.find(v=>v.id===id);if(!b||!Number.isFinite(x)||!Number.isFinite(y))return false;this.drag={id,dx:b.x-x,dy:b.y-y};b.vx=b.vy=0;return true;}
 moveDrag(x,y){if(!this.drag||!Number.isFinite(x)||!Number.isFinite(y))return;const b=this.bodies.find(v=>v.id===this.drag.id);b.x=x+this.drag.dx;b.y=y+this.drag.dy;b.vx=b.vy=0;this.constrain(b);}
 endDrag(){this.drag=null;}
 hit(x,y){return [...this.bodies].reverse().find(b=>Math.hypot(b.x-x,b.y-y)<=b.r)?.id??null;}
 step(dt){if(this.disposed||!Number.isFinite(dt)||dt<=0)return;this.accumulator+=Math.min(dt,.05);let budget=8;while(this.accumulator>=1/120&&budget-->0){this.integrate(1/120);this.accumulator-=1/120;}}
 integrate(dt){this.steps++;for(const b of this.bodies){if(b.id===this.drag?.id)continue;b.vy+=this.gravity*dt;b.vx*=.997;b.x+=b.vx*dt;b.y+=b.vy*dt;if(b.x<b.r||b.x>this.width-b.r)b.vx=-b.vx*this.bounce;if(b.y<b.r||b.y>this.height-b.r){b.vy=-b.vy*this.bounce;if(Math.abs(b.vy)<12)b.vy=0;}this.constrain(b);}
 for(let pass=0;pass<3;pass++)for(let i=0;i<this.bodies.length;i++)for(let j=i+1;j<this.bodies.length;j++){const a=this.bodies[i],b=this.bodies[j],dx=b.x-a.x,dy=b.y-a.y,d=Math.hypot(dx,dy),overlap=a.r+b.r-d;if(overlap<=0)continue;const nx=d?dx/d:1,ny=d?dy/d:0,wa=a.id===this.drag?.id?0:1,wb=b.id===this.drag?.id?0:1,total=wa+wb;if(!total)continue;const correction=(overlap+.01)/total;a.x-=nx*correction*wa;a.y-=ny*correction*wa;b.x+=nx*correction*wb;b.y+=ny*correction*wb;const speed=(b.vx-a.vx)*nx+(b.vy-a.vy)*ny;if(speed<0){const impulse=-(1+this.bounce)*speed/total;a.vx-=impulse*nx*wa;a.vy-=impulse*ny*wa;b.vx+=impulse*nx*wb;b.vy+=impulse*ny*wb;}}
 for(const b of this.bodies){this.constrain(b);b.vx=clamp(b.vx,-700,700);b.vy=clamp(b.vy,-700,700);}}
 dispose(){if(this.disposed)return;this.disposed=true;this.drag=null;this.bodies=[];this.accumulator=0;}
}
