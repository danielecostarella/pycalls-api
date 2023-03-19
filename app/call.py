from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .database import get_db

router = APIRouter()


@router.get('/')
def get_calls(db: Session = Depends(get_db), limit: int = 1000, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    calls = db.query(models.Call).filter(
        models.Call.name.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(calls), 'calls': calls}


# Before posting a call look for the name in the Directory db
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_call(payload: schemas.CallBaseSchema, db: Session = Depends(get_db)):

    """ First look for the name into the directory """
    """ Otherwise is Unknown """
    
    # print query result
    #print (whoIs.title+ " is calling from "+ whoIs.content)

    #if not whoIs:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                        detail=f"No call with this id: {id} found")

    new_call = models.Call(**payload.dict())
    db.add(new_call)
    db.commit()
    db.refresh(new_call)
    return {"status": "success", "call": new_call}


@router.patch('/{callId}')
def update_call(callId: str, payload: schemas.CallBaseSchema, db: Session = Depends(get_db)):
    call_query = db.query(models.Call).filter(models.Call.id == callId)
    db_call = call_query.first()

    if not db_call:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No call with this id: {callId} found')
    update_data = payload.dict(exclude_unset=True)
    call_query.filter(models.Call.id == callId).update(update_data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(db_call)
    return {"status": "success", "call": db_call}


@router.get('/{callId}')
def get_call(callId: str, db: Session = Depends(get_db)):
    call = db.query(models.Call).filter(models.Call.id == callId).first()
    if not call:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No call with this id: {id} found")
    return {"status": "success", "call": call}


@router.delete('/{callId}')
def delete_call(callId: str, db: Session = Depends(get_db)):
    call_query = db.query(models.Call).filter(models.Call.id == callId)
    call = call_query.first()
    if not call:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No call with this id: {id} found')
    call_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
