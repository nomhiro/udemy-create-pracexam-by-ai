origin_csv_file_path = './data/AZ305forJapan_76-100.csv'
result_csv_file_path = './data/AZ305forJapan_76-100_translated.csv'
judge_result_csv_file_path = './data/AZ305forJapan_76-100_judged.csv'

import os
import csv

from model import PracticeTestItem, JudgeResultItem
from openai_service import judge_practice_test_item

current_path = os.getcwd()
origin_csv_file_path = os.path.join(current_path, origin_csv_file_path)
result_csv_file_path = os.path.join(current_path, result_csv_file_path)

# 翻訳元csvファイルの読み込み
origin_items: list[PracticeTestItem] = []
with open(origin_csv_file_path, "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        item = PracticeTestItem.from_csv_row(row=row)
        origin_items.append(item)

# 翻訳結果csvファイルの読み込み
result_items: list[PracticeTestItem] = []
with open(result_csv_file_path, "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        item = PracticeTestItem.from_csv_row(row=row)
        result_items.append(item)

assert len(origin_items) == len(result_items)
print("評価対象のデータの読み込みが完了しました。")



raw_responses = []
judge_results: list[JudgeResultItem] = []
for i, (origin_item, result_item) in enumerate(zip(origin_items, result_items), start=1):
    print(f"{i}問目の問題文を評価します。")
    inputs = {
        "origin": origin_item.model_dump(),
        "translation_result": result_item.model_dump(),
    }
    response = judge_practice_test_item(origin=origin_item, translation_result=result_item)
    print(f"評価結果: {response}")
    judge_results.append(response)

print("評価が完了しました。")



current_path_path = os.getcwd()

judge_result_csv_file_path = os.path.join(current_path_path, judge_result_csv_file_path)

with open(judge_result_csv_file_path, "w") as f:
    writer = csv.DictWriter(f, fieldnames=judge_results[0].model_dump().keys())
    writer.writeheader()
    writer.writerows([judge_result.model_dump() for judge_result in judge_results])

print(f"評価結果を{judge_result_csv_file_path}に保存しました。")
