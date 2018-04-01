# -*- coding: utf-8 -*-
# by dimy44
import appuifw2
import e32
import txtfield


class ListBox(object):
    # by dimy44
    def __init__(self, select_callback=None, double=0, icons=0):
        self.select_callback = select_callback
        self.double = double
        self.icons = icons
        self.lb = appuifw2.Listbox2(select_callback=self.callback, double=double, icons=icons)
        (a, b), (x, y) = appuifw2.app.layout(appuifw2.EControlPane)
        self.window_search = txtfield.New((int(a / 2.5), 0, a - int(a / 2.5), b), txtlimit=5)
        self.window_search.visible(0)
        self.window_search.setpos(int(a / 2.5), y)
        self.window_search.bgcolor(0xffffff)
        self.list_lb = []

    def callback(self):
        if callable(self.select_callback):
            self.select_callback()
        self.window_search.clear()

    def current(self):
        if not self.lb: return
        return self.lb.current_item().index

    def execute(self, lb=None):
        if lb is not None:
            self.list_lb[:] = []
            n = 0
            for i in lb:
                if not self.double and not self.icons:
                    self.list_lb.append(appuifw2.Item(title=i.title, index=n))
                elif not self.double and self.icons:
                    self.list_lb.append(appuifw2.Item(title=i.title, icon=i.icon, index=n))
                elif self.double and not self.icons:
                    self.list_lb.append(appuifw2.Item(title=i.title, subtitle=i.subtitle, index=n))
                elif self.double and self.icons:
                    self.list_lb.append(appuifw2.Item(title=i.title, subtitle=i.subtitle, icon=i.icon, index=n))
                n += 1
        self.edit_lb()
        appuifw2.app.body = self.lb
        self.window_search_show()


    def window_search_show(self):
        self.text = u''
        self.edit() 
        self.window_search.focus(1)


    def window_search_hide(self):
        self.window_search.focus(0)
        self.window_search.visible(0)


    def edit(self):
        if appuifw2.app.body != self.lb:
            self.window_search_hide()
            return
        g = self.window_search.get()
        if self.text != g:
            self.window_search.visible(bool(g))
            self.edit_lb(g)
            self.text = g
        e32.ao_sleep(0.1, self.edit)

    def edit_lb(self, text=u''):
        self.lb.begin_update()
        self.lb.clear()
        if not text:
            self.lb.extend(self.list_lb)
        else:
            text = text.lower()
            for i in self.list_lb:
                if i.title.lower().startswith(text) or \
                self.double and \
                i.subtitle.lower().startswith(text):
                    self.lb.append(i)
        if self.lb:
            self.lb.set_current(0)
        self.lb.end_update()

if __name__ == '__main__':

    '''Список аналогичный для Listbox2'''
    L = []
    for i in zip(range(6), ('a', 'b', 'c', 'A', 'B', 'C')):
        L.append(appuifw2.Item(unicode(i[1]), subtitle=unicode(i[0])))

    t = appuifw2.Text()

    def callback(): #select_callback
        index = lb.current() #индекс
        appuifw2.app.body = t
        t.add(L[index].title)
        t.add(unicode(index))
        appuifw2.app.exit_key_handler = menu

    def menu():
        lb.execute()
        appuifw2.app.exit_key_handler = lock.signal

    lb = ListBox(select_callback=callback, double=1) #экземпляр
    lb.execute(L) #активация
    lock = e32.Ao_lock()
    appuifw2.app.exit_key_handler = lock.signal
    lock.wait()