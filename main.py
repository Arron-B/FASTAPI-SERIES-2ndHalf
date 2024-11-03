from fastapi import FastAPI, HTTPException
from schemas import GenreURLChoices, BandBase, BandCreate, BandWithID

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
async def bands(genre: GenreURLChoices | None = None,
                has_albums: bool = False
                ) -> list[BandWithID]: #sets type as GenreURLChoices or None, then sets the default value to None
                    band_list = [BandWithID(**b) for b in BANDS]

                    if genre:
                        band_list = [
                            b for b in band_list if b.genre.value.lower() == genre.value  #genre.value retrieves the string value of the selected genre Enum member
                        ]


                    if has_albums:
                        band_list = [b for b in band_list if len(b.albums) > 0]

                    return band_list

    # return [
    #     Band(**b) for b in BANDS # ** is like the spread operator (...) in JS. But can only be used on a dictionary. * is used for lists.
    # ]

@app.get('/bands/{band_id}', status_code = 206)
async def band(band_id: int) -> BandWithID:
    band = next((BandWithID(**b) for b in BANDS if b['id'] == band_id), None)
    if band is None:
        # status code 404
        raise HTTPException(status_code=404, detail='Band not found')
    return band

# @app.get('/bands/genre/{genre}')
# async def bands_for_genre(genre: GenreURLChoices) -> list[dict]: #parameter type hints use : and return type hints use ->
#     print(genre.value)
#     return [
#         b for b in BANDS if b['genre'].lower() == genre.value #genre.value retrieves the string value of the selected genre Enum member
#     ]




@app.post('/bands')
async def create_band(band_data: BandCreate) -> BandWithID:
       id = BANDS[-1]['id'] + 1
       band = BandWithID(id=id, **band_data.model_dump()).model_dump()
       BANDS.append(band)
       return band