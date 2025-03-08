from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class People(db.Model):
    __tablename__ = "people"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    height: Mapped[str] = mapped_column(nullable=False)
    hair_color: Mapped[str] = mapped_column(String(), nullable=False)
    planet: Mapped[str] = mapped_column(String())
    eye_color: Mapped[str] = mapped_column()


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "planet":self.planet,
            "height": self.height
            # do not serialize the password, its a security breach
        }


class Favorite(db.Model):
    __tablename__ = 'favorite'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id: Mapped[int] = mapped_column(primary_key=True)
    user_favorite : Mapped[int] = mapped_column(ForeignKey("user.id"))
    planet_favorite: Mapped[int] = mapped_column(ForeignKey("planet.id"))
    people_favorite: Mapped[int] = mapped_column(ForeignKey('people.id'))

    def serialize(self):
         return{
              "id":self.id,
              "user_favorite": self.user_favorite,
              "planet_favorite": self.planet_favorite,
              "people_favorite": self.people_favorite

         }


class Planet(db.Model):
        __tablename__ = 'planet'
        id: Mapped[int] = mapped_column(primary_key=True)
        population: Mapped[str] = mapped_column(nullable=False)
        size: Mapped[str] = mapped_column(nullable=False)
        gas: Mapped[str]

        def serialize(self):
         return{
              "id":self.id,
              "population ": self.population,
              "size": self.size,
              "gas": self.gas

         }

