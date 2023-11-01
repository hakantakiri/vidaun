import kivy
from kivy.app import App 
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

class MyGridLayout(GridLayout):

    def __init__(self, **kwargs):
        super(MyGridLayout, self).__init__(**kwargs)

        # set columns
        self.cols = 2
        
        # Add Widgets
        self.add_widget(Label(text='Url: '))
        
        ## Add input
        self.name=TextInput(multiline=False)
        self.add_widget(self.name)

        # Add submit button
        self.submit = Button(text='Download', font_size='32')
        self.submit.bind(on_press=self.press)
        self.add_widget(self.submit)

    def press(self, instance):
        url = self.name.text 
        print("Clicked to download url {}".format(url))



class MyApp(App):
    def build(self):
        return MyGridLayout()
    

if __name__ == '__main__':
    MyApp().run()