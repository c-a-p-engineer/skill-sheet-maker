import os
import shutil
import yaml
import markdown
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
from weasyprint import HTML, CSS
from dotenv import load_dotenv

# --- 環境変数読み込み (.env) ---
load_dotenv()
page_size = os.getenv('PAGE_SIZE', 'A4')
page_margin = os.getenv('PAGE_MARGIN', '20mm')

# --- 設定ファイルパス ---
BASE_DIR = os.path.dirname(__file__)
RESUME_MD_EXAMPLE = os.path.join(BASE_DIR, 'resume.md.example')
RESUME_MD = os.path.join(BASE_DIR, 'resume.md')
PROJECTS_YML_EXAMPLE = os.path.join(BASE_DIR, 'projects.yml.example')
PROJECTS_YML = os.path.join(BASE_DIR, 'projects.yml')
TEMPLATE_HTML = os.path.join(BASE_DIR, 'template.html')
OUTPUT_HTML = os.path.join(BASE_DIR, 'resume.html')
OUTPUT_PDF = os.path.join(BASE_DIR, 'resume.pdf')

# --- 初期設定: resume.md / projects.yml がなければ example からコピー ---
if not os.path.exists(RESUME_MD):
    shutil.copy(RESUME_MD_EXAMPLE, RESUME_MD)
    print(f"'{RESUME_MD}' を作成しました。")

if not os.path.exists(PROJECTS_YML):
    shutil.copy(PROJECTS_YML_EXAMPLE, PROJECTS_YML)
    print(f"'{PROJECTS_YML}' を作成しました。")

# 1. resume.md からフロントマターと本文を読み込み
with open(RESUME_MD, encoding='utf-8') as f:
    content = f.read()
header, body = content.split('---', 2)[1:3]
data = yaml.safe_load(header)
data['body'] = markdown.markdown(body)

# 2. 年齢自動計算
birth = datetime.fromisoformat(data['birthday'])
today = datetime.strptime(data['updated_at'], '%Y-%m-%d')
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
tpl = env.get_template(os.path.basename(TEMPLATE_HTML))

# 5. テンプレートにデータを渡してHTMLを生成
render_data = {
    'resume': data,
    'projects': data['projects'],
    'page_size': page_size,
    'page_margin': page_margin
}
html_body = tpl.render(**render_data)

# 6. 中間HTMLファイルとして出力
with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
    f.write(html_body)
print(f"HTML を生成しました: {OUTPUT_HTML}")

# 7. HTML を PDF へ
HTML(string=html_body, base_url=BASE_DIR).write_pdf(OUTPUT_PDF)
print(f"PDF を生成しました: {OUTPUT_PDF}")
