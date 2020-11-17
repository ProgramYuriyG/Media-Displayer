# package imports
import MediaDisplayer.ImageManipulations.transformations as transformations
from MediaDisplayer.ImageManipulations import histogram

# kivy imports
from kivy.atlas import CoreImage
from kivy.cache import Cache
from kivy.config import Config
from kivy.graphics.texture import Texture
from kivy import Logger
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.stacklayout import StackLayout
from plyer import filechooser

# higher order imports
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.metrics import dp
from kivy.clock import Clock

# layout imports
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, FadeTransition

# widget imports
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image, AsyncImage
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem, TabbedPanelHeader

# base imports
from PIL import Image as PILImage
from io import BytesIO
import numpy as np
import math
import io

'''
Import Commands

python -m pip install --upgrade pip wheel setuptools virtualenv
python -m virtualenv kivy_venv
kivy_venv\Scripts\activate
python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*
python -m pip install kivy_deps.gstreamer==0.1.*
python -m pip install kivy==1.11.1
python -m pip install pillow
python -m pip install opencv-python
python -m pip install numpy==1.19.3
python -m pip install -U matplotlib
pip install plyer
'''

'''
from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)
'''

# disables multitouch with right click
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# Builds the kivy gui
Builder.load_file('MediaDisplayer/gui/kv_application_files/application.kv')


class ImageTransformer:
    img_list = []

    def transformImage(self, img, text, params):
        PILimg = ''
        text = ' '.join(text.split())

        if text == 'RGB to Greyscale':
            PILimg = transformations.colortogrey(img)
        elif text == 'Negative Transformation':
            PILimg = transformations.negativetransform(img)
        elif text == 'Binary Transformation':
            PILimg = transformations.binarytransform(img, params[0])
        elif text == 'Multilevel Transformation':
            PILimg = transformations.multileveltransform(img, params[0], params[1])
        elif text == 'Log 10 Transformation':
            PILimg = transformations.logtransform(img)
        elif text == 'Gamma Transformation':
            PILimg = transformations.gammatransform(img, params[0])
        elif text == 'Histogram Equalization':
            PILimg = histogram.histogram_equalize(img)
        elif text == 'AINDANE Color Enhancement':
            PILimg = transformations.aindane(img, params[0])

        if PILimg == '':
            raise Exception('PILimg Not Populated')

        self.img_list.append(img.texture)
        PILimg.save('MediaDisplayer\\gui\\images\\temp.jpg')
        img.source = 'MediaDisplayer\\gui\\images\\temp.jpg'

        img.reload()

    def undo(self, img):
        if self.img_list:

            texture = self.img_list.pop()

            test = np.frombuffer(texture.pixels, np.uint8)
            test = test.reshape(texture.height, texture.width, 4)
            im = PILImage.fromarray(test)
            if im.mode == 'RGBA':
                im = im.convert('RGB')
            im.save('MediaDisplayer\\gui\\images\\temp.jpg')
            img.source = 'MediaDisplayer\\gui\\images\\temp.jpg'
            img.reload()

class ContainerBox(ImageTransformer, BoxLayout):
    source = ObjectProperty('MediaDisplayer/GUI/images/landscape.jpg')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def browse_files(self):
        path = filechooser.open_file(title="Pick a CSV file..",
                                     filters=[("Comma-separated Values", "*.csv")])
        self.source = path[0]

    def save_image(self):
        pass

    def restart(self, img):
        img.source = self.source
        img.reload()


class SliderButton(ImageTransformer, StackLayout):
    button_text = ObjectProperty(None)
    image_id = ObjectProperty(None)

    min_value = ObjectProperty(None)
    max_value = ObjectProperty(None)
    step_value = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FullButton(ImageTransformer, RelativeLayout):
    button_text = ObjectProperty(None)
    image_id = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LayoutContainer(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GuiApplication(App):

    def window_settings(self):
        Window.maximize()
        Window.clearcolor = (.15, .15, .15, 1)

    def build(self):
        self.window_settings()
        self.title = 'Media Displayer'
        return LayoutContainer()
