from tkinter import *
from PIL import Image, ImageTk
from dataclasses import dataclass
from common import ExtrinsicParams, CallbacksAndTriggers, TranslationCoordinate, EulerAngles
from typing import Callable


@dataclass
class GuiLabels:
    translation_label: Label
    x_slider_label: Label
    y_slider_label: Label
    z_slider_label: Label
    euler_angles_label: Label
    roll_slider_label: Label
    pitch_slider_label: Label
    yaw_slider_label: Label


@dataclass
class GuiFrames:
    x_frame: Frame
    y_frame: Frame
    z_frame: Frame
    roll_frame: Frame
    pitch_frame: Frame
    yaw_frame: Frame

    @classmethod
    def overload_constractor(cls, frame_func: Callable):
        return cls(frame_func(), frame_func(), frame_func(), frame_func(), frame_func(), frame_func())


@dataclass
class GuiImage:
    axis_photo_img: PhotoImage
    axis_image_label: Label


@dataclass
class GuiSliders:
    x: Scale
    y: Scale
    z: Scale
    roll: Scale
    pitch: Scale
    yaw: Scale


@dataclass
class GuiButtons:
    calibrate_button: Button
    restore_button: Button


class Gui:
    __root_window: Tk
    __gui_frames: GuiFrames
    __gui_labels: GuiLabels
    __gui_sliders: GuiSliders
    __gui_buttons: GuiButtons
    __gui_image: GuiImage

    def __init__(self):
        self.__create_window()
        self.__create_frames()
        self.__create_labels()
        self.__create_sliders()
        self.__create_buttons()
        self.__create_images()

    def __create_window(self):
        self.__root_window = Tk()
        self.__root_window.title('Extrinsic calibration GUI')
        self.__root_window.geometry('1000x1050')

    def __create_frames(self):
        frame_settings: Callable = lambda: Frame(self.__root_window, borderwidth='2', relief='groove')
        gui_frames: GuiFrames = GuiFrames.overload_constractor(
            frame_settings)
        self.__gui_frames = gui_frames

    def __create_labels(self):
        gui_labels: GuiLabels = GuiLabels(
            Label(self.__root_window, text='Translation Parameters', font=18),
            Label(self.__gui_frames.x_frame, text='X'),
            Label(self.__gui_frames.y_frame, text='Y'),
            Label(self.__gui_frames.z_frame, text='Z'),
            Label(self.__root_window, text='Euler Angles', font=18),
            Label(self.__gui_frames.roll_frame, text='Roll'),
            Label(self.__gui_frames.pitch_frame, text='Pitch'),
            Label(self.__gui_frames.yaw_frame, text='Yaw'),
        )
        self.__gui_labels = gui_labels

    def __create_images(self, image_path='resources/Roll-Pitch-Yaw.jpg'):
        axis_image = Image.open(image_path)
        axis_image = axis_image.resize((400, 400), Image.ANTIALIAS)
        axis_photo_img = ImageTk.PhotoImage(axis_image)
        axis_image_label = Label(self.__root_window, image=axis_photo_img)
        self.__gui_image = GuiImage(axis_photo_img, axis_image_label)

    def __create_sliders(self):
        coordinate_max_value: int = 1
        angles_max_value: int = 180
        angles_resolution: float = 0.1
        cartesian_resolution: float = 0.001
        sliders_settings: Callable = lambda frame, from_, to, resolution: Scale(frame,
                                                                                from_=from_, to=to,
                                                                                orient=HORIZONTAL,
                                                                                length=400,
                                                                                width=30,
                                                                                resolution=resolution)
        gui_sliders: GuiSliders = GuiSliders(
            sliders_settings(self.__gui_frames.x_frame, -coordinate_max_value, coordinate_max_value,
                             cartesian_resolution),
            sliders_settings(self.__gui_frames.y_frame, -coordinate_max_value, coordinate_max_value,
                             cartesian_resolution),
            sliders_settings(self.__gui_frames.z_frame, -coordinate_max_value, coordinate_max_value,
                             cartesian_resolution),
            sliders_settings(self.__gui_frames.roll_frame, -angles_max_value, angles_max_value, angles_resolution),
            sliders_settings(self.__gui_frames.pitch_frame, -angles_max_value, angles_max_value,
                             angles_resolution),
            sliders_settings(self.__gui_frames.yaw_frame, -angles_max_value, angles_max_value, angles_resolution),
        )
        self.__gui_sliders = gui_sliders

    def __create_buttons(self):
        gui_buttons: GuiButtons = GuiButtons(
            Button(self.__root_window, text='Calibrate !', bd='5'),
            Button(self.__root_window, text='Restore !', bd='5')
        )
        self.__gui_buttons = gui_buttons

    def __pack_gui_elements(self):
        gui_elements: dict = {
            'translation':
                [self.__gui_labels.translation_label,
                 self.__gui_frames.x_frame,
                 self.__gui_sliders.x,
                 self.__gui_labels.x_slider_label,
                 self.__gui_frames.y_frame,
                 self.__gui_sliders.y,
                 self.__gui_labels.y_slider_label,
                 self.__gui_frames.z_frame,
                 self.__gui_sliders.z,
                 self.__gui_labels.z_slider_label],
            'Euler':
                [self.__gui_labels.translation_label,
                 self.__gui_frames.roll_frame,
                 self.__gui_sliders.roll,
                 self.__gui_labels.roll_slider_label,
                 self.__gui_frames.pitch_frame,
                 self.__gui_sliders.pitch,
                 self.__gui_labels.pitch_slider_label,
                 self.__gui_frames.yaw_frame,
                 self.__gui_sliders.yaw,
                 self.__gui_labels.yaw_slider_label],
            'button':
                [self.__gui_buttons.restore_button,
                 self.__gui_buttons.calibrate_button],
            'image':
                [self.__gui_image.axis_image_label]
        }

        for key, values in gui_elements.items():
            if isinstance(values, list):
                for value in values:
                    value.pack()

    def run_main_loop(self):
        self.__pack_gui_elements()
        self.__root_window.mainloop()

    def values_to_sliders(self, gui_sliders_values: ExtrinsicParams):
        slider_index = 0
        slider_value_index = 1
        sliders_values = [(self.__gui_sliders.x, gui_sliders_values.translation_coordinate.x),
                          (self.__gui_sliders.y, gui_sliders_values.translation_coordinate.y),
                          (self.__gui_sliders.z, gui_sliders_values.translation_coordinate.z),
                          (self.__gui_sliders.roll, gui_sliders_values.euler_angles.roll),
                          (self.__gui_sliders.pitch, gui_sliders_values.euler_angles.pitch),
                          (self.__gui_sliders.yaw, gui_sliders_values.euler_angles.yaw)]

        for slider in sliders_values:
            slider[slider_index].set(slider[slider_value_index])

    def bind_callbacks(self, callbacks_and_triggers: CallbacksAndTriggers):
        callbacks: dict = {'sliders': callbacks_and_triggers.slider_callback,
                           'calibrate': callbacks_and_triggers.calibrate_callback,
                           'restore': callbacks_and_triggers.restore_callback}

        triggers = {'sliders': callbacks_and_triggers.sliders_trigger_type,
                    'buttons': callbacks_and_triggers.buttons_trigger_type}

        buttons: dict = {'restore': self.__gui_buttons.restore_button,
                         'calibrate': self.__gui_buttons.calibrate_button}
        sliders: list = [self.__gui_sliders.x, self.__gui_sliders.y, self.__gui_sliders.z,
                         self.__gui_sliders.roll, self.__gui_sliders.pitch, self.__gui_sliders.yaw]

        buttons['restore'].bind(triggers['buttons'], callbacks['restore'])
        buttons['calibrate'].bind(triggers['buttons'], callbacks['calibrate'])

        for slider in sliders:
            slider.bind(triggers['sliders'], callbacks['sliders'])

    def values_from_sliders(self) -> ExtrinsicParams:
        gui_sliders_values: ExtrinsicParams = ExtrinsicParams(
            TranslationCoordinate(
                self.__gui_sliders.x.get(),
                self.__gui_sliders.y.get(),
                self.__gui_sliders.z.get()),
            EulerAngles(
                self.__gui_sliders.roll.get(),
                self.__gui_sliders.pitch.get(),
                self.__gui_sliders.yaw.get())
        )
        return gui_sliders_values
