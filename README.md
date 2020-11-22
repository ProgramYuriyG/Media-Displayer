# Project Eikona

![](/images/media_displayer.png)


## Necessary Installations
Before running the application, from inside of the Windows console, make sure any necessary packages are installed by executing the commands in the following order:


- python -m pip install --upgrade pip wheel setuptools virtualenv
- python -m virtualenv kivy_venv
- kivy_venv\Scripts\activate
- python -m pip install docutils pygments pypiwin32 kivy_deps.sdl2==0.1.* kivy_deps.glew==0.1.*
- python -m pip install kivy_deps.gstreamer==0.1.*
- python -m pip install kivy==1.11.1
- python -m pip install pillow
- python -m pip install opencv-python
- python -m pip install numpy==1.19.3
- python -m pip install -U matplotlib
- pip install plyer


## How To Run
From the base directory run the following command from console:
- python -m MediaDisplayer


## Media Displayer Features
1.	Media Displayer Toolbar: 
    - Contains auxiliary features such as toggling between image and histogram display, saving and loading an image and reverting an image back to its initial, untransformed state.

2.	Display Window: 
    - Main display for the currently loaded image. Toggles between showing the image and its respective intensity histogram based on selected options

3.	Transformation Pane: 
    - Contains options for applying transformations on the currently loaded image. Certain options feature additional parameters which may be set by the user through adjusting the value of associated sliders.


## Media Displayer Toolbar:
1.	Image Display Button: Toggles off the histogram display if shown and displays the currently loaded image.

2.	Histogram Display Button: Shows the currently loaded image’s histogram as an overlay to the user. 

NOTE: The user may freely use the transform features, undo changes, save and load a new image and the histogram will update accordingly to reflect the new changes.

3.	Load Button: Loads a new image to the display window

NOTE: Loading in a new image will clear old transformations from memory. The user will have to load the old image back in if they wish to use it for further transformations or save the image before loading something else.

4.	Save Button: Save the current image to a targeted location. If the user does not specify the extension type in the image name, the image is saved as a .png by default.

5.	Reload Button: Revert the image back to its initial state prior to any transformations being applied

NOTE: Reloading the image will clear old transformations from memory, similarly to loading a new image


## Transformation Features
1.	Undo Button: 
    - Reloads the last state of the image prior to the current transformation.

2.	RGB to Greyscale Button: 
    - Converts a color image to its greyscale equivalent using a weighted method on each channel.

3.	Negative Transformation Button: 
    - Inverts all the intensities of the image by subtracting each pixel value from the highest allowable level.

4.	Binary Transformation Button: 
    - Applies a binary transformation to the image where each pixel level is set to 0 or max depending on what side of the threshold its on. The user may adjust the threshold via the slider to the right. Allowable levels range from 0-255.

5.	Multilevel Transformation Button: 
    - Applies a multilevel transformation to the image where pixel intensities that fall outside of the interval [t1, t2] are set to 0. Both intensities may be set in the range 0-255 via the sliders to the right.

6.	Log 10 Transformation Button: 
    - Applies a logarithmic transformation to the image, expanding dark intensities and compressing lighter ones

7.	Gamma Transformation Button: 
    - Applies a gamma transformation to the image, where the strength of the gamma curve depends on the value of gamma provided to the function. User may provide values for gamma in the range 0-25 in 0.1 intervals via the slider to the right.

8.	Histogram Equalization Button: 
    - Applies histogram equalization to the image, spreading out the intensity values over the full distribution range.

9.	AINDANE Color Enhancement Button: 
    - Enhances the color of the image using the AINDANE enhancement technique. Strength of the color hue depends on a parameter lambda provided to the function. User may provide values for lambda in the range 0.75-0.99 in 0.01 intervals via the slider to the right.

NOTE: Each transformation requires the application to be in focus and may take a bit of time before the output image is displayed. If the changes are not immediate, do not click the buttons multiple times.






