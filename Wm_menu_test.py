import appuifw2 as aw
import sys
aw.e32.ao_yield()
sys.path.append('e:\\')
sys.path.append('c:\\')
import windows_menu

def ru(text):
    return text.decode('utf-8')
#-------------------------
# функция для примера работы меню:

aw.app.body = body = aw.Text()
body.font = 'normal'
body.focus = False

def func(t='функция вызвана без аргументов'):
    body.set(ru(t))
    aw.app.exit_key_handler = exit
#-------------------------
# самое главное:

def menu():
    # вкладка внутри вкладки:
    sub_sub_items = ((u'sub_sub_item', func), (u'sub_sub_item', func), (u'sub_sub_item', func), (u'sub_sub_item', func, 'функции передан аргумент')) # кортеж из кортежей вида: (название пункта, функция [,перечисление аргументов]) 

    # вкладка:
    sub_items = ((u'subitem', '2', sub_sub_items), (u'subitem', func), (u'subitem', func), (u'subitem', func, 'функции передан аргумент')) 
    # кортеж из кортежей вида: (название пункта, функция [,перечисление аргументов])
    # но если Вы делаете вкладку, то кортеж: (название пункта, '2', массив под_вкладки (см. выше))
    # где '2' - это флаг, указывающий, что здесь будет под_вкладка

    # главное окно:
    main_items = ((u'main_item', func), (u'main_item', '1', sub_items), (u'main_item', func), (u'main_item', func), (u'main_item', func), (u'main_item', func, 'функции передан аргумент'))
    # кортеж из кортежей вида: (название пункта, функция [,перечисление аргументов])
    # но если Вы делаете вкладку, то кортеж: (название пункта, '1', массив вкладки (см. выше))
    # где '1' - это флаг, указывающий, что здесь будет вкладка
#-------------------------

    global wm
    wm = windows_menu.Windows_menu(main_items, ru('Опции:')) # второй необязательный аргумент - заголовок главного окна, по-умолчанию 'Menu:'
#-------------------------
    # необязательные аттрибуты:
    wm.shadow = 3 # тень

#    wm.x_pos = 5 # коорд. X верхн. левого угла главного окна 
#    wm.y_pos = 5 # коорд. Y верхн. левого угла  главного окна
#    wm.x_pos_add1 = 15 # коорд. X верхн. левого угла  вкладки
#    wm.y_pos_add1 = 15 # коорд. Y верхн. левого угла  вкладки
#    wm.x_pos_add2 = 25 # коорд. X верхн. левого угла  под_вкладки
#    wm.y_pos_add2 = 25 # коорд. Y верхн. левого угла под_вкладки

#    wm.width = 120 # ширина главного окна
#    wm.width_add1 = 100 # ширина окна вкладки
#    wm.width_add2 = 100 # ширина окна под_вкладки

    wm.color_background = 0xeeeeee # цвет фона осн. окна
    wm.color_background_add1 = 0xeeeeee # цвет фона окна первой вкладки
    wm.color_background_add2 = 0xeeeeee # цвет фона окна второй вкладки

    wm.color_background_upper = 0x555555 # цвет фона заголовка

    wm.color_cursor = 0x880000 # цвет курсора осн. окна
    wm.color_cursor_add1 = 0x0000ff # цвет курсора  окна первой вкладки
    wm.color_cursor_add2 = 0xff00ff # цвет курсора  окна второй вкладки
    wm.color_text = 0 # цвет текста осн. окна вне курсора
    wm.color_text_cursor = 0xffffff # цвет текста осн. окна в курсоре
    wm.color_text_add1 = 0 # цвет текста окна первой вкладки вне курсора
    wm.color_text_cursor_add1 = 0xffffff # цвет текста окна первой вкладки в курсоре
    wm.color_text_add2 = 0 # цвет текста окна второй вкладки вне курсора
    wm.color_text_cursor_add2 = 0xffffff # цвет текста окна второй вкладки в курсоре

    wm.color_text_upper = 0xffffff # цвет текста заголовка
#-------------------------
    # инициализация всех параметров:
    wm.initialization()

menu()

# вешаем на клавишу вызов нашего меню;
# необязательный аргумент - надпись над правой софтклавишей
# по умолчанию 'Cancel':
aw.app.menu_key_handler = lambda: wm.start_menu(ru('Отмена'))

aw.app.menu=[]
lock = aw.e32.Ao_lock()
def exit():
    wm.stop_menu() # функция деактивации меню
    lock.signal()
aw.app.exit_key_handler = exit

lock.wait()