from typing import Annotated

from pydantic import BaseModel, StringConstraints

QuestionText = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=5, max_length=500)
]


class QuestionBody(BaseModel):
    question: QuestionText
