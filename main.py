from kivy.app import App
from kivy.config import Config
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty
from kivy.core.clipboard import Clipboard
import random
import hashlib, binascii
from urlparse import urlparse
import string

def gen_random_string(password, str_len):
    symbols = string.ascii_letters +string.ascii_letters+string.ascii_letters+string.ascii_letters+ string.punctuation
    hash_str = binascii.hexlify(hashlib.pbkdf2_hmac('sha256', password, b'somesalt',1000, dklen=2*str_len))
    rand_str = ''
    while len(hash_str):
        rand_str += symbols[int(hash_str[:4],16)%len(symbols)]
        hash_str = hash_str[4:]
    return rand_str



class NewPasswordWidget(BoxLayout):
    new_pass = StringProperty()
    resurse_str = StringProperty()

    def to_clipboard(self):
        if self.new_pass != 'Copyed!':
            Clipboard.copy(self.new_pass)
            self.new_pass = 'Copyed!'


class PassGeneratorWindow(BoxLayout):
    error_label_exists = BooleanProperty(True)
    pass_widget = ObjectProperty(None)
    def generate(self,pass_phrace, resurce):
        if self.pass_widget:
            self.remove_widget(self.pass_widget)
        if self.error_label_exists:
            self.remove_widget(self.ids.error_label)
            self.error_label_exists = False
        url = urlparse(resurce)
        if url.hostname:
            username = url.username
            hostname = '.'.join(url.hostname.split('.')[-2:])
            resurce = username+'@'+hostname if username else hostname

        self.pass_widget = NewPasswordWidget()
        self.pass_widget.new_pass = gen_random_string(pass_phrace+resurce+'\n',14)#hashlib.sha256((pass_phrace+resurce+'\n').encode('utf-8')).hexdigest()[:14]
        self.pass_widget.resurse_str = resurce
        self.add_widget(self.pass_widget)

#    def some_function(self,text):
#        return text+'surprize'


class PassGeneratorApp(App):
    pass

if __name__ == "__main__":
#    Config.set('graphics', 'width', '400')
#    Config.set('graphics', 'height', '200')
    PassGeneratorApp().run()
