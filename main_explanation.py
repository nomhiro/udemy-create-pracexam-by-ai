import os
import csv
from pprint import pprint

from util.model import PracticeTestItem, UdemyPracticeTestItem
from util.openai_service import create_explanation_practice_test_item
from util.udemy_csv_convert import update_csv_header

target_csv_file_path = './data/ProjectManagement_Sample.csv'
result_csv_file_path = './data/ProjectManagement_Sample_modified.csv'

current_path = os.getcwd()
target_path = os.path.join(current_path, target_csv_file_path)

# csvファイルの読み込み
input_items: list[PracticeTestItem] = []
with open(target_path, "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        item = PracticeTestItem.from_csv_row(row=row)
        input_items.append(item)

items_count = len(input_items)
print(f"{items_count}件の問題文を読み込みました。")
if items_count > 1:
    print("入力データの先頭1件を表示します。")
    pprint(input_items[0].model_dump())


# execute the prompt
raw_responses = []
results: list[UdemyPracticeTestItem] = []
for i, input_item in enumerate(input_items, start=1):
    print(f"{i}問目の問題文の詳細解説をします。")
    response = create_explanation_practice_test_item(item=input_item)
    results.append(response)
    pprint(response.model_dump())

print("詳細解説が完了しました。")


current_path_path = os.getcwd()
result_csv_file_path = os.path.join(current_path_path, result_csv_file_path)

with open(result_csv_file_path, "w") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].model_dump().keys())
    writer.writeheader()
    writer.writerows([result.model_dump() for result in results])

print(f"詳細解説を生成しました。CSVヘッダーの修正を行います。")

# CSVのヘッダーを修正
new_header = [
    "Question", "Question Type", "Answer Option 1", "Explanation 1",
    "Answer Option 2", "Explanation 2", "Answer Option 3", "Explanation 3",
    "Answer Option 4", "Explanation 4", "Answer Option 5", "Explanation 5",
    "Answer Option 6", "Explanation 6", "Correct Answers", "Overall Explanation", "Domain"
]

update_csv_header(result_csv_file_path, new_header)

print(f"最終結果を{result_csv_file_path}に保存しました。")
