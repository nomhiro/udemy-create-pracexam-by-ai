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
    Question: str
    QuestionType: str
    AnswerOption1: str
    Explanation1: str
    AnswerOption2: str
    Explanation2: str
    AnswerOption3: str
    Explanation3: str
    AnswerOption4: str
    Explanation4: str
    AnswerOption5: str
    Explanation5: str
    AnswerOption6: str
    Explanation6: str
    CorrectAnswers: str
    OverallExplanation: str
    Domain: str

    @classmethod
    def from_csv_row(cls, row: list) -> "UdemyPracticeTestItem":
        return cls(
            Question=row[0],
            QuestionType=row[1],
            AnswerOption1=row[2],
            Explanation1=row[3],
            AnswerOption2=row[4],
            Explanation2=row[5],
            AnswerOption3=row[6],
            Explanation3=row[7],
            AnswerOption4=row[8],
            Explanation4=row[9],
            AnswerOption5=row[10],
            Explanation5=row[11],
            AnswerOption6=row[12],
            Explanation6=row[13],
            CorrectAnswers=row[14],
            OverallExplanation=row[15],
            Domain=row[16],
        )


class JudgeResultItem(BaseModel):
    result: Literal["ok", "ng"]
    comment: str
