import sys
import io
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from ddgs import DDGS

r = DDGS().text('Kubernetes是什么', max_results=3)
for i, item in enumerate(r):
    print(f'{i+1}. 标题: {item["title"]}')
    print(f'   摘要: {item["body"][:100]}...')
    print(f'   URL: {item["href"]}')
    print()
