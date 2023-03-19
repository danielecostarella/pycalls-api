from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .database import get_db

router = APIRouter()

# Look for a number in the db
@router.get('/{number}')
def get_contact_by_number(number: str, db: Session = Depends(get_db)):
   
    contact = db.query(models.Contact).filter(models.Contact.phonenumber == number).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No contact with this number: {number} found")
    else:
        contact_details = {
            'name': contact.name,
            'phone_number': contact.phonenumber,
        }
    return contact_details, 200
