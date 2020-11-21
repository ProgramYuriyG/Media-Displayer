# package imports
import os

import MediaDisplayer.ImageManipulations.transformations as transformations
from MediaDisplayer.ImageManipulations import histogram

# kivy imports
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.uix.stacklayout import StackLayout
from plyer import filechooser

# higher order imports
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window

# layout imports
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout

# widget imports
from kivy.core.image import Image

# base imports
from PIL import Image as PILImage
import numpy as np

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
    img_list = ObjectProperty([])

    def transformImage(self, img, text, params, is_histogram, histogram_img):
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
        PILimg.save(os.path.join(os.path.dirname(__file__), 'images\\temp.png'))
        img.source = os.path.join(os.path.dirname(__file__), 'images\\temp.png')
        img.reload()

        if is_histogram:
            plt = histogram.display_histogram(img)
            plt.savefig(os.path.join(os.path.dirname(__file__), 'images\\histogram.png'))
            plt.clf()
            histogram_img.reload()

    def undo(self, img, is_histogram, histogram_img):
        if self.img_list:

            texture = self.img_list.pop()

            test = np.frombuffer(texture.pixels, np.uint8)
            test = test.reshape(texture.height, texture.width, 4)
            im = PILImage.fromarray(test)
            if im.mode == 'RGBA':
                im = im.convert('RGB')
            im.save(os.path.join(os.path.dirname(__file__), 'images\\temp.png'))
            img.source = os.path.join(os.path.dirname(__file__), 'images\\temp.png')
            img.reload()

            if is_histogram:
                plt = histogram.display_histogram(img)
                plt.savefig(os.path.join(os.path.dirname(__file__), 'images\\histogram.png'))
                plt.clf()
                histogram_img.reload()


class ContainerBox(ImageTransformer, BoxLayout):
    source = ObjectProperty(os.path.join(os.path.dirname(__file__), 'images\\landscape.jpg'))
    histogram_source = ObjectProperty(os.path.join(os.path.dirname(__file__), 'images\\histogram.png'))
    is_histogram = ObjectProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def display_histogram(self, img, hist_image):
        self.is_histogram = True
        plt = histogram.display_histogram(img)
        plt.savefig(os.path.join(os.path.dirname(__file__), 'images\\histogram.png'))
        plt.clf()
        hist_image.reload()

    def display_image(self):
        self.is_histogram = False

    def browse_files(self, img):
        self.img_list.append(img.texture)
        path = filechooser.open_file(title="Pick an Image file..",
                                     filters=["*.jpg", "*.jpeg", "*.png"])
        if not path:
            return
        PILImage.open(path[0]).save(os.path.join(os.path.dirname(__file__), 'images\\temp.png'))
        self.source = os.path.join(os.path.dirname(__file__), 'images\\temp.png')
        img.reload()
        self.img_list = []

    def save_image(self, img):
        path = filechooser.save_file(title="Save File As")
        org_source = os.path.basename(img.source)
        if not path:
            return
        if not path[0].lower().endswith((".jpg", ".jpeg", ".png")):
            path[0] += ".png"
        Image(img.texture).save(path[0])

        self.source = os.path.join(os.path.dirname(__file__), 'images\\', org_source)
        img.reload()

    def restart(self, img, hist_image):
        if len(self.img_list) > 0:
            texture = self.img_list[0]

            test = np.frombuffer(texture.pixels, np.uint8)
            test = test.reshape(texture.height, texture.width, 4)
            im = PILImage.fromarray(test)
            if im.mode == 'RGBA':
                im = im.convert('RGB')
            im.save(os.path.join(os.path.dirname(__file__), 'images\\temp.png'))
            img.source = os.path.join(os.path.dirname(__file__), 'images\\temp.png')
            img.reload()
            self.img_list = []

            if self.is_histogram:
                plt = histogram.display_histogram(img)
                plt.savefig(os.path.join(os.path.dirname(__file__), 'images\\histogram.png'))
                plt.clf()
                hist_image.reload()


class SliderButton(StackLayout):
    button_text = ObjectProperty(None)
    image_id = ObjectProperty(None)

    min_value = ObjectProperty(None)
    max_value = ObjectProperty(None)
    step_value = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FullButton(RelativeLayout):
    button_text = ObjectProperty(None)
    image_id = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GuiApplication(App):

    def window_settings(self):
        Window.maximize()
        Window.clearcolor = (.15, .15, .15, 1)

    def build(self):
        self.window_settings()
        self.title = 'Media Displayer'
        return ContainerBox()
