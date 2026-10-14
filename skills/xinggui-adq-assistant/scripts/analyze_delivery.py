"""No API: calculate observed metrics and a bounded first-bid hypothesis."""
import argparse, csv, json, math
from pathlib import Path

def number(value, name):
    if value is None or value == '':
        return None
    if isinstance(value, bool):
        raise ValueError(f'{name}: expected a number')
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise ValueError(f'{name}: expected a finite nonnegative number')
    return result

def ratio(a, b, multiplier=1):
    return None if a is None or b is None or b == 0 else a / b * multiplier

def analyze(config):
    if config.get('goal') not in ['exposure', 'conversion']:
        raise ValueError('goal must be exposure or conversion')
    bid = config.get('bid', {})
    unit = bid.get('unit')
    reference = bid.get('reference', {})
    ceiling = number(bid.get('business_ceiling'), 'business_ceiling')
    budget = number(config.get('approved_test_budget'), 'approved_test_budget')
    blockers = []
    if budget is None or budget <= 0:
        blockers.append('客户尚未确定正数试投消耗上限')
    if config.get('audience_confirmed') is not True:
        blockers.append('尚未确认名单挂载及人群范围')
    if config['goal'] == 'conversion' and config.get('event_verified') is not True:
        blockers.append('目标转化事件的实际统计或回传尚未验证')
    low = number(reference.get('low'), 'reference.low')
    high = number(reference.get('high'), 'reference.high')
    known = reference.get('source') and reference.get('same_context') is True and reference.get('unit') == unit and unit in ['元/千次曝光','元/点击','元/目标事件']
    proposal = None
    if low is not None and high is not None and low > high:
        raise ValueError('reference.low must not exceed reference.high')
    if known and low is not None and high is not None and low > 0:
        proposal = (low + high) / 2
        if ceiling is not None:
            proposal = min(proposal, ceiling)
        if proposal <= 0:
            proposal = None
            blockers.append('经营成本边界为零，当前不适合开展付费验证')
    else:
        blockers.append('缺少同单位、同目标和版位适用的后台推荐范围或历史参考')
    return {
        'goal':config['goal'], 'bid_hypothesis': proposal, 'bid_unit':unit,
        'basis':'适用参考范围的中点；如有同口径经营上限则取较低值。这是可修改的首轮试验启发式，不是腾讯规则或最优出价。' if proposal is not None else None,
        'reference_source':reference.get('source'), 'approved_test_budget':budget,
        'ready_for_manual_review':not blockers, 'blockers':blockers,
        'warnings':['竞价目标价不保证实际成本。','消耗上限需要人工观察执行，脚本不会停止广告。','经营上限低于参考下限时，可能难以起量。'] if ceiling is not None and low is not None and ceiling < low else ['竞价目标价不保证实际成本。','消耗上限需要人工观察执行，脚本不会停止广告。']
    }

def metrics(row):
    names=['消耗元','曝光次数','名单内去重触达人数','点击次数','有效线索数','归因成交客户数','可投名单人数']
    n={k:number(row.get(k),k) for k in names}
    return {'原始记录':row,'指标':{
        'CPM元':ratio(n['消耗元'],n['曝光次数'],1000),
        'CTR':ratio(n['点击次数'],n['曝光次数']),
        '平均点击成本元':ratio(n['消耗元'],n['点击次数']),
        '有效线索成本元':ratio(n['消耗元'],n['有效线索数']),
        '归因成交客户成本元':ratio(n['消耗元'],n['归因成交客户数']),
        '名单覆盖率':ratio(n['名单内去重触达人数'],n['可投名单人数']),
        '平均频次':ratio(n['曝光次数'],n['名单内去重触达人数']) if row.get('曝光与触达同范围') == '是' else None},
        '口径提示':'不跨行相加去重触达；曝光与名单内触达必须是同范围，否则平均频次不可用。null 表示资料不足或分母为零。'}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--config',type=Path)
    p.add_argument('--csv',type=Path)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    if not args.config and not args.csv:
        p.error('provide --config or --csv')
    result={}
    if args.config:
        result['首轮建议']=analyze(json.loads(args.config.read_text(encoding='utf-8-sig')))
    if args.csv:
        with args.csv.open(encoding='utf-8-sig',newline='') as f:
            result['逐行复盘']=[metrics(row) for row in csv.DictReader(f)]
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(str(args.output))

if __name__=='__main__':
    main()
