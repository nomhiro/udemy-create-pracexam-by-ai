# 実践試験問題作成プロジェクト

本リポジトリには Azure OpenAI Service を使って試験問題に詳細解説を追加し、Udemy形式のCSVに変換するPythonプロジェクトが含まれています。

本プロジェクトを使うことで以下のことができます。

- 過去問の情報をもとに、詳細な解説を追加する（Udemyの試験問題のCSV形式に変換）
- 元の試験問題（csv ファイル）と詳細解説追加後の試験問題（csv ファイル）を渡して、結果の評価をする

https://www.youtube.com/watch?v=RaEJStqLsIw

## 使い方

### プロジェクトの clone

はじめに本リポジトリを clone します。

```sh
git clone <このリポジトリのURL>
```

次に VSCode を使ってプロジェクトを開きます。

```sh
code ./create-pracexam-by-ai
```

### 実行環境のセットアップ

プロジェクトの実行には`python`（3.11系）と`poetry`（2系）が必要です。

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

./dataフォルダ内にCSVファイルを格納しましょう。

AI推論前の過去問CSVファイルの形式
Question Type：単一選択問題の場合は「multiple-choice」、複数選択問題の場合は「multi-select」を指定してください。
| Question | Question Type | Answer Option 1 | Answer Option 2 | Answer Option 3 | Answer Option 4 | Correct Answers | Overall Explanation |
| -------- | ------------- | --------------- | --------------- | --------------- | --------------- | --------------- | ------------------- |
| <英語の試験問題文> | <問題の出題形式> | <回答の選択肢 1> | <回答の選択肢 2> | <回答の選択肢 3> | <回答の選択肢 4> | <正解の選択肢の番号> | <解説> |

AI推論後の csv ファイルは以下の構造になります。
**なお 1 行目はヘッダーになります。各列の意味的な配置が指定された構造に従っている必要があります。**

| Question           | Question Type    | Answer Option 1  | Explanation 1            | Answer Option 2  | Explanation 2           | Answer Option 3  | Explanation 3            | Answer Option 4   | Explanation 4            | Answer Option 5  | Explanation 5           | Answer Option 6  | Explanation 6           | Correct Answers      | Overall Explanation | Domain           |
| ------------------ | ---------------- | ---------------- | ------------------------ | ---------------- | ----------------------- | ---------------- | ------------------------ | ----------------- | ------------------------ | ---------------- | ----------------------- | ---------------- | ----------------------- | -------------------- | ------------------- | ---------------- |
| <英語の試験問題文> | <問題の出題形式> | <回答の選択肢 1> | <回答の選択肢 1 の説明>  | <回答の選択肢 2> | <回答の選択肢 2 の説明> | <回答の選択肢 3> | <回答の選択肢 3 の説明>  | <回答の選択肢 4>  | <回答の選択肢 4 の説明>  | <回答の選択肢 5> | <回答の選択肢 5 の説明> | <回答の選択肢 6> | <回答の選択肢 6 の説明> | <正解の選択肢の番号> | <解説>              | <問題の出題分野> |

### プロジェクトの実行

#### 詳細解説の追加

`main_explanation.py`を実行することで、指定した csv ファイルの内容を Azure OpenAI Service を使って詳細解説を追加し、Udemy形式の csv ファイルを出力します。

```sh
poetry run python main_explanation.py
```

#### 結果の評価

`main_judge.py`を実行することで、元の試験問題と詳細解説追加後の試験問題を比較評価します。

```sh
poetry run python main_judge.py
```

---

## プロジェクト構成

```
/
├── data/                           # データファイル
│   ├── ProjectManagement_Sample.csv         # 入力用サンプルCSV
│   ├── ProjectManagement_Sample_modified.csv # 出力用CSV
│   └── sample/                     # サンプルデータ
├── prompty/                        # プロンプトファイル
│   ├── translate/                  # 詳細解説追加用プロンプト
│   └── judge/                      # 評価用プロンプト
├── util/                           # ユーティリティモジュール
│   ├── model.py                    # データモデル定義
│   ├── openai_service.py          # Azure OpenAI Service連携
│   └── udemy_csv_convert.py       # CSV変換ユーティリティ
├── main_explanation.py             # 詳細解説追加メイン処理
├── main_judge.py                  # 評価メイン処理
├── pyproject.toml                 # Poetry設定ファイル
└── README.md                      # 本ファイル
```

## 技術要素

- コア
  - Python 3.11 系
  - Poetry 2 系
- ライブラリ
  - [prompty](https://github.com/microsoft/prompty) - Azure OpenAI Service連携
  - [Pydantic](https://docs.pydantic.dev/latest/) - データモデル定義
- プロンプトファイル
  - 詳細解説追加プロンプト [prompty/translate/main.prompty](./prompty/translate/main.prompty)
  - 評価プロンプト [prompty/judge/main.prompty](./prompty/judge/main.prompty)
