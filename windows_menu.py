#-*- coding: utf-8 -*-
# wimdows_menu.py by dimy44;
# 10.2010.
# ;)


import appuifw2 as aw
from topwindow import TopWindow
from graphics import Image
from keycapture import KeyCapturer



class Windows_menu:
    __module__ = __name__


    def __init__(self, items, title=u'Menu:'):
        self.items = items
        self.title = title
        self.capture=KeyCapturer(self.keys_answer)
        self.window_main = TopWindow()
        self.window_add1 = TopWindow()
        self.window_add2 = TopWindow()
        self.y, self.y1, self.y2, self.flag1, self.flag2 = 0, 0, 0, 0, 0
        try:
            self.size_display = aw.app.layout(aw.EScreen)[0]
        except AttributeError:
            self.size_display = (176, 208)


    def initialization(self):
        try:
            self.window_main.shadow = self.shadow
        except AttributeError:
            self.window_main.shadow = 2
        try:
            self.x_pos = self.x_pos
        except AttributeError:
            self.x_pos = 5
        try:
            self.y_pos = self.y_pos
        except AttributeError:
            self.y_pos = 5
        try:
            self.width = self.width
        except AttributeError:
            self.width = self.size_display[0] * 30 / 42
        try:
            self.color_background = self.color_background
        except AttributeError:
            self.color_background = 0xffffff
        try:
            self.color_background_upper = self.color_background_upper
        except AttributeError:
            self.color_background_upper = self.color_background
        try:
            self.color_cursor = self.color_cursor
        except AttributeError:
            self.color_cursor = 0xaaaaaa
        try:
            self.color_text = self.color_text
        except AttributeError:
            self.color_text = 0
        try:
            self.color_text_cursor = self.color_text_cursor
        except AttributeError:
            self.color_text_cursor = self.color_text
        try:
            self.color_text_upper = self.color_text_upper
        except AttributeError:
            self.color_text_upper = self.color_text

        try:
            self.x_pos_add1 = self.x_pos_add1
        except AttributeError:
            self.x_pos_add1 = self.x_pos + 20
        try:
            self.y_pos_add1 = self.y_pos_add1
        except AttributeError:
            self.y_pos_add1 = self.y_pos + 25
        try:
            self.width_add1 = self.width_add1
        except AttributeError:
            self.width_add1 = self.width
        try:
            self.color_background_add1 = self.color_background_add1
        except AttributeError:
            self.color_background_add1 = self.color_background
        try:
            self.color_cursor_add1 = self.color_cursor_add1
        except AttributeError:
            self.color_cursor_add1 = self.color_cursor
        try:
            self.color_text_add1 = self.color_text_add1
        except AttributeError:
            self.color_text_add1 = self.color_text
        try:
            self.color_text_cursor_add1 = self.color_text_cursor_add1
        except AttributeError:
            self.color_text_cursor_add1 = self.color_text_cursor

        try:
            self.x_pos_add2 = self.x_pos_add2
        except AttributeError:
            self.x_pos_add2 = self.x_pos_add1 + 20
        try:
            self.y_pos_add2 = self.y_pos_add2
        except AttributeError:
            self.y_pos_add2 = self.y_pos_add1 + 8
        try:
            self.width_add2 = self.width_add2
        except AttributeError:
            self.width_add2 = self.width_add1
        try:
            self.color_background_add2 = self.color_background_add2
        except AttributeError:
            self.color_background_add2 = self.color_background_add1
        try:
            self.color_cursor_add2 = self.color_cursor_add2
        except AttributeError:
            self.color_cursor_add2 = self.color_cursor_add1
        try:
            self.color_text_add2 = self.color_text_add2
        except AttributeError:
            self.color_text_add2 = self.color_text_add1
        try:
            self.color_text_cursor_add2 = self.color_text_cursor
        except AttributeError:
            self.color_text_cursor_add2 = self.color_text_add2


    def keys(self):
        self.capture.keys = [63495, 63496, 63497, 63498, 63557, 63554] + [i for i in xrange(48, 58)]
        self.capture.forwarding = 0
        aw.app.focus = self.focus
        self.capture.start()


    def focus(self,foc):
        if not foc:
            self.stop_menu()


    def stop_menu(self):
        self.window_main.hide()
        self.window_add1.hide()
        self.window_add2.hide()
        self.capture.stop()
        self.y1, self.y2, self.flag1, self.flag2 = 0, 0, 0, 0
        aw.app.exit_key_handler = self.exit_key_handler_old
        aw.app.exit_key_text = self.exit_key_text_old
        aw.app.menu_key_text = self.menu_key_text_old


    def start_menu(self, exit_key_text=u'Cancel'):
        self.exit_key_handler_old = aw.app.exit_key_handler
        self.exit_key_text_old = aw.app.exit_key_text
        self.menu_key_text_old = aw.app.menu_key_text
        aw.app.menu_key_text = u'Ok'
        aw.app.exit_key_text = exit_key_text
        aw.app.exit_key_handler = self.stop_menu
        self.keys()
        self.picture()


    def keys_answer(self, code):
        if code in xrange(48, 58):
            y = int(chr(code)) - 1
            if y < 0:
                y = 9
            if self.flag2:
                if len(self.items[self.y][2][self.y1][2]) >= y + 1:
                    self.y2 = y
                    self.picture2()
                    aw.e32.ao_sleep(0.2)
                    code = 63557
            elif self.flag1:
                if len(self.items[self.y][2]) >= y + 1:
                    self.y1 = y
                    self.picture1()
                    aw.e32.ao_sleep(0.2)
                    code = 63557
            else:
                if len(self.items) >= y + 1:
                    self.y = y
                    self.picture()
                    aw.e32.ao_sleep(0.2)
                    code = 63557
        elif code == 63498:
            if self.flag2:
                self.y2 += 1
                if self.y2 > len(self.items[self.y][2][self.y1][2]) - 1:
                    self.y2 = 0
                self.picture2()
                return None
            elif self.flag1:
                self.y1 += 1
                if self.y1 > len(self.items[self.y][2]) - 1:
                    self.y1 = 0
                self.picture1()
                return None
            else:
                self.y += 1
                if self.y > len(self.items) - 1:
                    self.y = 0
                self.picture()
                return None
        elif code == 63497:
            if self.flag2:
                self.y2 -= 1
                if self.y2 < 0:
                    self.y2 = len(self.items[self.y][2][self.y1][2]) - 1
                self.picture2()
                return None
            elif self.flag1:
                self.y1 -= 1
                if self.y1 < 0:
                    self.y1 = len(self.items[self.y][2]) - 1
                self.picture1()
                return None
            else:
                self.y -= 1
                if self.y < 0:
                    self.y = len(self.items) - 1
                self.picture()
                return None
        elif code == 63495:
            if self.flag2:
                self.window_add2.hide()
                self.y2, self.flag2 = 0, 0
            elif self.flag1:
                self.window_add1.hide()
                self.y1, self.flag1 = 0, 0
                return None
        elif code == 63496:
            if self.flag1 and self.items[self.y][2][self.y1][1] is '2' and not self.flag2:
                self.flag2 = 1
                self.picture2()
                return None
            elif self.items[self.y][1] is '1' and not self.flag1:
                self.flag1 = 1
                self.picture1()
                return None
        if code == 63557 or code == 63554:
            if not self.flag1:
                if  self.items[self.y][1] is not '1':
                    self.window_main.hide()
                    aw.app.exit_key_handler = self.exit_key_handler_old
                    aw.app.exit_key_text = self.exit_key_text_old
                    aw.app.menu_key_text = self.menu_key_text_old
                    self.items[self.y][1](*self.items[self.y][2:])
                    self.capture.stop()
                    return None
                elif  self.items[self.y][1] is '1':
                    self.flag1 = 1
                    self.picture1()
                    return None
            elif self.flag1 and not self.flag2:
                if  self.items[self.y][2][self.y1][1] is not '2':
                    self.window_main.hide()
                    self.window_add1.hide()
                    aw.app.exit_key_handler = self.exit_key_handler_old
                    aw.app.exit_key_text = self.exit_key_text_old
                    aw.app.menu_key_text = self.menu_key_text_old
                    self.items[self.y][2][self.y1][1](*self.items[self.y][2][self.y1][2:])
                    self.capture.stop()
                    self.y1, self.flag1 = 0, 0
                    return None
                elif  self.items[self.y][2][self.y1][1] is '2':
                    self.flag2 = 1
                    self.picture2()
                    return None
            elif self.flag2:
                self.window_main.hide()
                self.window_add1.hide()
                self.window_add2.hide()
                aw.app.exit_key_handler = self.exit_key_handler_old
                aw.app.exit_key_text = self.exit_key_text_old
                aw.app.menu_key_text = self.menu_key_text_old
                self.items[self.y][2][self.y1][2][self.y2][1](*self.items[self.y][2][self.y1][2][self.y2][2:])
                self.capture.stop()
                self.y1, self.y2, self.flag1, self.flag2 = 0, 0, 0, 0
                return None


    def picture(self):
        try:
            self.window_main.remove_image(self.img, (0, 0))
            del self.img
        except Exception:
            pass
        size = (self.width, len(self.items) * 20 + 20)
        self.img = Image.new(size)
        self.window_main.size = size
        self.window_main.position = (self.x_pos, self.y_pos)
        self.img.rectangle((0, 0, size[0], size[1]), 0x0, self.color_background)
        self.img.rectangle((1, 1, size[0] - 1, 20),fill = self.color_background_upper)
        self.img.rectangle((2, self.y * 20 + 22, size[0] - 2, self.y * 20 + 38),fill = self.color_cursor)
        a = self.img.measure_text(self.title, 'annotation',maxwidth = self.width - 15)
        if len(self.title) > a[2]:
            self.img.text(((self.width - a[0][2]) / 2, 14), self.title[:a[2]-1] + u'...', self.color_text_upper, 'annotation')
        else:
            self.img.text(((self.width - a[0][2]) / 2, 14), self.title, self.color_text_upper, 'annotation')
        d, n = 20, 0
        for t in self.items:
            n += 1
            if n - 1 is not self.y:
                color_text = self.color_text
            else:
                color_text = self.color_text_cursor
            if n < 10:
                i = unicode(n)
            elif n == 10:
                i = u'0'
            else:
                i = u''
            a = self.img.measure_text(i + u' ' + t[0], 'annotation', maxwidth = self.width - 23)
            if len(i + u' ' + t[0]) > a[2]:
                self.img.text((4, 14 + d), i + u' ' + t[0][:a[2]-2] + u'...', color_text, 'annotation')
            else:
                self.img.text((4, 14 + d), i + u' ' + t[0], color_text, 'annotation')
            if t[1] is '1':
                self.img.polygon((self.width - 9, 16 + d, self.width - 9, 4 + d, self.width - 3, 10 + d), fill = color_text)
            d+=20
        self.window_main.add_image(self.img, (0, 0))
        self.window_main.show()


    def picture1(self):
        try:
            self.window_add1.remove_image(self.img_add1, (0, 0))
            del self.img_add1
        except Exception:
            pass
        size = (self.width_add1, len(self.items[self.y][2]) * 20)
        self.img_add1 = Image.new(size)
        self.window_add1.size = size
        self.window_add1.position = (self.x_pos_add1, self.y_pos_add1)
        self.img_add1.rectangle((0, 0, size[0], size[1]), 0x0, self.color_background_add1)
        self.img_add1.rectangle((2, self.y1 * 20 + 2, size[0] - 2, self.y1 * 20 + 18),fill = self.color_cursor_add1)
        d, n = 0, 0
        for t in self.items[self.y][2]:
            n += 1
            if n - 1 is not self.y1:
                color_text = self.color_text_add1
            else:
                color_text = self.color_text_cursor_add1
            if n < 10:
                i = unicode(n)
            elif n == 10:
                i = u'0'
            else:
                i = u''
            a = self.img_add1.measure_text(i + u' ' + t[0], 'annotation', maxwidth = self.width_add1 - 23)
            if len(i + u' ' + t[0]) > a[2]:
                self.img_add1.text((4, 14 + d), i + u' ' + t[0][:a[2]-2] + u'...', color_text, 'annotation')
            else:
                self.img_add1.text((4, 14 + d), i + u' ' + t[0], color_text, 'annotation')
            if t[1] is '2':
                self.img_add1.polygon((self.width_add1 - 9, 16 + d, self.width_add1 - 9, 4 + d, self.width_add1 - 3, 10 + d), fill = color_text)
            d+=20
        self.window_add1.add_image(self.img_add1, (0, 0))
        self.window_add1.show()


    def picture2(self):
        try:
            self.window_add2.remove_image(self.img_add2, (0, 0))
            del self.img_add2
        except Exception:
            pass
        size = (self.width_add2, len(self.items[self.y][2][self.y1][2]) * 20)
        self.img_add2 = Image.new(size)
        self.window_add2.size = size
        self.window_add2.position = (self.x_pos_add2, self.y_pos_add2)
        self.img_add2.rectangle((0, 0, size[0], size[1]), 0x0, self.color_background_add2)
        self.img_add2.rectangle((2, self.y2 * 20 + 2, size[0] - 2, self.y2 * 20 + 18),fill = self.color_cursor_add2)
        d, n = 0, 0
        for t in self.items[self.y][2][self.y1][2]:
            n += 1
            if n - 1 is not self.y2:
                color_text = self.color_text_add2
            else:
                color_text = self.color_text_cursor_add2
            if n < 10:
                i = unicode(n)
            elif n == 10:
                i = u'0'
            else:
                i = u''
            a = self.img_add2.measure_text(i + u' ' + t[0], 'annotation', maxwidth = self.width_add2 - 23)
            if len(i + u' ' + t[0]) > a[2]:
                self.img_add2.text((4, 14 + d), i + u' ' + t[0][:a[2]-2] + u'...', color_text, 'annotation')
            else:
                self.img_add2.text((4, 14 + d), i + u' ' + t[0], color_text, 'annotation')
            d+=20
        self.window_add2.add_image(self.img_add2, (0, 0))
        self.window_add2.show()

# the end :)