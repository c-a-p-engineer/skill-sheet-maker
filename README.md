# IT経歴書生成ツール

このツールは、Markdown と YAML で記述した経歴情報から、HTMLおよびPDF形式の職務経歴書を自動生成します。

## 特徴

- 経歴情報は `resume.md` と `projects.yml` で管理
- 出力レイアウトは `template.html` (Jinja2) で自由にカスタマイズ可能
- PDF生成にはWeasyPrintを使用
- 中間ファイルとしてHTMLが出力されるため、デバッグが容易
- Dev Containerに対応し、環境構築が簡単

## 構成ファイル

- **`skill2file.py`**: メインの実行スクリプト
- **`resume.md.example`**: 経歴情報のサンプル（これをコピーして `resume.md` を作成）
- **`projects.yml.example`**: プロジェクト一覧のサンプル（これをコピーして `projects.yml` を作成）
- **`template.html`**: 出力レイアウトを定義するJinja2テンプレート
- **`requirements.txt`**: Pythonの依存ライブラリリスト
- **`.env.example`**: 環境変数設定のサンプル（用紙サイズ・マージン）
- **`.devcontainer/`**: 開発環境を定義するDev Container設定

## 必要環境

- Python 3.7+
- 日本語フォント（PDFで日本語を表示するために必要です）

## セットアップ

### A) Dev Container を使用する場合 (推奨)

1.  リポジトリをクローンします。
2.  Visual Studio Code で開き、「Reopen in Container」を選択します。
    -   必要なライブラリと日本語フォントが自動でインストールされます。

### B) 手動でセットアップする場合

1.  リポジトリをクローンします。
2.  お使いのシステムに日本語フォントをインストールします。(例: `sudo apt-get install -y fonts-noto-cjk`)
3.  Pythonの仮想環境を作成し、ライブラリをインストールします。
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
4.  設定ファイルのサンプルをコピーして、自分用に編集します。
    ```bash
    cp resume.md.example resume.md
    cp projects.yml.example projects.yml
    cp .env.example .env
    ```

## 使い方

以下のコマンドを実行します。

```bash
python skill2file.py
```

成功すると、同ディレクトリに `resume.html` と `resume.pdf` が出力されます。

## カスタマイズ

- **テンプレートの編集**: `template.html` を書き換えます。
- **経歴情報の編集**: `resume.md` を編集します。
- **プロジェクト情報の追加**: `projects.yml` にエントリを追記します。
- **用紙サイズや余白の調整**: `.env` ファイルを編集します。

## ライセンス

MIT
