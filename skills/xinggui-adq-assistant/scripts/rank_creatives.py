"""Rank user-provided public creative evidence; never invent results."""
import argparse,json
from pathlib import Path
from urllib.parse import urlparse

def rank(brief, items):
    results=[]
    for item in items:
        u=urlparse(item.get('url',''))
        if u.scheme!='https' or not u.hostname or u.username or u.password:
            raise ValueError('Every creative must have a public HTTPS source URL without credentials')
        score=0; reasons=[]
        for field,weight in [('industry',3),('product',3),('placement',2),('goal',3),('audience_relation',3)]:
            if brief.get(field) and item.get(field)==brief[field]:
                score+=weight; reasons.append(field)
        results.append({'similarity_score':score,'matched_fields':reasons,'evidence':item,
            'performance_label':'仅有来源材料中的数据，未验证可比性；不能推断客户投放效果',
            'usable_for':'选择结构、卖点及画面参考；素材高曝光不能证明高转化'})
    return sorted(results,key=lambda r:r['similarity_score'],reverse=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--input',type=Path,required=True); p.add_argument('--output',type=Path,required=True); a=p.parse_args()
    d=json.loads(a.input.read_text(encoding='utf-8-sig')); out=rank(d['brief'],d['items']); a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(str(a.output))
