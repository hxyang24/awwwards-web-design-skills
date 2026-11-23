#!/usr/bin/env python3
"""Copy a complete, original, dependency-free website into a new empty directory."""
import argparse,shutil,json
from pathlib import Path
ALLOWED=['saas','commerce','dashboard','portfolio','editorial','immersive']
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--kind',choices=ALLOWED,required=True);p.add_argument('--name',required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();dst=a.output
 if not a.name.strip() or any(x in a.name for x in ['<','>','{','}','&']):p.error('品牌名为空或包含HTML敏感字符')
 if dst.exists() and any(dst.iterdir()):p.error('拒绝覆盖非空目录')
 src=Path(__file__).resolve().parents[1]/'templates'/a.kind
 dst.mkdir(parents=True,exist_ok=True)
 shutil.copy2(src/'main.js',dst/'main.js');html=(src/'index.html').read_text(encoding='utf-8').replace('{{BRAND}}',a.name.strip())
 (dst/'index.html').write_text(html,encoding='utf-8')
 assets=dst/'assets';assets.mkdir(exist_ok=True)
 shared=src.parent/'shared'
 for fn in ('styles.css','common.js'):shutil.copy2(shared/fn,assets/fn)
 (dst/'README.md').write_text(f'# {a.name}\n\n类型：{a.kind}\n\n原创静态页面蓝本，零外部依赖。运行：`python -m http.server 8000 --directory .`，随后访问 http://localhost:8000。由于 ES 模块需 HTTP，请勿直接用 file:// 打开。\n\n演示交互不会向后端发送数据，产品、数字与价格为占位的虚构内容。上线前替换实际业务内容并执行浏览器/无障碍/性能验收。\n',encoding='utf-8')
 print(json.dumps({'created':str(dst),'kind':a.kind,'files':sorted(str(f.relative_to(dst)) for f in dst.rglob('*') if f.is_file())},ensure_ascii=False))
