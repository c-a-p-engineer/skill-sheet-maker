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

# 3. projects.yml 読み込み & 期間計算
with open(PROJECTS_YML, encoding='utf-8') as f:
    proj_data = yaml.safe_load(f)
projects = proj_data.get('projects', [])

# No 自動付番 & 期間計算
for idx, p in enumerate(projects, start=1):
    p['no'] = idx
    
    # 期間計算ロジック
    try:
        start_str, end_str = p['period'].split('〜')
        start_date = datetime.strptime(start_str, '%Y/%m')
        
        if end_str == '現在':
            end_date = datetime.now()
            p['period_str'] = f"{start_date.strftime('%Y年%m月')} 〜 現在"
        else:
            end_date = datetime.strptime(end_str, '%Y/%m')
            p['period_str'] = f"{start_date.strftime('%Y年%m月')} 〜 {end_date.strftime('%Y年%m月')}"

        # 期間を計算（年と月）
        delta_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month) + 1
        years = delta_months // 12
        months = delta_months % 12
        
        duration = []
        if years > 0:
            duration.append(f"{years}年")
        if months > 0:
            duration.append(f"{months}ヶ月")
        
        p['duration'] = "".join(duration) if duration else "1ヶ月未満"

    except (ValueError, AttributeError):
        p['period_str'] = p.get('period', '') # パース失敗時はそのまま表示
        p['duration'] = '' # 期間は空

    # 概要をリストに変換
    if 'overview' in p and isinstance(p['overview'], str):
        lines = p['overview'].strip().split('\n')
        p['overview_list'] = [line.strip().lstrip('- ').strip() for line in lines if line.strip()]
    else:
        p['overview_list'] = []

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
