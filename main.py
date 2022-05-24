import asyncio
from get_characters import get_data
from database import db_main

async def main_async():
        print('Start:')
        characters = await get_data()
        await db_main(characters)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main_async())