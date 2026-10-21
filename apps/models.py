from sqlmodel import Field, SQLModel, create_engine, Relationship


class User(SQLModel, table=True):
    __tablename__ = 'users'
    id: int = Field(primary_key=True)
    name: str
    age: int | None = Field(default=None)
    username : str = Field(unique=True , nullable=False)
    password : str = Field(nullable=False) # HASH
    cars: list['Car'] = Relationship(back_populates="user")




class Car(SQLModel , table =True):
    __tablename__ = 'cars'
    id: int = Field(primary_key=True)
    title : str
    model : str = Field(nullable=False)
    user_id : int = Field(foreign_key='users.id' , ondelete='CASCADE')
    user: 'User' = Relationship(back_populates="cars")


url = 'postgresql://postgres:1@localhost:5433/postgres'
engine = create_engine(url)
SQLModel.metadata.create_all(engine)
