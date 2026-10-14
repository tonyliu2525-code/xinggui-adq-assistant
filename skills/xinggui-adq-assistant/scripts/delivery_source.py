"""Data-source seam. CSV works today; Tencent API is deliberately unconnected."""
import argparse
import csv
import json
from pathlib import Path


class CsvSource:
    def __init__(self, path):
        self.path = Path(path)

    def read_configuration(self, account_id):
        raise NotImplementedError('CSV does not contain complete account configuration; provide screenshots.')

    def read_report(self, account_id=None, start=None, end=None):
        if account_id is not None or start is not None or end is not None:
            raise ValueError('CSV is an already scoped export; filter and verify scope before importing.')
        with self.path.open(encoding='utf-8-sig', newline='') as handle:
            reader = csv.DictReader(handle)
            required = {'消耗元', '曝光次数', '点击次数'}
            if not required.issubset(reader.fieldnames or []):
                raise ValueError('Missing report columns: ' + ', '.join(sorted(required - set(reader.fieldnames or []))))
            return list(reader)


class TencentApiSource:
    """Implement against authorized, verified official endpoints in a future update."""
    def __init__(self, config):
        self.config = config

    def read_configuration(self, account_id):
        raise NotImplementedError('Tencent API configuration adapter is reserved, not connected.')

    def read_report(self, account_id, start, end):
        raise NotImplementedError('Tencent API report adapter is reserved, not connected.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', choices=['csv', 'tencent'], required=True)
    parser.add_argument('--input', type=Path)
    parser.add_argument('--config', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.source == 'csv':
        if args.input is None:
            parser.error('--input is required for CSV')
        result = {'source': 'csv', 'records': CsvSource(args.input).read_report(),
                  'scope': 'Scope and metric definitions require review against the original export.'}
    else:
        if args.config is None:
            parser.error('--config is required for Tencent')
        config = json.loads(args.config.read_text(encoding='utf-8-sig'))
        parser.exit(2, 'Tencent API adapter is reserved, not connected; no network request was sent.\n')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
