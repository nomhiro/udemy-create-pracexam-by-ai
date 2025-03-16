from typing import Literal
from pydantic import BaseModel


class PracticeTestItem(BaseModel):
    question: str
    question_type: Literal["multiple-choice", "multi-select"]
    answer_option1: str
    answer_option2: str
    answer_option3: str
    answer_option4: str
    answer_option5: str
    answer_option6: str
    correct_answers: str
    overall_explanation: str

    @classmethod
    def from_csv_row(cls, row: list) -> "PracticeTestItem":
        return cls(
            question=row[0],
            question_type=row[1].lower(),
            answer_option1=row[2],
            answer_option2=row[3],
            answer_option3=row[4],
            answer_option4=row[5],
            answer_option5=row[6],
            answer_option6=row[7],
            correct_answers=row[8],
            overall_explanation=row[9],
        )


class UdemyPracticeTestItem(BaseModel):
    question: str
    question_type: str
    answer_option1: str
    explanation1: str
    answer_option2: str
    explanation2: str
    answer_option3: str
    explanation3: str
    answer_option4: str
    explanation4: str
    answer_option5: str
    explanation5: str
    answer_option6: str
    explanation6: str
    correct_answers: str
    overall_explanation: str
    domain: str

    @classmethod
    def from_csv_row(cls, row: list) -> "UdemyPracticeTestItem":
        return cls(
            question=row[0],
            question_type=row[1],
            answer_option1=row[2],
            explanation1=row[3],
            answer_option2=row[4],
            explanation2=row[5],
            answer_option3=row[6],
            explanation3=row[7],
            answer_option4=row[8],
            explanation4=row[9],
            answer_option5=row[10],
            explanation5=row[11],
            answer_option6=row[12],
            explanation6=row[13],
            correct_answers=row[14],
            overall_explanation=row[15],
            domain=row[16],
        )


class JudgeResultItem(BaseModel):
    result: Literal["ok", "ng"]
    comment: str
