from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from sqlmodel import  select
from starlette import status
from apps.forms import ProfileResponse
from apps.models import User, engine
from typing import Annotated, Optional
from fastapi import Depends
from sqlmodel import Session
from apps.utils import verify_token

app = FastAPI()



security = HTTPBearer()
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/user/get/me" , response_model=ProfileResponse)
async def get_profile(credentials: HTTPAuthorizationCredentials = Depends(security)):
    username = verify_token(credentials.credentials, token_type="access")
    session = Session(engine)
    user = session.exec(select(User).where(User.username==username)).all()[0]
    return user.__dict__


class UserForm(BaseModel):
    name: str
    age: int

class UserUpdate(BaseModel):
    name: Optional[str]
    age: Optional[int]

# ---------- CREATE ----------
@app.post("/user/create", status_code=status.HTTP_201_CREATED, tags=['Crud'])
async def user_create(user_form: UserForm, session: SessionDep):
    instance = User(**user_form.model_dump())
    session.add(instance)
    session.commit()
    session.refresh(instance)  # id ni olish uchun
    return {"message": "Success create!", "status": 201, "data": instance}

# ---------- READ ----------
@app.get("/user/list", tags=['Crud'])
async def user_list(session: SessionDep, offset: int = 0, limit: int = 10):
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return users


# ---------- DETAIL ----------
@app.get("/user/{user_id}", tags=['Crud'])
async def user_detail(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User topilmadi")
    return user

# ---------- UPDATE ----------
@app.patch("/user/{user_id}/update" , tags=['Crud'])
async def user_partial_update(user_id: int, user_form: UserUpdate, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User topilmadi")
    data = user_form.model_dump(exclude_unset=True)  # faqat yuborilgan maydonlar
    for key, value in data.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "Success partial update!", "status": 200, "data": user}


# ---------- DELETE ----------
@app.delete("/user/{user_id}/delete", tags=['Crud'])
async def user_delete(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User topilmadi")
    session.delete(user)
    session.commit()
    return {"message": "Success delete!", "status": 200}




