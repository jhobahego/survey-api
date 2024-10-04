from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from api.Auth import get_current_user
from api.Respondent_api import check_admin
from config.db import get_db
from models import SurveyModels
from schemas import SurveySchemas

router = APIRouter()


@router.post("/questions/", status_code=201, dependencies=[Depends(check_admin)])
def create_question(question: SurveySchemas.QuestionCreate, db: Session = Depends(get_db)):
    try:
        db_question = SurveyModels.Question(text=question.text, type=question.type)
        db.add(db_question)
        db.flush()

        if question.type != SurveySchemas.QuestionType.FREE_TEXT:
            for option in question.options:
                db_option = SurveyModels.ResponseOption(question_id=db_question.id, text=option.text)
                db.add(db_option)

        db.commit()
        db.refresh(db_question)

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Question with this text already exists")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/questions/", response_model=List[SurveySchemas.Question], dependencies=[Depends(get_current_user)])
def get_questions(skip: int = Query(0, ge=0), limit: int = Query(100, le=100), db: Session = Depends(get_db)):
    questions = db.query(SurveyModels.Question).offset(skip).limit(limit).all()
    return questions


@router.get("/questions/{question_id}", response_model=SurveySchemas.Question, dependencies=[Depends(get_current_user)])
def get_question(question_id: int, db: Session = Depends(get_db)):
    db_question = db.query(SurveyModels.Question).filter(SurveyModels.Question.id == question_id).first()
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@router.get("/questions/{question_id}/options", response_model=List[SurveySchemas.ResponseOption], dependencies=[Depends(get_current_user)])
def get_question_options(question_id: int, db: Session = Depends(get_db)):
    options = db.query(SurveyModels.ResponseOption).filter(SurveyModels.ResponseOption.question_id == question_id).all()
    if not options:
        raise HTTPException(status_code=404, detail="No options found for this question")
    return options


@router.post("/survey-responses/", response_model=SurveySchemas.SurveyResponse,
             dependencies=[Depends(get_current_user)])
def create_survey_response(
        survey_response: SurveySchemas.SurveyResponseInput,
        db: Session = Depends(get_db)
):
    try:
        db_respondent = db.query(SurveyModels.Respondent).filter(
            SurveyModels.Respondent.id == survey_response.respondent_id
        ).first()
        if db_respondent is None:
            raise HTTPException(status_code=404, detail="Respondent not found")

        db_question = db.query(SurveyModels.Question).filter(
            SurveyModels.Question.id == survey_response.question_id
        ).first()
        if db_question is None:
            raise HTTPException(status_code=404, detail="Question not found")

        if db_question.type == SurveySchemas.QuestionType.FREE_TEXT:
            if survey_response.text_response is None or survey_response.text_response.strip() == "":
                raise HTTPException(
                    status_code=400,
                    detail="Text response is required for FREE_TEXT questions"
                )

        if survey_response.response_option_id is not None:
            db_response_option = db.query(SurveyModels.ResponseOption).filter(
                SurveyModels.ResponseOption.id == survey_response.response_option_id,
                SurveyModels.ResponseOption.question_id == survey_response.question_id
            ).first()
            if db_response_option is None:
                raise HTTPException(
                    status_code=404,
                    detail="Response option not found or does not belong to the question"
                )

        db_response = SurveyModels.SurveyResponse(
            respondent_id=survey_response.respondent_id,
            question_id=survey_response.question_id,
            response_option_id=survey_response.response_option_id,
            text=survey_response.text_response
        )
        db.add(db_response)
        db.commit()
        db.refresh(db_response)

        return db_response
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data or constraint violation")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
