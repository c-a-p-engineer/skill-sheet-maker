import os
import yaml
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from weasyprint import HTML, CSS
from dotenv import load_dotenv

# --- 環境変数読み込み (.env) ---
load_dotenv()
page_size = os.getenv('PAGE_SIZE', 'A4')  # 用紙サイズ（例: A4, Letterなど）
page_margin = os.getenv('PAGE_MARGIN', '20mm')  # マージン（例: 20mm）

# --- 設定ファイルパス ---
BASE_DIR = os.path.dirname(__file__)
RESUME_MD = os.path.join(BASE_DIR, 'resume.md')
PROJECTS_YML = os.path.join(BASE_DIR, 'projects.yml')
TEMPLATE_MD = os.path.join(BASE_DIR, 'template.md')
OUTPUT_PDF = os.path.join(BASE_DIR, 'resume.pdf')

# 1. resume.md からフロントマター読み込み
with open(RESUME_MD, encoding='utf-8') as f:
    content = f.read()
header, _ = content.split('---', 2)[1:3]
data = yaml.safe_load(header)

# 2. 年齢自動計算
birth = datetime.fromisoformat(data['birthday'])
today = datetime.strptime(data['date'], '%Y-%m-%d')
data['age'] = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

# 3. projects.yml 読み込み
with open(PROJECTS_YML, encoding='utf-8') as f:
    proj_data = yaml.safe_load(f)
projects = proj_data.get('projects', [])

# No 自動付番
for idx, p in enumerate(projects, start=1):
    p['no'] = idx

data['projects'] = projects

# 4. テンプレート読み込み & Jinja2 環境設定
env = Environment(
    loader=FileSystemLoader(BASE_DIR),
    autoescape=False,
    keep_trailing_newline=True,
)
tpl = env.get_template(os.path.basename(TEMPLATE_MD))

# 5. Markdown → HTML
md_text = tpl.render(**data)
html_body = markdown.markdown(md_text, extensions=['fenced_code', 'tables'])

# 6. HTML を PDF へ (env指定用紙サイズ)
css_str = f"""
@page {{ size: {page_size}; margin: {page_margin}; }}
body {{ font-family: sans-serif; }}
"""
global_css = CSS(string=css_str)
HTML(string=html_body, base_url=BASE_DIR).write_pdf(OUTPUT_PDF, stylesheets=[global_css])

print(f"PDF を生成しました: {OUTPUT_PDF} (size={page_size}, margin={page_margin})")
