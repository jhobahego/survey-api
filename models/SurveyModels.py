from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship

from schemas.SurveySchemas import Role, TimeInSeedbed, QuestionType
from config.db import Base


class Respondent(Base):
    __tablename__ = 'respondent'

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    role = Column(Enum(Role), nullable=False)
    other_role = Column(String(100))
    is_seedling = Column(Boolean, nullable=False)
    time_in_seedbed = Column(Enum(TimeInSeedbed))

    responses = relationship("SurveyResponse", back_populates="respondent")


class Question(Base):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    type = Column(Enum(QuestionType), nullable=False)

    options = relationship("ResponseOption", back_populates="question")
    responses = relationship("SurveyResponse", back_populates="question")

    def to_dict(self):
        text = self.text
        question_type = self.type


class ResponseOption(Base):
    __tablename__ = 'response_option'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)

    question = relationship("Question", back_populates="options")
    responses = relationship("SurveyResponse", back_populates="response_option")


class SurveyResponse(Base):
    __tablename__ = 'survey_response'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    respondent_id = Column(Integer, ForeignKey('respondent.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
    response_option_id = Column(Integer, ForeignKey('response_option.id'))

    respondent = relationship("Respondent", back_populates="responses")
    question = relationship("Question", back_populates="responses")
    response_option = relationship("ResponseOption", back_populates="responses")
