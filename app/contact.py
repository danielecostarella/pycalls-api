from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .database import get_db

router = APIRouter()


@router.get('/')
def get_contacts(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    contacts = db.query(models.Contact).filter(
        models.Contact.name.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(contacts), 'contacts': contacts}


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_contact(payload: schemas.ContactBaseSchema, db: Session = Depends(get_db)):
    new_contact = models.Contact(**payload.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return {"status": "success", "contact": new_contact}


@router.patch('/{contactId}')
def update_contact(contactId: str, payload: schemas.ContactBaseSchema, db: Session = Depends(get_db)):
    contact_query = db.query(models.Contact).filter(models.Contact.id == contactId)
    db_contact = contact_query.first()

    if not db_contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No contact with this id: {contactId} found')
    update_data = payload.dict(exclude_unset=True)
    contact_query.filter(models.Contact.id == contactId).update(update_data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(db_contact)
    return {"status": "success", "contact": db_contact}


@router.get('/{contactId}')
def get_contact(contactId: str, db: Session = Depends(get_db)):
    contact = db.query(models.Contact).filter(models.Contact.id == contactId).first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No contact with this id: {id} found")
    return {"status": "success", "contact": contact}


@router.delete('/{contactId}')
def delete_contact(contactId: str, db: Session = Depends(get_db)):
    contact_query = db.query(models.Contact).filter(models.Contact.id == contactId)
    contact = contact_query.first()
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No contact with this id: {id} found')
    contact_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
