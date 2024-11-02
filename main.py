from fastapi import FastAPI, HTTPException
from schemas import GenreURLChoices, Band

app = FastAPI()


BANDS = [
    {'id': 1, 'name': 'The Kinks', 'genre': 'Rock'},
    {'id': 2, 'name': 'Aphex Twin', 'genre': 'Electronic'},
    {'id': 3, 'name': 'Black Sabbath', 'genre': 'Metal', 'albums': [
        {'title': 'Master of Reality', 'release_date': '1971-07-21'}
    ]},
    {'id': 4, 'name': 'Wu-Tang Clan', 'genre': 'Hip-Hop'},
]

@app.get('/bands') 
async def bands() -> list[Band]:
    return [
        Band(**b) for b in BANDS # ** is like the spread operator (...) in JS. But can only be used on a dictionary. * is used for lists.
    ]

@app.get('/bands/{band_id}', status_code = 206)
async def band(band_id: int) -> Band:
    band = next((Band(**b) for b in BANDS if b['id'] == band_id), None)
    if band is None:
        # status code 404
        raise HTTPException(status_code=404, detail='Band not found')
    return band

@app.get('/bands/genre/{genre}')
async def bands_for_genre(genre: GenreURLChoices) -> list[dict]: #parameter type hints use : and return type hints use ->
    print(genre.value)
    return [
        b for b in BANDS if b['genre'].lower() == genre.value #genre.value retrieves the string value of the selected genre Enum member
    ]