import asyncio
import requests
import aiohttp
from pprint import pprint

base_url = 'https://swapi.dev/api/people'

async def make_request(char_id, session):
    res = await (await session.get(f'{base_url}/{char_id}/')).json(content_type=None)
    return res


def max_chars():
    response = requests.get(base_url).json()
    return response.get('count')


async def get_params(chars_list, session):
    chars_list = [char for char in chars_list if char.get('detail') != 'Not found'] # Проверка на удаленных персонажей
    characters = []
    for char in chars_list:
        character_dict = {}
        character_dict['id'] = int(''.join(filter(str.isdigit, char.get('url'))))
        character_dict['birth_year'] = char.get('birth_year')
        character_dict['eye_color'] = char.get('eye_color')
        character_dict['films'] = ','.join(str(i) for i in [(await (await session.get(film)).json(content_type=None)).get('title') for film in char.get('films')]) 
        character_dict['gender'] = char.get('gender')
        character_dict['hair_color'] = char.get('hair_color')
        character_dict['height'] = char.get('height')
        character_dict['homeworld'] = (await (await session.get(char.get('homeworld'))).json(content_type=None)).get('name')
        character_dict['mass'] = char.get('mass')
        character_dict['name'] = char.get('name')
        character_dict['skin_color'] = char.get('skin_color')
        character_dict['species'] = ','.join(str(i) for i in [(await (await session.get(item)).json(content_type=None)).get('name') for item in char.get('species')])
        character_dict['starships'] = ','.join(str(i) for i in [(await (await session.get(item)).json(content_type=None)).get('name') for item in char.get('starships')])
        character_dict['vehicles'] = ','.join(str(i) for i in [(await (await session.get(item)).json(content_type=None)).get('name') for item in char.get('vehicles')])

        characters.append(character_dict)
        
        return characters


async def get_data():
    chars_count = int(max_chars())
    chars_list = []
    async with aiohttp.ClientSession() as session:
        chars_list = [make_request(char_id, session) for char_id in range(1, chars_count + 1)]
        chars = await asyncio.gather(*chars_list)
        res = await get_params(chars, session)

    return res

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())