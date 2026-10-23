from pydantic import BaseModel, Field
from typing import List

class GenerateRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=250)
    notes: str = Field(default="", max_length=12000)
    level: str = Field(default="Beginner", pattern="^(Beginner|Intermediate|Advanced)$")

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str
    explanation: str

class StudyPack(BaseModel):
    title: str
    summary: str
    key_points: List[str]
    quiz: List[QuizQuestion]
    revision_tips: List[str]
