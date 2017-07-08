# coding=utf-8
import json
from time import time

import pymysql
from kivy.adapters.dictadapter import DictAdapter
from kivy.app import App
from os.path import dirname, join
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, \
    ListProperty, ObjectProperty, partial
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.listview import ListItemButton, ListItemLabel, CompositeListItem, ListView
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from math import log, log10
from fixtures import integers_dict
import sqlite3


class MainView(GridLayout):
    def __init__(self, **kwargs):
        kwargs['cols'] = 2
        super(MainView, self).__init__(**kwargs)

        args_converter = lambda row_index, rec: {
            'text': rec['text'],
            'size_hint_y': None,
            'height': 25,
            'cls_dicts': [{'cls': ListItemButton,
                           'kwargs': {'text': rec['text']}},
                          {
                              'cls': ListItemLabel,
                              'kwargs': {
                                  'text': "Middle-{0}".format(rec['text']),
                                  'is_representing_cls': True}},
                          {
                              'cls': ListItemButton,
                              'kwargs': {'text': rec['text']}}]}

        item_strings = ["{0}".format(index) for index in range(100)]

        dict_adapter = DictAdapter(sorted_keys=item_strings,
                                   data=integers_dict,
                                   args_converter=args_converter,
                                   selection_mode='single',
                                   allow_empty_selection=False,
                                   cls=CompositeListItem)

        # Use the adapter in our ListView:
        list_view = ListView(adapter=dict_adapter)
        self.add_widget(list_view)


Builder.load_string('''
# define how clabel looks and behaves
<CLabel>:
  canvas.before:
    Color:
      rgb: self.bgcolor
    Rectangle:
      size: self.size
      pos: self.pos

<HeaderLabel>:
  canvas.before:
    Color:
      rgb: self.bgcolor
    Rectangle:
      size: self.size
      pos: self.pos
'''
                    )


class CLabel(ToggleButton):
    bgcolor = ListProperty([1, 1, 1])


class HeaderLabel(Label):
    bgcolor = ListProperty([0.108, 0.476, 0.611])


data_json = open('data.json')
data = json.load(data_json)

header = ['ID', 'Nome', 'Preco', 'IVA']
col_size = [0.1, 0.5, 0.2, 0.2]
# body_alignment = ["center", "left", "right", "right"]
body_alignment = ["center", "center", "center", "center"]

products_list = []

counter = 0


class DataGrid(GridLayout):
    def add_row(self, row_data, row_align, cols_size, instance, **kwargs):
        global counter
        self.rows += 1

        # self.rows = 2
        ##########################################################
        def change_on_press(self):
            childs = self.parent.children
            for ch in childs:
                if ch.id == self.id:
                    print(ch.id)
                    print(len(ch.id))
                    row_n = 0
                    if len(ch.id) == 11:
                        row_n = ch.id[4:5]
                    else:
                        row_n = ch.id[4:6]
                    for c in childs:
                        if ('row_' + str(row_n) + '_col_0') == c.id:
                            if c.state == "normal":
                                c.state = "down"
                            else:
                                c.state = "normal"
                        if ('row_' + str(row_n) + '_col_1') == c.id:
                            if c.state == "normal":
                                c.state = "down"
                            else:
                                c.state = "normal"
                        if ('row_' + str(row_n) + '_col_2') == c.id:
                            if c.state == "normal":
                                c.state = "down"
                            else:
                                c.state = "normal"
                        if ('row_' + str(row_n) + '_col_3') == c.id:
                            if c.state == "normal":
                                c.state = "down"
                            else:
                                c.state = "normal"

        def change_on_release(self):
            if self.state == "normal":
                self.state = "down"
            else:
                self.state = "normal"

        ##########################################################
        n = 0
        for item in row_data:
            cell = CLabel(text=('[color=000000]' + item + '[/color]'),
                          background_normal="background_normal.png",
                          background_down="background_pressed.png",
                          halign=row_align[n],
                          markup=True,
                          on_press=partial(change_on_press),
                          on_release=partial(change_on_release),
                          text_size=(0, None),
                          size_hint_x=cols_size[n],
                          size_hint_y=None,
                          height=40,
                          id=("row_" + str(counter) + "_col_" + str(n)))
            cell_width = Window.size[0] * cell.size_hint_x
            cell.text_size = (cell_width - 30, None)
            cell.texture_update()
            self.add_widget(cell)
            n += 1
        counter += 1

    # self.rows += 1
    def remove_row(self, n_cols, instance, **kwargs):
        childs = self.parent.children
        selected = 0
        for ch in childs:
            for c in reversed(ch.children):
                if c.id != "Header_Label":
                    if c.state == "down":
                        self.remove_widget(c)
                        print(str(c.id) + '   -   ' + str(c.state))
                        selected += 1
        if selected == 0:
            for ch in childs:
                count_01 = n_cols
                count_02 = 0
                count = 0
                while (count < n_cols):
                    if n_cols != len(ch.children):
                        for c in ch.children:
                            if c.id != "Header_Label":
                                print("Length: " + str(len(ch.children)))
                                print("N_cols: " + str(n_cols + 1))

                                self.remove_widget(c)
                                count += 1
                                break
                            else:
                                break
                    else:
                        break

    def select_all(self, instance, **kwargs):
        childs = self.parent.children
        for ch in childs:
            for c in ch.children:
                if c.id != "Header_Label":
                    c.state = "down"

    def unselect_all(self, instance, **kwargs):
        childs = self.parent.children
        for ch in childs:
            for c in ch.children:
                if c.id != "Header_Label":
                    c.state = "normal"

    def show_log(self, instance, **kwargs):
        childs = self.parent.children
        for ch in childs:
            for c in ch.children:
                if c.id != "Header_Label":
                    print(str(c.id) + '   -   ' + str(c.state) + '   -   ' + str(c.text))

    def __init__(self, header_data, body_data, b_align, cols_size, **kwargs):
        super(DataGrid, self).__init__(**kwargs)
        self.size_hint_y = None
        self.bind(minimum_height=self.setter('height'))
        self.cols = len(header_data)
        self.rows = len(body_data) + 1
        self.spacing = [1, 1]
        n = 0
        for hcell in header_data:
            header_str = "[b]" + str(hcell) + "[/b]"
            self.add_widget(HeaderLabel(text=header_str,
                                        markup=True,
                                        size_hint_y=None,
                                        height=40,
                                        id="Header_Label",
                                        size_hint_x=cols_size[n]))
            n += 1


