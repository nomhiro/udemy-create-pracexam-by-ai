# Azure 資格試験問題の作成プロジェクト

本リポジトリには Azure の資格試験を Azure OpenAI Service を使って翻訳するPythonファイルが含まれています。

本ノートブックを使うことで以下のことができます。

- 過去問の情報をもとに、詳細な解説を追加する。※Udemyの試験問題のCSV形式に変換する
- 元の試験問題（csv ファイル）と詳細解説追加後の試験問題（csv ファイル）を渡して、結果の評価をする。

## 使い方

### プロジェクトの clone

はじめに本リポジトリを clone します。

```sh
git clone https://github.com/azpoc-lab/mcp-translate-notebook.git
```

次に VSCode を使ってプロジェクトを開きます。

```sh
code ./mcp-translate-notebook
```

### 実行環境のセットアップ

ノートブックの実行には`python`と`poetry`が必要です。  
[`asdf`](https://asdf-vm.com/)を利用している場合は[`.tool-versions`](./.tool-versions)のファイルの情報から`python`と`poetry`のバージョンを参照できます。

`poetry`を使って依存関係を解決してください。

```sh
# 依存関係の解決
poetry install
```

### Azure OpenAI Service のセットアップと環境変数の設定

Azure 上で Azure OpenAI Service リソースを作成して、以下の要件をクリアしたモデルをデプロイしてください。

- 構造化出力（Structured Outputs）に対応していること
  - 参考： https://learn.microsoft.com/ja-jp/azure/ai-services/openai/how-to/structured-outputs?tabs=python-secure

プロジェクトルートに`.env`ファイルを用意し、Azure OpenAI Service との接続情報を記載しておきます。

```sh
AZURE_OPENAI_ENDPOINT=<接続先のAzureOpenAIServiceリソースのエンドポイント>
AZURE_OPENAI_API_KEY=<接続先のAzureOpenAIServiceリソースのAPIキー>
AZURE_OPENAI_DEPLOYMENT=<翻訳・評価に利用するデプロイ名>
```

なお以下のリソース構成での動作を確認しています。

| 項目             | 値               |
| :--------------- | :--------------- |
| リージョン       | 東日本           |
| モデル           | `gpt-4o-mini`    |
| モデルバージョン | `2024-07-18`     |
| デプロイの種別   | `グローバル標準` |
| TPM              | `100K`           |

### csv ファイルの整形と配置

AI推論前の過去問CSVファイルの形式
Question Type：単一選択問題の場合は「multiple-choice」、複数選択問題の場合は「multi-select」を指定してください。
| Question | Question Type | Answer Option 1 | Answer Option 2 | Answer Option 3 | Answer Option 4 | Correct Answers | Overall Explanation |
| -------- | ------------- | --------------- | --------------- | --------------- | --------------- | --------------- | ------------------- |
| <英語の試験問題文> | <問題の出題形式> | <回答の選択肢 1> | <回答の選択肢 2> | <回答の選択肢 3> | <回答の選択肢 4> | <正解の選択肢の番号> | <解説> |

AI推論後の csv ファイルは以下の構造になるように整形しておいてください。  
**なお 1 行目はヘッダーになります。ヘッダーの各列の名前の表記ゆれは問題ありません。各列の意味的な配置が指定された構造に従っている必要があります。**

| Question           | Question Type    | Answer Option 1  | Explanation 1            | Answer Option 2  | Explanation 2           | Answer Option 3  | Explanation 3            | Answer Option 4   | Explanation 4            | Answer Option 5  | Explanation 5           | Answer Option 6  | Explanation 6           | Correct Answers      | Overall Explanation | Domain           |
| ------------------ | ---------------- | ---------------- | ------------------------ | ---------------- | ----------------------- | ---------------- | ------------------------ | ----------------- | ------------------------ | ---------------- | ----------------------- | ---------------- | ----------------------- | -------------------- | ------------------- | ---------------- |
| <英語の試験問題文> | <問題の出題形式> | <回答の選択肢 1> | <回答の選択肢 1 の説明>  | <回答の選択肢 2> | <回答の選択肢 2 の説明> | <回答の選択肢 3> | <回答の選択肢 3 の説明>  | <回答の選択肢 4>  | <回答の選択肢 4 の説明>  | <回答の選択肢 5> | <回答の選択肢 5 の説明> | <回答の選択肢 6> | <回答の選択肢 6 の説明> | <正解の選択肢の番号> | <解説>              | <問題の出題分野> |

翻訳対象の csv ファイルは[`data`](./data/.keep)配下に配置することを推奨としています。

### ノートブックの実行

`main_explanation.py`を実行することで、指定した csv ファイルの内容を Azure OpenAI Service を使って翻訳し、詳細解説を追加した csv ファイルを出力します。

実行は、以下のコマンドを実行してください。

```sh
poetry run python main_explanation.py
```

---

## 技術要素

- コア
  - Python 3.11 系
  - Poetry 2 系
- ライブラリ
  - [prompty](https://github.com/microsoft/prompty)
  - [Pydantic](https://docs.pydantic.dev/latest/)
- プロンプトファイル
  - 翻訳プロンプト [notebooks/prompty/translate/main.prompty](./notebooks/prompty/translate/main.prompty)
  - 評価プロンプト [notebooks/prompty/judge/main.prompty](./notebooks/prompty/judge/main.prompty)
