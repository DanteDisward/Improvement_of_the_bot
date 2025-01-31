from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import crud_functions

crud_functions.initiate_db()
products = crud_functions.get_all_products()

# ======================================================= Bot ==========================================================
api_token = ''
bot = Bot(token=api_token)
dispatcher = Dispatcher(bot, storage=MemoryStorage())

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_calculate = KeyboardButton(text='Рассчитать')
button_info = KeyboardButton(text='Информация')
button_buy = KeyboardButton(text='Купить')
keyboard.row(button_calculate, button_info)
keyboard.add(button_buy)

il_keyboard = InlineKeyboardMarkup()
button_begin = InlineKeyboardButton('Рассчитать норму калорий', callback_data='calories')
button_formula = InlineKeyboardButton('Формула рассчёта', callback_data='formulas')

il_keyboard.row(button_begin, button_formula)

il_list_product = InlineKeyboardMarkup()
button_product1 = InlineKeyboardButton('Product1', callback_data='product_buying')
button_product2 = InlineKeyboardButton('Product2', callback_data='product_buying')
button_product3 = InlineKeyboardButton('Product3', callback_data='product_buying')
button_product4 = InlineKeyboardButton('Product4', callback_data='product_buying')
il_list_product.add(button_product1, button_product2, button_product3, button_product4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dispatcher.message_handler(commands='start')
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=keyboard)


@dispatcher.message_handler(text='Купить')
async def get_buying_list(message):
    for i in products:
        await message.answer(f'Название: {i[1]} | Описание: {i[2]} | Цена: {i[3]}')
        with open(f'image/{i[0]}.jpg', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки:', reply_markup=il_list_product)


@dispatcher.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dispatcher.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=il_keyboard)


@dispatcher.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()


@dispatcher.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dispatcher.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dispatcher.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dispatcher.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norm_cal = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
    await message.answer(f'Ваша норма калорий: {norm_cal}', reply_markup=keyboard)
    await state.finish()


@dispatcher.message_handler(text='Информация')
async def info_about_the_bot(message):
    (await message.answer('Это тренировочный бот.', reply_markup=keyboard))


@dispatcher.message_handler()
async def info_about_the_bot(message):
    await message.answer('Для начала напишите /start', reply_markup=keyboard)


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=True)
