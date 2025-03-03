from sqlmodel import Field, Relationship, SQLModel


class Hobby(SQLModel, table=True):
    __tablename__: str = "hobby"
    id: int | None = Field(default=None, primary_key=True)
    hobby_name: str
    user_hobbies: list["UserHobby"] = Relationship(back_populates="hobby")


class UserHobby(SQLModel, table=True):
    __tablename__: str = "userhobby"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    hobby_id: int | None = Field(default=None, foreign_key="hobby.id")
    reaction: str | None = None
    severity: str | None = None
    user: "User" = Relationship(back_populates="hobbies")
    hobby: "Hobby" = Relationship(back_populates="user_hobbies")


class User(SQLModel, table=True):
    __tablename__: str = "user"
    id: int | None = Field(default=None, primary_key=True)
    date_of_birth: str | None = Field(default=None, nullable=True)
    first_name: str
    middle_name: str | None = None
    last_name: str
    sex: str
    hobbies: list["UserHobby"] = Relationship(back_populates="user")


Hobby.model_rebuild()
UserHobby.model_rebuild()
User.model_rebuild()
