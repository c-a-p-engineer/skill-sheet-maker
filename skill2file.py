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
for path, example in [(RESUME_MD, RESUME_MD_EXAMPLE), (PROJECTS_YML, PROJECTS_YML_EXAMPLE)]:
    if not os.path.exists(path):
        shutil.copy(example, path)
        print(f"'{path}' を作成しました。")

# 1. resume.md から frontmatter と本文を読み込み
with open(RESUME_MD, encoding='utf-8') as f:
    content = f.read()
header, body = content.split('---', 2)[1:3]

data = yaml.safe_load(header) or {}

# HTML 化
data['body'] = markdown.markdown(body)

# 2. 年齢自動計算
birth = datetime.fromisoformat(data.get('birthday', datetime.now().isoformat()))
today = datetime.strptime(data.get('updated_at', datetime.now().strftime('%Y-%m-%d')), '%Y-%m-%d')
data['age'] = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

# 3. projects.yml 読み込み & 期間計算
with open(PROJECTS_YML, encoding='utf-8') as f:
    proj_data = yaml.safe_load(f)
projects = proj_data if isinstance(proj_data, list) else proj_data.get('projects', [])

for idx, p in enumerate(projects, start=1):
    p['no'] = idx
    # 期間計算
    try:
        start_str, end_str = p['period'].split('〜')
        start = datetime.strptime(start_str.strip(), '%Y/%m')
        if end_str.strip() == '現在':
            end = datetime.now()
            p['period_str'] = f"{start.strftime('%Y年%m月')} 〜 現在"
        else:
            end = datetime.strptime(end_str.strip(), '%Y/%m')
            p['period_str'] = f"{start.strftime('%Y年%m月')} 〜 {end.strftime('%Y年%m月')}"
        months = (end.year - start.year)*12 + end.month - start.month + 1
        years, mon = divmod(months, 12)
        p['duration'] = ''.join([f"{years}年"*(years>0), f"{mon}ヶ月"*(mon>0)]) or '1ヶ月未満'
    except Exception:
        p['period_str'] = p.get('period', '')
        p['duration'] = ''
    # 概要リスト
    p['overview_list'] = [l.strip().lstrip('- ').strip() for l in p.get('overview', '').split('\n') if l.strip()]

# 4. テンプレート読み込み & Jinja2 設定
if not os.path.isfile(TEMPLATE_HTML):
    raise FileNotFoundError(f"テンプレートファイルが見つかりません: {TEMPLATE_HTML}")

env = Environment(
    loader=FileSystemLoader(BASE_DIR),
    autoescape=False,
    keep_trailing_newline=True,
)
template_name = os.path.basename(TEMPLATE_HTML)
tpl = env.get_template(template_name)

# 5. レンダリング
render_data = {
    'resume': data,
    'projects': projects,
    'page_size': page_size,
    'page_margin': page_margin,
}
html_body = tpl.render(**render_data)

# 6. HTML 出力
with open(OUTPUT_HTML, 'w', encoding='utf-8') as f:
    f.write(html_body)
print(f"HTML を生成しました: {OUTPUT_HTML}")

# 7. PDF 出力
HTML(string=html_body, base_url=BASE_DIR).write_pdf(OUTPUT_PDF)
print(f"PDF を生成しました: {OUTPUT_PDF}")
