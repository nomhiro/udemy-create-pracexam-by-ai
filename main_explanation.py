import os
import csv
from pprint import pprint

from model import PracticeTestItem, UdemyPracticeTestItem
from openai_service import create_explanation_practice_test_item

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

print(f"翻訳結果を{result_csv_file_path}に保存しました。")
