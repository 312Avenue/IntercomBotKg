import asyncio
from aiogram import Bot, Dispatcher

from logic import router


with open('token.txt', 'r') as f:
    token = f.read()

bot = Bot(token)
dp = Dispatcher()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)
    

if __name__ == '__main__':
    try:
        print('Work begin!')
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit!')