class Tables(ListItemLabel):
    pass


class ShowcaseScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(ShowcaseScreen, self).add_widget(*args)


class ShowcaseApp(App):
    firstcol = StringProperty()
    secondcol = StringProperty()
    thirdcol = StringProperty()
    data = []

    # liste = ObjectProperty()
    # liste2 = ObjectProperty()
    # liste3 = ObjectProperty()

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])

    def build(self):
        self.title = 'STATICAL TOOL '
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}
        self.available_screens = [
            'WELCOME', 'SETTLEMENT STUDIES', 'POPULATION STUDIES', 'TRANSPORTATION STUDIES',
            'ROAD TRAFFIC ANALYSIS', 'TRAFFIC ANALYSIS', 'MainView']
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens',
                                       '{}.kv'.format(fn)) for fn in self.available_screens]
        self.go_next_screen()

    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_current_title(self, instance, value):
        self.root.ids.spnr.text = value

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        # self.update_sourcecode()

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name
        # self.update_sourcecode()

    def go_screen(self, idx):
        self.index = idx
        self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
        # self.update_sourcecode()

    def go_hierarchy_previous(self):
        ahr = self.hierarchy
        if len(ahr) == 1:
            return
        if ahr:
            ahr.pop()
        if ahr:
            idx = ahr.pop()
            self.go_screen(idx)

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index].lower())
        self.screens[index] = screen
        return screen

    '''def read_sourcecode(self):
        fn = self.available_screens[self.index].lower()
        with open(fn) as fd:
            return fd.read()

    def toggle_source_code(self):
        self.show_sourcecode = not self.show_sourcecode
        if self.show_sourcecode:
            height = self.root.height * .3
        else:
            height = 0

        Animation(height=height, d=.3, t='out_quart').start(
                self.root.ids.sv)

        self.update_sourcecode()

    def update_sourcecode(self):
        if not self.show_sourcecode:
            self.root.ids.sourcecode.focus = False
            return
        self.root.ids.sourcecode.text = self.read_sourcecode()
        self.root.ids.sv.scroll_y = 1'''

    def showcase_floatlayout(self, layout):

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 5:
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
#:import random random.random
Button:
    size_hint: random(), random()
    pos_hint: {'x': random(), 'y': random()}
    text:
        'size_hint x: {} y: {}\\n pos_hint x: {} y: {}'.format(\
            self.size_hint_x, self.size_hint_y, self.pos_hint['x'],\
            self.pos_hint['y'])
