from datetime import date
from enum import Enum
from pydantic import BaseModel, validator

class GenreURLChoices(Enum): #for url query params genre checking
    ROCK = 'rock'
    ELECTRONIC = 'electronic'
    METAL = 'metal'
    HIP_HOP = 'hip-hop'

class GenreChoices(Enum): #for post body genre checking
    ROCK = 'Rock'
    ELECTRONIC = 'Electronic'
    METAL = 'Metal'
    HIP_HOP = 'Hip-Hop'


class Album(BaseModel):
    title: str
    release_date: date


class BandBase(BaseModel):
    name: str
    genre: GenreChoices
    albums: list[Album] = [] # sets default value as empty list

class BandCreate(BandBase):
    @validator('genre', pre=True)
    def title_case_genre(cls, value):
        return value.title()              #rock -> Rock

class BandWithID(BandBase):
    id: int