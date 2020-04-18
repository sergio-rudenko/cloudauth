from typing import List
from fastapi import Depends, APIRouter, Header, HTTPException
from sqlalchemy.orm import Session

from app import conf, models, schemas
from app.data import get_db

router = APIRouter()


def check_authorised(token: str, admin_access_required: bool = False):
    if not admin_access_required:
        return token == conf.ADMIN_TOKEN or token == conf.USER_TOKEN
    else:
        return token == conf.ADMIN_TOKEN


# database functions ---------------------------------------------------------
def db_get_user_by_phone(db: Session, user_phone: str):
    return db.query(models.User).filter(models.User.phone == user_phone).first()


def db_add_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def db_add_token(db: Session, token: schemas.TokenCreate, user_id: int):
    db_token = models.Token(user_id=user_id, key=token.key, description=token.description)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def db_add_auth_hash(db: Session, auth_hash: schemas.HashCreate, user_id: int):
    db_auth_hash = models.Hash(user_id=user_id, key=auth_hash.key, description=auth_hash.description)
    db.add(db_auth_hash)
    db.commit()
    db.refresh(db_auth_hash)
    return db_auth_hash


# Endpoint	    HTTP Method	    CRUD Method	    Result
# /notes/	    GET	            READ	        get all notes
# /notes/:id/	GET	            READ	        get a single note
# /notes/	    POST	        CREATE	        add a note
# /notes/:id/	PUT	            UPDATE	        update a note
# /notes/:id/	DELETE	        DELETE	        delete a note

# admin ----------------------------------------------------------------------
@router.get("/users/", tags=['admin'], response_model=List[schemas.User])
async def read_user_list(offset: int = 0, limit: int = 100, x_token: str = Header(...), db: Session = Depends(get_db)):
    if not check_authorised(token=x_token, admin_access_required=True):
        raise HTTPException(status_code=401, detail="Admin Token Required")
    return db.query(models.User).offset(offset).limit(limit).all()


@router.get("/tokens/", tags=['admin'], response_model=List[schemas.Token])
async def read_token_list(offset: int = 0, limit: int = 100, x_token: str = Header(...), db: Session = Depends(get_db)):
    if not check_authorised(token=x_token, admin_access_required=True):
        raise HTTPException(status_code=401, detail="Admin Token Required")
    return db.query(models.Token).offset(offset).limit(limit).all()


@router.get("/hashes/", tags=['admin'], response_model=List[schemas.Hash])
async def read_auth_hash_list(offset: int = 0, limit: int = 100, x_token: str = Header(...),
                              db: Session = Depends(get_db)):
    if not check_authorised(token=x_token, admin_access_required=True):
        raise HTTPException(status_code=401, detail="Admin Token Required")
    return db.query(models.Hash).offset(offset).limit(limit).all()


@router.get("/user", tags=['admin', 'CRUD'], response_model=schemas.User)
async def read_user(auth_hash: str = None, lk_token: str = None, phone: str = None,
                    x_token: str = Header(...), db: Session = Depends(get_db)):
    if not phone and not auth_hash and not lk_token:
        raise HTTPException(status_code=400, detail="Parameter Required")

    if phone:
        if not check_authorised(token=x_token, admin_access_required=True):
            raise HTTPException(status_code=401, detail="Admin Token Required")

        db_user = db_get_user_by_phone(db, phone)
        if not db_user:
            raise HTTPException(status_code=404, detail="Not Found")
        return db_user

    else:
        if not check_authorised(token=x_token, admin_access_required=False):
            raise HTTPException(status_code=401, detail="Not Authorised")

        if auth_hash:
            db_hash = db.query(models.Hash).filter(models.Hash.key == auth_hash).first()
            if not db_hash:
                raise HTTPException(status_code=404, detail="Not Found")
            user_id = db_hash.user_id

        if lk_token:
            db_token = db.query(models.Token).filter(models.Token.key == lk_token).first()
            if not db_token:
                raise HTTPException(status_code=404, detail="Not Found")
            user_id = db_token.user_id

        return db.query(models.User).filter(models.User.id == user_id).first()


@router.delete("/user/{phone}/", tags=['admin'], status_code=204)
async def read_user(phone: str = None, x_token: str = Header(...), db: Session = Depends(get_db)):
    if not check_authorised(token=x_token, admin_access_required=True):
        raise HTTPException(status_code=401, detail="Admin Token Required")

    db_user = db_get_user_by_phone(db, phone)
    if not db_user:
        raise HTTPException(status_code=404, detail="Not Found")

    db_hash_list = db.query(models.Hash).filter(models.Hash.user_id == db_user.id).all()
    for db_hash in db_hash_list:
        db.delete(db_hash)
    db.commit()

    db_token_list = db.query(models.Token).filter(models.Token.user_id == db_user.id).all()
    for db_token in db_token_list:
        db.delete(db_token)
    db.commit()

    db.delete(db_user)
    db.commit()
    return None


# CRUD -----------------------------------------------------------------------
@router.post('/tokens/', tags=['CRUD'], status_code=201, response_model=schemas.Token)
def create_user_token(payload: schemas.TokenCreate, x_token: str = Header(...), db: Session = Depends(get_db)):
    if not check_authorised(token=x_token):
        raise HTTPException(status_code=401, detail="Not Authorised")

    db_user = db_get_user_by_phone(db, payload.user_phone)
    if not db_user:
        db_user = db_add_user(db, schemas.UserCreate(
            phone=payload.user_phone,
            description='created by create_user_token'
        ))

    db_token = db.query(models.Token).filter(models.Token.key == payload.key).first()
    if db_token:
        raise HTTPException(status_code=409, detail="Already Exists")

    return db_add_token(db, payload, db_user.id)


@router.post('/hashes/', tags=['CRUD'], status_code=201, response_model=schemas.Hash)
def create_user_hash(payload: schemas.HashCreate, x_token: str = Header(...), db: Session = Depends(get_db)):
    if not check_authorised(token=x_token):
        raise HTTPException(status_code=401, detail="Not Authorised")

    db_user = db_get_user_by_phone(db, payload.user_phone)
    if not db_user:
        db_user = db_add_user(db, schemas.UserCreate(
            phone=payload.user_phone,
            description='created by create_user_hash'
        ))

    db_hash = db.query(models.Hash).filter(models.Hash.key == payload.key).first()
    if db_hash:
        raise HTTPException(status_code=409, detail="Already Exists")

    return db_add_auth_hash(db, payload, db_user.id)


@router.delete("/hashes/{auth_hash}/", tags=['CRUD'], status_code=204)
async def read_user(auth_hash: str = None, x_token: str = Header(...), db: Session = Depends(get_db)):
    if not check_authorised(token=x_token):
        raise HTTPException(status_code=401, detail="Not Authorised")

    db_hash = db.query(models.Hash).filter(models.Hash.key == auth_hash).first()
    if not db_hash:
        raise HTTPException(status_code=404, detail="Not Found")

    db.delete(db_hash)
    db.commit()
    return None


@router.delete("/tokens/{lk_token}/", tags=['CRUD'], status_code=204)
async def read_user(lk_token: str = None, x_token: str = Header(...), db: Session = Depends(get_db)):
    if not check_authorised(token=x_token):
        raise HTTPException(status_code=401, detail="Not Authorised")

    db_token = db.query(models.Token).filter(models.Token.key == lk_token).first()
    if not db_token:
        raise HTTPException(status_code=404, detail="Not Found")

    db.delete(db_token)
    db.commit()
    return None
