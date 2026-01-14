# CRUD for KB entries


from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..deps import get_current_user, get_db

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

@router.get("/", response_model=list[schemas.KnowledgeBaseEntry])
def read_entries(skip: int = 0, limit: int = 10,
                 db: Session = Depends(get_db),
                 current_user: schemas.UserInDB = Depends(get_current_user)):
    return crud.get_entries(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.KnowledgeBaseEntry)
def create_entry(entry_in: schemas.KnowledgeBaseEntryCreate,
                 db: Session = Depends(get_db),
                 current_user: schemas.UserInDB = Depends(get_current_user)):
    return crud.create_entry(db, entry_in, current_user.id)

@router.get("/{entry_id}", response_model=schemas.KnowledgeBaseEntry)
def read_entry(entry_id: int,
               db: Session = Depends(get_db),
               current_user: schemas.UserInDB = Depends(get_current_user)):
    entry = crud.get_entry(db, entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@router.put("/{entry_id}", response_model=schemas.KnowledgeBaseEntry)
def update_entry(entry_id: int,
                 entry_in: schemas.KnowledgeBaseEntryUpdate,
                 db: Session = Depends(get_db),
                 current_user: schemas.UserInDB = Depends(get_current_user)):
    entry = crud.update_entry(db, entry_id, entry_in)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry

@router.delete("/{entry_id}", status_code=204)
def delete_entry(entry_id: int,
                 db: Session = Depends(get_db),
                 current_user: schemas.UserInDB = Depends(get_current_user)):
    success = crud.delete_entry(db, entry_id)
    if not success:
        raise HTTPException(status_code=404, detail="Entry not found")
    return None
