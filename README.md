# IT経歴書生成ツール

このツールは、Markdown と YAML で記述した経歴情報から、PDF（A4 など任意サイズ）形式の職務経歴書を自動生成します。

## 構成ファイル

* `resume.md`
  フロントマター（YAML）に氏名・誕生日・メールアドレス・最寄り駅・作成日などのパーソナル情報を記載。
* `projects.yml`
  プロジェクト一覧を YAML フォーマットで管理。
* `template.md`
  Jinja2 テンプレート（Markdown形式）で出力レイアウトを定義。
* `generate_resume_pdf.py`
  上記ファイルを読み込み、WeasyPrint で PDF を生成するスクリプト。
* `.env`
  環境変数として用紙サイズやマージンを指定可能。

## 必要環境

* Python 3.7+
* 以下ライブラリ

  ```bash
  pip install PyYAML Jinja2 markdown weasyprint python-dotenv
  ```

## セットアップ

1. リポジトリをクローン／Download。
2. ルートに以下ファイルを配置：

   * `resume.md`
   * `projects.yml`
   * `template.md`
3. `.env` ファイル を作成（任意）：

   ```dotenv
   # 用紙サイズ：A4, Letter など
   PAGE_SIZE=A4
   # 余白：例) 20mm, 1in など
   PAGE_MARGIN=20mm
   ```

## 使い方

```bash
# 経歴書を生成
python skill2file.py
```

成功すると、同ディレクトリに `resume.pdf` が出力されます。

## カスタマイズ

* テンプレートの編集は `template.md` を書き換え。
* プロジェクト情報追加は `projects.yml` にエントリを追記。
* 用紙サイズや余白は `.env` で調整。

## ライセンス

MIT
