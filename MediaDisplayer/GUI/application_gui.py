# package imports
import MediaDisplayer.ImageManipulations.transformations as transformations
from MediaDisplayer.ImageManipulations import histogram

# kivy imports
from kivy.uix.stacklayout import StackLayout
from kivy.properties import ObjectProperty
from plyer import filechooser
from kivy.config import Config

# higher order imports
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.app import App

# layout imports
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout

# widget imports
from kivy.core.image import Image

# base imports
from PIL import Image as PILImage
import numpy as np
import os


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
Builder.load_file('MediaDisplayer/GUI/kv_application_files/application.kv')


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
        fp = os.path.join(os.path.dirname(__file__), 'images\\temp.png')
        PILimg.save(fp)
        img.source = fp

        img.reload()

    def undo(self, img):
        if self.img_list:
            print('uhm')

            texture = self.img_list.pop()

            test = np.frombuffer(texture.pixels, np.uint8)
            test = test.reshape(texture.height, texture.width, 4)
            im = PILImage.fromarray(test)
            if im.mode == 'RGBA':
                im = im.convert('RGB')
            fp = os.path.join(os.path.dirname(__file__), 'images\\temp.png')
            im.save(fp)
            img.source = fp
            img.reload()

class ContainerBox(ImageTransformer, BoxLayout):
    source = ObjectProperty('MediaDisplayer/GUI/images/landscape.jpg')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def browse_files(self, img):
        temp_location = os.path.join(os.path.dirname(__file__), 'images\\temp.png')
        path = filechooser.open_file(title="Pick an Image file..",
                                     filters=["*.jpg", "*.png", "*.svg"])
        if not path:
            return
        self.source = path[0]

        pil_img = PILImage.open(path[0])
        pil_img.save(temp_location)
        img.source = temp_location
        img.reload()
        img.img_list = []

    def save_image(self):
        temp_location = os.path.join(os.path.dirname(__file__), 'images\\temp.png')
        path = filechooser.save_file(title="Save Your Image..",
                                     filters=["*.png"])
        if not path:
            return

        pil_img = PILImage.open(temp_location)
        pil_img.save('{}.png'.format(path[0]))

    def restart(self, img):
        img.source = self.source
        img.reload()
        img.img_list = []


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
