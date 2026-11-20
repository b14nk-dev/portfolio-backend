from pydantic import BaseModel, field_validator


class QuestionBody(BaseModel):
    question: str

    @field_validator("question")
    @classmethod
    def check_question(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 5:
            raise ValueError("question must contain at least 5 characters")
        if len(value) > 500:
            raise ValueError("question must contain at most 500 characters")
        return value
