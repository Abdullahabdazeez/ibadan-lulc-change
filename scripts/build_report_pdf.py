from pathlib import Path
import markdown
from weasyprint import HTML

src = Path('docs/PROJECT_REPORT.md')
out = Path('reports/Ibadan_LULC_2013_2023_Portfolio_Report.pdf')
out.parent.mkdir(parents=True, exist_ok=True)

body = markdown.markdown(src.read_text(encoding='utf-8'), extensions=['tables'])
css = '''
@page { size: A4; margin: 18mm; }
body { font-family: Arial, sans-serif; color: #222; font-size: 10.5pt; line-height: 1.45; }
h1 { font-size: 23pt; margin-bottom: 14px; }
h2 { font-size: 15pt; margin-top: 22px; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; }
th, td { border: 1px solid #bbb; padding: 7px; text-align: left; }
th { background: #f3f3f3; }
'''
html = f'<html><head><style>{css}</style></head><body>{body}</body></html>'
HTML(string=html, base_url=str(Path.cwd())).write_pdf(out)
print(f'Created {out} ({out.stat().st_size} bytes)')