from typing import Optional, List

from pydantic import BaseModel
from enum import Enum as PyEnum


class Role(PyEnum):
    STUDENT = "Student"
    TEACHER_RESEARCHER = "Teacher/Researcher"
    ADMINISTRATOR = "Administrator"
    OTHER = "Other"


class TimeInSeedbed(PyEnum):
    LESS_THAN_ONE_YEAR = "Less than one year"
    ONE_TO_TWO_YEARS = "One to two years"
    MORE_THAN_TWO_YEARS = "More than two years"


class QuestionType(PyEnum):
    UNIQUE_SELECTION = "Unique selection"
    MULTIPLE_SELECTION = "Multiple selection"
    FREE_TEXT = "Free text"


class RespondentCreate(BaseModel):
    id: int
    username: str
    full_name: str
    role: Optional[Role] = Role.OTHER
    other_role: Optional[str] = None
    is_seedling: bool = False
    time_in_seedbed: Optional[TimeInSeedbed] = None


class Respondent(BaseModel):
    id: int
    name: str
    role: Role
    other_role: str
    is_seedling: bool
    time_in_seedbed: Optional[TimeInSeedbed]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "role": "Student",
                "other_role": "Teacher/Researcher",
                "is_seedling": True,
                "time_in_seedbed": "Less than one year",
            }
        }


class ResponseOptionCreate(BaseModel):
    text: str


class QuestionCreate(BaseModel):
    text: str
    type: QuestionType
    options: Optional[List[ResponseOptionCreate]] = []

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "text": "text",
                "type": "Multiple selection",
                "options": [
                    {"text": "A). Rojo"},
                    {"text": "B). Azul"},
                    {"text": "C). Verde"}
                ]
            }
        }


class ResponseOption(BaseModel):
    id: int
    question_id: int
    text: str

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "question_id": 1,
                "text": "Response",
            }
        }


class Question(BaseModel):
    id: int
    text: str
    type: QuestionType
    options: Optional[List[ResponseOption]] = []

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "text": "Question",
                "type": "Unique selection",
                "options": []
            }
        }


class SurveyResponseInput(BaseModel):
    respondent_id: int
    question_id: int
    response_option_id: Optional[int] = None
    text_response: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "respondent_id": 1,
                "question_id": 1,
                "response_option_id": 2,
                "text_response": None
            }
        }


class SurveyResponse(BaseModel):
    id: int
    respondent_id: int
    question_id: int
    response_option_id: Optional[int]
    text: Optional[str]

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "respondent_id": 1,
                "question_id": 1,
                "response_option_id": 1,
                "text": None
            }
        }