'''))
            Clock.schedule_once(add_button, 1)

        Clock.schedule_once(add_button)

    def showcase_boxlayout(self, layout):

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 5:
                layout.orientation = 'vertical' \
                    if layout.orientation == 'horizontal' else 'horizontal'
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
Button:
    text: self.parent.orientation if self.parent else ''
'''))
            Clock.schedule_once(add_button, 1)

        Clock.schedule_once(add_button)

    def showcase_gridlayout(self, layout):

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 15:
                layout.rows = 3 if layout.rows is None else None
                layout.cols = None if layout.rows == 3 else 3
                layout.clear_widgets()
            layout.add_widget(Builder.load_string('''
Button:
    text:
        'rows: {}\\ncols: {}'.format(self.parent.rows, self.parent.cols)\
        if self.parent else ''
'''))
            Clock.schedule_once(add_button, 1)

        Clock.schedule_once(add_button)

    def showcase_stacklayout(self, layout):
        orientations = ('lr-tb', 'tb-lr',
                        'rl-tb', 'tb-rl',
                        'lr-bt', 'bt-lr',
                        'rl-bt', 'bt-rl')

        def add_button(*t):
            if not layout.get_parent_window():
                return
            if len(layout.children) > 11:
                layout.clear_widgets()
                cur_orientation = orientations.index(layout.orientation)
                layout.orientation = orientations[cur_orientation - 1]
            layout.add_widget(Builder.load_string('''
Button:
    text: self.parent.orientation if self.parent else ''
    size_hint: .2, .2
'''))
            Clock.schedule_once(add_button, 1)

        Clock.schedule_once(add_button)

    def showcase_anchorlayout(self, layout):

        def change_anchor(self, *l):
            if not layout.get_parent_window():
                return
            anchor_x = ('left', 'center', 'right')
            anchor_y = ('top', 'center', 'bottom')
            if layout.anchor_x == 'left':
                layout.anchor_y = anchor_y[anchor_y.index(layout.anchor_y) - 1]
            layout.anchor_x = anchor_x[anchor_x.index(layout.anchor_x) - 1]

            Clock.schedule_once(change_anchor, 1)

        Clock.schedule_once(change_anchor, 1)

    """   def add_col(self):
        # # Get the text from textInput
        # column_one = '{}'.format(self.firstcol)
        # column_two = '{}'.format(self.secondcol)
        # column_three = '{}'.format(self.thirdcol)
        #
        # # Add to ListView
        # self.liste.adapter.data.extend([column_one])
        # self.liste2.adapter.data.extend([column_two])
        # self.liste3.adapter.data.extend([column_three])
        #
        # # Reset the ListView
        # self.liste._trigger_reset_populate()
        # self.liste2._trigger_reset_populate()
        # self.liste3._trigger_reset_populate()
        pass

    def del_col(self):
        pass

    def replace_col(self):
        # # if a list item is selected
        # if self.liste.adapter.selection:
        #     # Get the text from  item selected
        #     selection = self.liste.adapter.selection[0].text
        #
        #     # Remove the matching item
        #     self.liste.adapter.data.remove(selection)
        #     # Get the text from TextInput
        #     column_one = self.firstcol.text
        #
        #     # Add the Updated data to the ListView
        #     self.liste.adapter.data.extend([column_one])
        #
        #     # Reset the ListView
        #     self.liste._trigger_reset_populate()
        pass
        """

    def _update_clock(self, dt):
        self.time = time()

    def poop(self):
        pop1 = ModalView(size_hint=(.5, .5), auto_dismiss=True)
        rount = GridLayout(cols=1, rows=8)

        ester = Button(text="POPULATION PROJECTION", background_color=(0, 0, .9, .5))
        po1 = TextInput(hint_text='population at initial date', input_filter='int', write_tab=False)
        po2 = TextInput(hint_text='population at a later date', input_filter='int', write_tab=False)
        yr1 = TextInput(hint_text='year of initial date', input_filter='int', write_tab=False)
        yr2 = TextInput(hint_text='year of later date', input_filter='int', write_tab=False)
        yrt = TextInput(hint_text='year of future date', input_filter='int', write_tab=False)
        result = Label()

        def pop_projectn(self):

            if po1.text != '' and po2.text != '' and yr1.text != '' and yr2 != '' and yrt != '':
                pe1 = int(po1.text)
                p3 = int(po2.text)
                yer1 = int(yr1.text)
                yer2 = int(yr2.text)
                yert = int(yrt.text)
                n = yer2 - yer1
                n2 = yert - yer2
                r = pow(10, ((log10(p3 / pe1)) / n)) - 1
                r2 = round(r, 3)
                red = round(p3 * (1 + r2) ** n2, 1)
                result.text = str(red)
            else:
                d = Popup(title='Wrong Input', size_hint=(.4, .3), auto_dismiss=True)
                b = Button(text='textinputs cannot be empty', on_press=d.dismiss)
                d.add_widget(b)
                d.open()

        b = BoxLayout()

        cal_proj = Button(text='CALCULATE PROJECTION')
        # noinspection PyTypeChecker
        backhome = Button(text='back home', on_press=pop1.dismiss)
        b.add_widget(cal_proj)
        b.add_widget(backhome)

        rount.add_widget(ester)
        rount.add_widget(po1)
        rount.add_widget(po2)
        rount.add_widget(yr1)
        rount.add_widget(yr2)
        rount.add_widget(yrt)
        rount.add_widget(result)
        rount.add_widget(b)
        pop1.add_widget(rount)

        pop1.open()
        cal_proj.bind(on_press=pop_projectn)

    def popden(self):
        pop1 = ModalView(size_hint=(.7, .5), auto_dismiss=True)
        rount = GridLayout(cols=1, rows=7)
        ester = Button(text='POPULATION DENSITY', background_color=(0, 0, .9, .5))
        po1 = TextInput(hint_text='population at initial date', input_filter='int', write_tab=False)
        po2 = TextInput(hint_text='Area in Km2', input_filter='int', write_tab=False)
        result = Label()

        def cal_pop_den(self):
            if po1.text != '' and po2.text != '':
                pe1 = int(po1.text)
                p3 = int(po2.text)
                r = round((pe1 / p3), 0)
                result.text = str(r)
            else:
                d = Popup(title='Wrong Input', size_hint=(.5, .5), auto_dismiss=True)
                b = Button(text='textinputs cannot be empty', on_press=d.dismiss)
                d.add_widget(b)
                d.open()

        b = BoxLayout()
        cal_proj = Button(text='CALCULATE POPULATON DENSITY')
        backhome = Button(text='back home', on_press=pop1.dismiss)
        b.add_widget(cal_proj)
        b.add_widget(backhome)

        rount.add_widget(ester)
        rount.add_widget(po1)
        rount.add_widget(po2)
        rount.add_widget(result)
        rount.add_widget(b)
        pop1.add_widget(rount)

        pop1.open()
        cal_proj.bind(on_press=cal_pop_den)

    def sex_ratio(self):
        pop1 = ModalView(size_hint=(.7, .3), auto_dismiss=True)
        rount = GridLayout(cols=1, rows=7)

        ester = Button(text=' SEX RATIO', background_color=(0, 0, .9, .5))
        po1 = TextInput(hint_text='Number of Males', input_filter='int', write_tab=False)
        po2 = TextInput(hint_text='Number of females', input_filter='int', write_tab=False)
        result = Label(text='text')

        def cal_sex_ratio(self):
            if po1.text != '' and po2.text != '':
                pe1 = int(po1.text)
                p3 = int(po2.text)
                r = round((pe1 / p3) * 100, 0)
                result.text = str(r)
            else:
                d = Popup(title='Wrong Input', size_hint=(.5, .5), auto_dismiss=True)
                b = Button(text='textinputs cannot be empty', on_press=d.dismiss)
                d.add_widget(b)
                d.open()

        b = BoxLayout()
        cal_proj = Button(text='CALCULATE SEX RATIO')
        backhome = Button(text='back home', on_press=pop1.dismiss)
        b.add_widget(cal_proj)
        b.add_widget(backhome)

        rount.add_widget(ester)
        rount.add_widget(po1)
        rount.add_widget(po2)
        rount.add_widget(result)
        rount.add_widget(b)
        pop1.add_widget(rount)

        pop1.open()
        cal_proj.bind(on_press=cal_sex_ratio)

    def depend_ratio(self):
        pop1 = ModalView(size_hint=(.7, .5), auto_dismiss=True)
        rount = GridLayout(cols=1, rows=7)

        ester = Button(text='DEPENDENCY RATIO', background_color=(0, 0, .9, .5))
        po1 = TextInput(hint_text='Children under Age 15', input_filter='int', write_tab=False)
        po2 = TextInput(hint_text='Adult over Age 65 ', input_filter='int', write_tab=False)
        po3 = TextInput(hint_text='Adults between ade 15 and 64', input_filter='int', write_tab=False)

        result = Label(text='text')

        def cal_depend_ratio(self):
            if po1.text != '' and po2.text != '' and po3.text != '':
                pe1 = int(po1.text)
                p3 = int(po2.text)
                pe3 = int(po3.text)
                r = round(((pe1 + p3) / pe3) * 100, 0)
                result.text = str(r)
            else:
                d = Popup(title='Wrong Input', size_hint=(.5, .3), auto_dismiss=True)
                b = Button(text='textinputs cannot be empty', on_press=d.dismiss)
                d.add_widget(b)
                d.open()

        b = BoxLayout()
        cal_proj = Button(text='CALCULATE DENPENDENCY RATIO')
        backhome = Button(text='back home', on_press=pop1.dismiss)
        b.add_widget(cal_proj)
        b.add_widget(backhome)

        rount.add_widget(ester)
        rount.add_widget(po1)
        rount.add_widget(po2)
        rount.add_widget(po3)
        rount.add_widget(result)
        rount.add_widget(b)
        pop1.add_widget(rount)

        pop1.open()
        cal_proj.bind(on_press=cal_depend_ratio)

    def yong_dend_ratio(self):
        pop1 = ModalView(size_hint=(.9, .5), auto_dismiss=True)
        rount = GridLayout(cols=1, rows=7)
        ester = Button(text='YOUNG DEPENDENCY RATIO', background_color=(0, 0, .9, .5))
        po1 = TextInput(hint_text='Children under Age 15', input_filter='int', write_tab=False)
        po2 = TextInput(hint_text='Adults between ade 15 and 64', input_filter='int', write_tab=False)

        result = Label(text='text')

        def cal_young_dend_ratio(self):
            if po1.text != '' and po2.text != '':
                pe1 = int(po1.text)
                p3 = int(po2.text)
                r = round((pe1 / p3) * 100, 0)
                result.text = str(r)
            else:
                d = Popup(title='Wrong Input', size_hint=(.5, .3), auto_dismiss=True)
                b = Button(text='textinputs cannot be empty', on_press=d.dismiss)
                d.add_widget(b)
                d.open()

        b = BoxLayout()
        cal_proj = Button(text='CALCULATE  YOUNG DENPENDENCY RATIO')
        backhome = Button(text='back home', on_press=pop1.dismiss)
        b.add_widget(cal_proj)
        b.add_widget(backhome)

        rount.add_widget(ester)
        rount.add_widget(po1)
        rount.add_widget(po2)
        rount.add_widget(result)
        rount.add_widget(b)
        pop1.add_widget(rount)

        pop1.open()
        cal_proj.bind(on_press=cal_young_dend_ratio)

    def old_depend_ratio(self):
        pop1 = ModalView(size_hint=(.7, .5), auto_dismiss=True)
        rount = GridLayout(cols=1, rows=7)

        ester = Button(text="OLD DEPENDECNY RATIO", background_color=(0, 0, .9, .5))
        po1 = TextInput(hint_text='A', input_filter='int', write_tab=False)
        po2 = TextInput(hint_text='Area in Km2', input_filter='int', write_tab=False)
        po3 = TextInput(hint_text='Area in Km2', input_filter='int', write_tab=False)

        result = Label(text='text')

        def cal_young_dend_ratio(self):
            if po1.text != '' and po2.text != '':
                pe1 = int(po1.text)
                p3 = int(po2.text)
                r = round((pe1 / p3) * 100, 0)
                result.text = str(r)
            else:
                d = Popup(title='Wrong Input', size_hint=(.5, .3), auto_dismiss=True)
                b = Button(text='textinputs cannot be empty', on_press=d.dismiss)
                d.add_widget(b)
                d.open()

        b = BoxLayout()
        cal_proj = Button(text='CALCULATE OLD DENPENDENCY RATIO')
        backhome = Button(text='back home', on_press=pop1.dismiss)
        b.add_widget(cal_proj)
        b.add_widget(backhome)

        rount.add_widget(ester)
        rount.add_widget(po1)
        rount.add_widget(po2)
        rount.add_widget(po3)
        rount.add_widget(result)
        rount.add_widget(b)
        pop1.add_widget(rount)

        pop1.open()
        cal_proj.bind(on_press=cal_young_dend_ratio)

    def crud_det_ratio(self):
        pop1 = ModalView(size_hint=(.7, .5), auto_dismiss=True)
        rount = GridLayout(cols=1, rows=7)

        ester = Button(text='CRUDE DEATH RATIO', background_color=(0, 0, .9, .5))
        po1 = TextInput(hint_text='A', input_filter='int', write_tab=False)
        po2 = TextInput(hint_text='Area in Km2', input_filter='int', write_tab=False)
        po3 = TextInput(hint_text='Area in Km2', input_filter='int', write_tab=False)
        result = Label(text='text')

        def cal_young_dend_ratio(self):
            if po1.text != '' and po2.text != '':
                pe1 = int(po1.text)
                p3 = int(po2.text)
                r = round((pe1 / p3) * 100, 0)
                result.text = str(r)
            else:
                d = Popup(title='Wrong Input', size_hint=(.5, .3), auto_dismiss=True)
                b = Button(text='textinputs cannot be empty', on_press=d.dismiss)
                d.add_widget(b)
                d.open()

        b = BoxLayout()
        cal_proj = Button(text='CALCULATE CRUDE DEATH RATIO')
        backhome = Button(text='back home', on_press=pop1.dismiss)
        b.add_widget(cal_proj)
        b.add_widget(backhome)

        rount.add_widget(ester)
        rount.add_widget(po1)
        rount.add_widget(po2)
        rount.add_widget(po3)
        rount.add_widget(result)
        rount.add_widget(b)
        pop1.add_widget(rount)

        pop1.open()
        cal_proj.bind(on_press=cal_young_dend_ratio)

    def crud_bet_ratio(self):
        pop1 = ModalView(size_hint=(.7, .5), auto_dismiss=True)
        rount = GridLayout(cols=1, rows=7)

        ester = Button(text='CRUDE BIRTH RATIO', background_color=(0, 0, .9, .5))
        po1 = TextInput(hint_text='A', input_filter='int', write_tab=False)
        po2 = TextInput(hint_text='Area in Km2', input_filter='int', write_tab=False)
        po3 = TextInput(hint_text='Area in Km2', input_filter='int', write_tab=False)
        result = Label(text='text')

        def cal_young_dend_ratio(self):
            if po1.text != '' and po2.text != '':
                pe1 = int(po1.text)
                p3 = int(po2.text)
                r = round((pe1 / p3) * 100, 0)
                result.text = str(r)
            else:
                d = Popup(title='Wrong Input', size_hint=(.5, .5), auto_dismiss=True)
                b = Button(text='textinputs cannot be empty', on_press=d.dismiss)
                d.add_widget(b)
                d.open()

        b = BoxLayout()
        cal_proj = Button(text='CALCULATE CRUDE BIRTH RATIO')
        backhome = Button(text='back home', on_press=pop1.dismiss)
        b.add_widget(cal_proj)
        b.add_widget(backhome)

        rount.add_widget(ester)
        rount.add_widget(po1)
        rount.add_widget(po2)
        rount.add_widget(po3)
        rount.add_widget(result)
        rount.add_widget(b)
        pop1.add_widget(rount)

        pop1.open()
        cal_proj.bind(on_press=cal_young_dend_ratio)

    def nat_increase(self):
        pop1 = ModalView(size_hint=(.6, .5), auto_dismiss=True)
        rount = GridLayout(cols=1, rows=7)

        ester = Button(text='NATIONAL INCREASE', background_color=(0, 0, .9, .5))
        po1 = TextInput(hint_text='A', input_filter='int', write_tab=False)
        po2 = TextInput(hint_text='Area in Km2', input_filter='int', write_tab=False)
        po3 = TextInput(hint_text='Area in Km2', input_filter='int', write_tab=False)
        result = Label(text='text')

        def cal_young_dend_ratio(self):
            if po1.text != '' and po2.text != '':
                pe1 = int(po1.text)
                p3 = int(po2.text)
                r = round((pe1 / p3) * 100, 0)
                result.text = str(r)
            else:
                d = Popup(title='Wrong Input', size_hint=(.4, .3), auto_dismiss=True)
                b = Button(text='textinputs cannot be empty', on_press=d.dismiss)
                d.add_widget(b)
                d.open()

        b = BoxLayout()
        cal_proj = Button(text='CALCULATE NATURAL INCREASE')
        backhome = Button(text='back home', on_press=pop1.dismiss)
        b.add_widget(cal_proj)
        b.add_widget(backhome)

        rount.add_widget(ester)
        rount.add_widget(po1)
        rount.add_widget(po2)
        rount.add_widget(po3)
        rount.add_widget(result)
        rount.add_widget(b)
        pop1.add_widget(rount)

        pop1.open()
        cal_proj.bind(on_press=cal_young_dend_ratio)

    def fat_rate(self):
        pop1 = ModalView(size_hint=(.7, .3), auto_dismiss=True)
        rount = GridLayout(cols=1, rows=7)

        ester = Button(text='FAT RATE', background_color=(0, 0, .9, .5))
        po1 = TextInput(hint_text='A', input_filter='int', write_tab=False)
        po2 = TextInput(hint_text='Area in Km2', input_filter='int', write_tab=False)
        po3 = TextInput(hint_text='Area in Km2', input_filter='int', write_tab=False)
        result = Label(text='text')

        def cal_young_dend_ratio(self):
            if po1.text != '' and po2.text != '':
                pe1 = int(po1.text)
                p3 = int(po2.text)
                r = round((pe1 / p3) * 100, 0)
                result.text = str(r)
            else:
                d = Popup(title='Wrong Input', size_hint=(.5, .5), auto_dismiss=True)
                b = Button(text='textinputs cannot be empty', on_press=d.dismiss)
                d.add_widget(b)
                d.open()

        b = BoxLayout()
        cal_proj = Button(text='CALCULATE FERTILITY RATE')
        backhome = Button(text='back home', on_press=pop1.dismiss)
        b.add_widget(cal_proj)
        b.add_widget(backhome)

        rount.add_widget(ester)
        rount.add_widget(po1)
        rount.add_widget(po2)
        rount.add_widget(po3)
        rount.add_widget(result)
        rount.add_widget(b)
        pop1.add_widget(rount)

        pop1.open()
        cal_proj.bind(on_press=cal_young_dend_ratio)

    def age_index(self):
        pop1 = ModalView(size_hint=(.6, .3), auto_dismiss=True)
        rount = GridLayout(cols=1, rows=7)
        ester = Button(text='AGEING INDEX', background_color=(0, 0, .9, .5))
        po1 = TextInput(hint_text='A', input_filter='int', write_tab=False)
        po2 = TextInput(hint_text='Area in Km2', input_filter='int', write_tab=False)
        po3 = TextInput(hint_text='Area in Km2', input_filter='int', write_tab=False)
        result = Label(text='text')

        def cal_young_dend_ratio(self):
            if po1.text != '' and po2.text != '':
                pe1 = int(po1.text)
                p3 = int(po2.text)
                r = round((pe1 / p3) * 100, 0)
                result.text = str(r)
            else:
                d = Popup(title='Wrong Input', size_hint=(.5, .5), auto_dismiss=True)
                b = Button(text='textinputs cannot be empty', on_press=d.dismiss)
                d.add_widget(b)
                d.open()

        b = BoxLayout()
        cal_proj = Button(text='CALCULATE AGEING INDEX')
        backhome = Button(text='back home', on_press=pop1.dismiss)
        b.add_widget(cal_proj)
        b.add_widget(backhome)

        rount.add_widget(ester)
        rount.add_widget(po1)
        rount.add_widget(po2)
        rount.add_widget(po3)
        rount.add_widget(result)
        rount.add_widget(b)
        pop1.add_widget(rount)

        pop1.open()
        cal_proj.bind(on_press=cal_young_dend_ratio)
        ###

    def grrid(self):
        grid = DataGrid(header, data, body_alignment, col_size)
        grid.rows = 10

        scroll = ScrollView(size_hint=(1, 1), size=(400, 500000), scroll_y=0, pos_hint={'center_x': .5, 'center_y': .5})
        scroll.add_widget(grid)
        scroll.do_scroll_y = True
        scroll.do_scroll_x = False

        pp = partial(grid.add_row, ['001', 'Teste', '4.00', '4.00'], body_alignment, col_size)
        add_row_btn = Button(text="Add Row", on_press=pp)
        del_row_btn = Button(text="Delete Row", on_press=partial(grid.remove_row, len(header)))
        upt_row_btn = Button(text="Update Row")
        slct_all_btn = Button(text="Select All", on_press=partial(grid.select_all))
        unslct_all_btn = Button(text="Unselect All", on_press=partial(grid.unselect_all))

        show_grid_log = Button(text="Show log", on_press=partial(grid.show_log))

        def modal_insert(self):
            lbl1 = Label(text='ID', id="lbl")
            lbl2 = Label(text='Nome', id="lbl")
            lbl3 = Label(text='Preco', id="lbl")
            lbl4 = Label(text='IVA', id="lbl")
            txt1 = TextInput(text='000', id="txtinp", input_filter='int')
            txt2 = TextInput(text='Product Name', id="txtinp")
            txt3 = TextInput(text='123.45', id="txtinp", input_filter='float')
            txt4 = TextInput(text='23', id="txtinp", input_filter='int')

            insertion_grid = GridLayout(cols=2)
            insertion_grid.add_widget(lbl1)
            insertion_grid.add_widget(txt1)
            insertion_grid.add_widget(lbl2)
            insertion_grid.add_widget(txt2)
            insertion_grid.add_widget(lbl3)
            insertion_grid.add_widget(txt3)
            insertion_grid.add_widget(lbl4)
            insertion_grid.add_widget(txt4)
            # create content and assign to the view

            content = Button(text='Close me!')

            modal_layout = BoxLayout(orientation="vertical")
            modal_layout.add_widget(insertion_grid)

            def insert_def(self):
                input_list = []
                for text_inputs in reversed(self.parent.children[2].children):
                    if text_inputs.id == "txtinp":
                        input_list.append(text_inputs.text)
                print(input_list)
                grid.add_row(input_list, body_alignment, col_size, self)

            # print view
            # view.dismiss


            insert_btn = Button(text="Insert", on_press=insert_def)
            modal_layout.add_widget(insert_btn)
            modal_layout.add_widget(content)

            view = ModalView(auto_dismiss=False)

            view.add_widget(modal_layout)
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=view.dismiss)
            insert_btn.bind(on_release=view.dismiss)

            view.open()

        add_custom_row = Button(text="Add Custom Row", on_press=modal_insert)

        ###
        def json_fill(self):
            for d in data:
                print(d)
                self.grid.add_row(d, body_alignment, col_size, self)

        json_fill_btn = Button(text="JSON fill", on_press=partial(json_fill))

        btn_grid = BoxLayout(orientation="vertical")
        rnk = Button(text=' Rank', size_hint_y=None, height='48dp')
        rnk1 = Button(text=' Fraction', size_hint_y=None, height='48dp')
        rnk2 = Button(text=' Predicted', size_hint_y=None, height='48dp')
        rnk3 = Button(text=' Analog', size_hint_y=None, height='48dp')
        rnk4 = Button(text=' PopLog', size_hint_y=None, height='48dp')
        rnk5 = Button(text=' Residual', size_hint_y=None, height='48dp')
        rnk6 = Button(text=' Settlement Index', size_hint_y=None, height='48dp')
        rnk7 = Button(text=' Sphere of Influence', size_hint_y=None, height='48dp')
        backhome = Button(text='back home')

        btn_grid.add_widget(add_custom_row)
        btn_grid.add_widget(del_row_btn)
        btn_grid.add_widget(upt_row_btn)
        btn_grid.add_widget(slct_all_btn)
        btn_grid.add_widget(unslct_all_btn)
        btn_grid.add_widget(rnk)
        btn_grid.add_widget(rnk1)
        btn_grid.add_widget(rnk2)
        btn_grid.add_widget(rnk3)
        btn_grid.add_widget(rnk4)
        btn_grid.add_widget(rnk5)
        btn_grid.add_widget(rnk6)
        btn_grid.add_widget(rnk7)
        btn_grid.add_widget(backhome)

        root = BoxLayout(orientation="horizontal")
        root.add_widget(scroll)
        root.add_widget(btn_grid)

        f = Popup(content=root, title='SETTLEMENT STUDIES')
        backhome.bind(on_press=f.dismiss)
        f.open()

    def table_view(self):
        tabl = ModalView()
        grids = GridLayout(cols=1)
        create_col1 = Button(text='add Row')
        create_col2 = Button(text='delete Row')
        create_clo3 = Button(text='update Row')

        textinput1 = TextInput(hint_text='settlement')
        textinput2 = TextInput(input_filter='int', hint_text='population')
        textinput3 = TextInput(input_filter='int', hint_text='rank')
        textinput4 = TextInput(input_filter='int', hint_text='fraction')
        dd = GridLayout(cols=7)
        dd.add_widget(create_col1)
        dd.add_widget(create_col2)
        dd.add_widget(create_clo3)
        dd.add_widget(textinput1)
        dd.add_widget(textinput2)
        dd.add_widget(textinput3)
        dd.add_widget(textinput4)

        ged = GridLayout(cols=4)
        d = Label(text = 'id')
        creat_col1 = Button(text='Settlement')
        creat_col2 = Button(text='population')
        creat_clo3 = Button(text='Rank')
        creat_clo4 = Button(text='Fraction')


        # ged.add_widget(d)
        ged.add_widget(creat_col1)
        ged.add_widget(creat_col2)
        ged.add_widget(creat_clo3)
        ged.add_widget(creat_clo4)

        grids.add_widget(dd)
        grids.add_widget(ged)
        ss = ScrollView()

        ss.add_widget(grids)
        tabl.add_widget(ss)

        tabl.open()

        def table_insert(self):
            db = pymysql.connect("localhost", "root", "",'table')
            cursor = db.cursor()
            sql = """INSERT INTO polpulation (settlement,population,rank,fraction) VALUES \
                        ('%s','%d',%d,'%f')""" % (str(textinput1.text),int(textinput2.text),int(textinput3.text),
                                                 float(textinput4.text))
            cursor.execute(sql)
            db.commit()
            results = cursor.fetchall()
            for row in results:
                fname = row[0]
                lname = row[1]

            giv = GridLayout(cols = 4)


            giv.add_widget(Label(text=str(textinput1.text),id='lad' ))
            giv.add_widget(Label(text=str(textinput2.text),id = 'lad'))
            giv.add_widget(Label(text=str(textinput3.text),id = 'lad'))
            giv.add_widget(Label(text=str(textinput4.text),id='lad'))
            ss = ScrollView()
            ss.add_widget(giv)
            grids.add_widget(ss)

        def delet(self):
            db = pymysql.connect("localhost", "root", "", 'table')
            cursor = db.cursor()
            sql = """SELECT * FROM polpulation WHERE settlement = '%s' """ % (textinput1.text)
        def updat(self):
            db = pymysql.connect("localhost", "root", "", 'table')
            cursor = db.cursor()
            sql = """SELECT * FROM polpulation """
            cursor.execute(sql)
            db.commit()
            results = cursor.fetchall()
            for row in results:
                f1 = row[0]
                f2 = row[1]
                f3 = row[2]
                f4 = row[3]


                skill = ScrollView()

                giv = GridLayout(cols=4)

                giv.add_widget(Label(text=str(f1), id='lad'))
                giv.add_widget(Label(text=str(f2), id='lad'))
                giv.add_widget(Label(text=str(f3), id='lad'))
                giv.add_widget(Label(text=str(f4), id='lad'))
                skill.add_widget(giv)
                grids.add_widget(skill)


            pass

        create_col1.bind(on_press = table_insert)
        create_clo3.bind(on_press = updat)


    def list_view(self):
        mainsf = MainView()
        a = ModalView()
        a.add_widget(mainsf)
        a.open()


if __name__ == '__main__':
    ShowcaseApp().run()
