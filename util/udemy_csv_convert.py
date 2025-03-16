import csv


def update_csv_header(file_path: str, new_header: list[str]):
    """
    CSVファイルのヘッダーを更新する関数

    :param file_path: CSVファイルのパス
    :param new_header: 新しいヘッダーのリスト
    """
    # 現在の内容を読み込む
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # フィールド名を新しいヘッダーに合わせて変換
    fieldname_map = {
        "Question": "Question",
        "QuestionType": "Question Type",
        "AnswerOption1": "Answer Option 1",
        "Explanation1": "Explanation 1",
        "AnswerOption2": "Answer Option 2",
        "Explanation2": "Explanation 2",
        "AnswerOption3": "Answer Option 3",
        "Explanation3": "Explanation 3",
        "AnswerOption4": "Answer Option 4",
        "Explanation4": "Explanation 4",
        "AnswerOption5": "Answer Option 5",
        "Explanation5": "Explanation 5",
        "AnswerOption6": "Answer Option 6",
        "Explanation6": "Explanation 6",
        "CorrectAnswers": "Correct Answers",
        "OverallExplanation": "Overall Explanation",
        "Domain": "Domain"
    }

    # 行のフィールド名を変換
    converted_rows = []
    for row in rows:
        converted_row = {fieldname_map.get(k, k): v for k, v in row.items()}
        converted_rows.append(converted_row)

    # 新しいヘッダーでCSVを書き直す
    with open(file_path, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=new_header)
        writer.writeheader()
        writer.writerows(converted_rows)

    print(f"修正されたヘッダーで翻訳結果を{file_path}に保存しました。")
