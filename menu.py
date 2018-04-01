import appuifw2 as aw
import sys
aw.e32.ao_yield()
sys.path.append('e:\\')
sys.path.append('c:\\')
import windows_menu

def ru(text):
    return text.decode('utf-8')
#-------------------------
# function for an example of the menu:

aw.app.body = body = aw.Text()
body.font = 'normal'
body.focus = False

def func(t='function is called with no arguments'):
    body.set(ru(t))
    aw.app.exit_key_handler = exit
#-------------------------
# the most important:

def menu():
    # tab within the tab:
    sub_sub_items = ((u'sub_sub_item', func), (u'sub_sub_item', func), (u'sub_sub_item', func), (u'sub_sub_item', func, 'function argument is passed')) # a tuple of tuples of the form: (name of the item, the function [, list of arguments])

    # tab:
    sub_items = ((u'subitem', '2', sub_sub_items), (u'subitem', func), (u'subitem', func), (u'subitem', func, 'function argument is passed'))
    # a tuple of tuples of the form: (name of the item, the function [, list of arguments])
    # but if you make a tab, then the tuple: (name of the item, '2 ', array subtab (see above))
    #where '2 '- a flag indicating that there will be subtab

    # main window:
    main_items = ((u'main_item', func), (u'main_item', '1', sub_items), (u'main_item', func), (u'main_item', func), (u'main_item', func), (u'main_item', func, 'function argument is passed'))
    # a tuple of tuples of the form: (name of the item, the function [, list of arguments])
    # but if you make a tab, then the tuple: (name of the item, '1 ', the array tab (see above))
    # where '1 '- a flag indicating that there will be tab
#-------------------------

    global wm
    wm = windows_menu.Windows_menu(main_items, ru('Options:')) # an optional second argument - the title of the main window by default 'Menu:'
#-------------------------
    # optional attributes:
    wm.shadow = 3 # shadow

#    wm.x_pos = 5 # X coordinate of the upper-left corner of the main window
#    wm.y_pos = 5 # Y coordinate of the upper-left corner of the main window
#    wm.x_pos_add1 = 15 # X coordinate of the upper-left corner of the tab
#    wm.y_pos_add1 = 15 # Y coordinate of the upper-left corner of the tab
#    wm.x_pos_add2 = 25 # X coordinate of the upper left corner of the subtab
#    wm.y_pos_add2 = 25 # Y coordinate of the upper-left corner of the subtab

#    wm.width = 120 # width of the main window
#    wm.width_add1 = 100 # width of the window
#    wm.width_add2 = 100 # width of the window of the second tab

    wm.color_background = 0xeeeeee # background color of the main window
    wm.color_background_add1 = 0xeeeeee # the background color of the windows of the first tab
    wm.color_background_add2 = 0xeeeeee # the background color of the windows of the second tab

    wm.color_background_upper = 0x555555 # the background color of the title

    wm.color_cursor = 0x880000 # the color of the cursor of the main window
    wm.color_cursor_add1 = 0x0000ff # the color of the cursor box first tab
    wm.color_cursor_add2 = 0xff00ff # the color of the cursor window of the second tab
    wm.color_text = 0 # color of the text of the main window out  cursor
    wm.color_text_cursor = 0xffffff # color of the text cursor in the main windowе
    wm.color_text_add1 = 0 # color of the text box is the first tab the cursor
    wm.color_text_cursor_add1 = 0xffffff # color of the text box cursor in the first tab
    wm.color_text_add2 = 0 # color of the text window of the second tab is the cursor
    wm.color_text_cursor_add2 = 0xffffff # color of the text window of the second tab in the cursor

    wm.color_text_upper = 0xffffff # header text color
#-------------------------
    # Initialization of all parameters:
    wm.initialization()

menu()

# hang on the key challenge of our menu;
# optional argument - the sign above the right softkeys
# by default 'Cancel':
aw.app.menu_key_handler = lambda: wm.start_menu(ru('Cancel'))

aw.app.menu=[]
lock = aw.e32.Ao_lock()
def exit():
    wm.stop_menu() # deactivate the function menu
    lock.signal()
aw.app.exit_key_handler = exit

lock.wait()