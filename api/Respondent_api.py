from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.Auth import get_current_user
from schemas import SurveySchemas
from models import SurveyModels
from config.db import get_db
from decouple import config

router = APIRouter()


def check_admin(current_user: SurveySchemas.Respondent = Depends(get_current_user)):
    if current_user.role != SurveySchemas.Role.ADMINISTRATOR:
        raise HTTPException(status_code=403, detail="You are not an admin")


@router.post("/respondents/", response_model=SurveySchemas.Respondent)
def create_respondent(respondent: SurveySchemas.RespondentCreate, db: Session = Depends(get_db)):
    try:
        db_respondent = SurveyModels.Respondent(
            full_name=respondent.full_name,
            email=respondent.email,
            role=respondent.role,
            other_role=respondent.other_role,
            is_seedling=respondent.is_seedling,
            time_in_seedbed=respondent.time_in_seedbed
        )

        if db_respondent.role == SurveySchemas.Role.ADMINISTRATOR:
            admin_emails = config("ADMIN_EMAILS").split(",")
            if not admin_emails.__contains__(db_respondent.email):
                raise HTTPException(status_code=400, detail="You are not an admin")

        db.add(db_respondent)
        db.commit()
        db.refresh(db_respondent)

        return db_respondent

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username already exists")
    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/respondents/me/", response_model=SurveySchemas.Respondent)
def read_respondent(current_respondent: SurveySchemas.Respondent = Depends(get_current_user)):
    return current_respondent
