import {fileURLToPath} from 'node:url';
import fs from 'node:fs/promises';
import path from 'node:path';

const query = process.argv.slice(2).filter(x => !x.startsWith('--')).join(' ').trim();
const limit = Number(process.argv.find(x => x.startsWith('--limit='))?.split('=')[1] || 12);
if (!query) { console.error('Usage: node tools/query-help.mjs <keywords> [--limit=12]'); process.exit(1); }
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../knowledge-base');
const current = JSON.parse(await fs.readFile(path.join(root, 'current.json'), 'utf8'));
const snapshot = path.join(root, current.path);
const articles = JSON.parse(await fs.readFile(path.join(snapshot, 'article-index.json'), 'utf8'));
const byId = new Map(articles.map(x => [x.postId, x]));
let clauseFile = 'readable-clauses.jsonl';
try { await fs.access(path.join(snapshot, clauseFile)); } catch { clauseFile = 'clauses.jsonl'; }
const clauses = (await fs.readFile(path.join(snapshot, clauseFile), 'utf8')).split('\n').filter(Boolean).map(x => JSON.parse(x));
try { clauses.push(...(await fs.readFile(path.join(snapshot, 'attachment-clauses.jsonl'), 'utf8')).split('\n').filter(Boolean).map(x => JSON.parse(x))); } catch {}
const terms = query.toLowerCase().split(/\s+/).filter(Boolean);
const ranked = clauses.map(c => {
  const article = byId.get(c.postId);
  if (!article) return { c, article, score: 0 };
  const title = c.title.toLowerCase();
  const section = c.section.toLowerCase();
  const body = c.text.toLowerCase();
  const route = article.routes.flat().join(' ').toLowerCase();
  const score = terms.reduce((sum, term) => sum + (title.includes(term) ? 5 : 0) + (section.includes(term) ? 3 : 0) + (body.includes(term) ? 6 : 0) + (route.includes(term) ? 1 : 0), 0);
  return { c, article, score, bodyHit: terms.some(t => body.includes(t)) };
}).filter(x => x.score > 0).sort((a, b) => b.score - a.score || Number(b.bodyHit) - Number(a.bodyHit));
console.log(`Snapshot: ${current.snapshot}; results are evidence candidates, not eligibility conclusions.\n`);
const selected = [];
const perArticle = new Map();
for (const result of ranked) {
  const key = result.c.sourceType === 'attachment' ? result.c.url : result.c.postId;
  if ((perArticle.get(key) || 0) >= 3) continue;
  perArticle.set(key, (perArticle.get(key) || 0) + 1);
  selected.push(result);
  if (selected.length >= limit) break;
}
for (const { c, article } of selected) {
  const originalFile = c.sourceType === 'attachment' ? c.attachment : article.raw;
  const documentFile = c.sourceType === 'attachment' ? c.extractedText : c.locator.includes(':R') ? article.readable : article.document;
  console.log(JSON.stringify({ title: c.title, section: c.section, officialClause: c.officialLabel || 'No extracted official number; cite heading and original quote', locator: c.locator, quote: c.text, url: c.url || article.url, officialUpdatedAt: article.updatedAt, fetchedAt: article.fetchedAt, document: path.join(snapshot, documentFile), raw: path.join(snapshot, originalFile), page: c.page, sheet: c.sheet, cell: c.cell, slide: c.slide }, null, 2));
}
