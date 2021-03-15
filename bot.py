import config
import logging
import asyncio, pyowm
from datetime import datetime

from aiogram import Bot, Dispatcher, executor, types
from Classes import MySQL


# ---------------------------------------connecting with bot--------------------
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
#===============================================================================
db = MySQL()

#-----------------------------изменение статуса---------------------------------
@dp.message_handler(commands=['change_status', 'status'])
async def status(message: types.Message):
        if (db.user_exist(message.from_user.id) == True):
            pass
        else:
            db.add_subscriber(message.from_user.id)
            await message.answer("Создан новый пользователь.")
        if db.check_parametrs(message.from_user.id)[0][2] == 0:
            db.update_status(message.from_user.id,1)
        elif db.check_parametrs(message.from_user.id)[0][2] == 1:
            db.update_status(message.from_user.id,0)
        db.commit()
        await message.answer("Вы успешно изменили статус пользования на {}!\n P.s 1 - контроль включен, 0 - контроль отключен.".format(db.check_parametrs(message.from_user.id)[0][2]))

@dp.message_handler(commands=['command=1', 'TurnOFF'])
async def setcommand(message: types.Message):
	if(db.user_exist(message.from_user.id) == False):
		db.add_subscriber(message.from_user.id)
		await message.answer("Пользователь создан. Команда не отправлена, т.к контроль не включен. Чтобы включить контроль запустите команду /status.")
	else:
		if db.check_parametrs(message.from_user.id)[0][2] == 0:
			await message.answer("Команда не отправлена, т.к контроль не включен. Чтобы включить контроль запустите команду /status.")
		else:
			db.send_command(message.from_user.id, 1)
			db.commit()
			await message.answer("Команда принята и будет исполнена через 30 секунд. Сообщение о исполнении придет на почту.")

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
	if(db.user_exist(message.from_user.id) == False):
		await message.answer("Вас приветствует бот для управления и просмотра информации о состоянии вашего рига. \nВ базе нет данных о Вас. Чтобы создать нового пользователя воспользуйтесь командой /new. \n Чтобы просмотреть все команды воспользуйтесь командой /commands.")
	else:
		await message.answer("Вас приветствует бот для управления и просмотра информации о состоянии вашего рига. \nЧтобы просмотреть все возможные команды воспользуйтесь командой /commands")

@dp.message_handler(commands=['commands'])
async def available_commands(message: types.Message):
	if(db.user_exist(message.from_user.id) == False):
		await message.answer("В базе нет данных о Вас. Чтобы создать нового пользователя воспользуйтесь командой /new.\n/show - показывает все установленные данные (Включен/Выключен контроль, выполнены ли все команды, ваш id)\n/status - включает контроль, если он выключен и наоборот.\n/command=? - отдача команды для рига. Вместо знака (?) поставить нужный индекс.")
	else:
		await message.answer("/show - показывает все установленные данные (Включен/Выключен контроль, выполнены ли все команды, ваш id)\n/status - включает контроль, если он выключен и наоборот.\n/command=? - отдача команды для рига. Вместо знака (?) поставить нужный индекс.")
		
@dp.message_handler(commands=['new'])
async def new_user(message: types.Message):
        if (db.user_exist(message.from_user.id) == True):
            await message.answer("Ваш аккаунт уже зарегистрирован")
        else:
            db.add_subscriber(message.from_user.id)
            await message.answer("Создан новый пользователь.")

@dp.message_handler(commands=['show'])
async def show_info(message: types.Message):
        if (db.user_exist(message.from_user.id) == True):
            await message.answer("Ваш личный id (его надо будет указать в программе рига): {}.\nСтатус пользования: {}. (1 - контроль включен,0 - выключен. Чтобы изменить это значение - /status).\nСтатус выполнения команды: {}. (0 - все команды выполнены, любое другое значение - команда ожидает выполнения.)".format(db.check_parametrs(message.from_user.id)[0][1],db.check_parametrs(message.from_user.id)[0][2],db.check_parametrs(message.from_user.id)[0][3]))
        else:
            await message.answer("Сначала создайте нового пользователя /new")



#-------
@dp.message_handler()
async def echo(message: types.Message):
	await message.answer('Нет такой команды.')
#-------




# long polling
if __name__ == '__main__': 
	executor.start_polling(dp, skip_updates=True)