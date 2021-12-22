from common import ExtrinsicParams, CallbacksAndTriggers, ExtrinsicValues
from gui import Gui
from calculator import ExtrinsicMatrixCalculator
from extrinsic_matrix_config_handler import ExtrinsicMatrixConfigHandler
from typing import Callable


class ExtrinsicCalibrationGuiApp:
    __extrinsic_initial_values: ExtrinsicValues
    __extrinsic_current_values: ExtrinsicValues
    gui: Gui

    def __init__(self, calibration_file_path: str, operational_file_path: str):
        self.__gui = Gui()
        self.__calibration_file_path = calibration_file_path
        self.__operational_file_path = operational_file_path
        extrinsic_initial_values: ExtrinsicValues = ExtrinsicValues.from_extrinsic_values(
            ExtrinsicMatrixCalculator.calc_initial_rotations(
                ExtrinsicMatrixConfigHandler.get_config_extrinsic_matrix(
                    self.__calibration_file_path)))
        self.__extrinsic_initial_values = ExtrinsicValues.from_extrinsic_values(extrinsic_initial_values)
        self.__extrinsic_current_values = ExtrinsicValues.from_extrinsic_values(extrinsic_initial_values)
        self.__values_to_gui(self.__extrinsic_initial_values.extrinsic_params)
        self.__bind_callback_to_gui(
            CallbacksAndTriggers(self.gui_slider_callback, self.gui_restore_callback,
                                 self.gui_calibrate_callback))

    def __values_to_gui(self, gui_sliders_values: ExtrinsicParams):
        self.__gui.values_to_sliders(gui_sliders_values)

    def __bind_callback_to_gui(self, callbacks_and_triggers: CallbacksAndTriggers):
        self.__gui.bind_callbacks(callbacks_and_triggers)

    def run_gui(self):
        self.__gui.run_main_loop()

    def gui_slider_callback(self, event):
        values_from_sliders = self.__gui.values_from_sliders()
        extrinsic_matrix = ExtrinsicMatrixCalculator.calc_extrinsic_matrix(values_from_sliders)
        self.__extrinsic_current_values = ExtrinsicValues(values_from_sliders, extrinsic_matrix)
        ExtrinsicMatrixConfigHandler.set_config_extrinsic_matrix(extrinsic_matrix, self.__calibration_file_path)

    def gui_restore_callback(self, event):
        self.__values_to_gui(self.__extrinsic_initial_values.extrinsic_params)
        self.__extrinsic_current_values = ExtrinsicValues.from_extrinsic_values(
            self.__extrinsic_initial_values)
        ExtrinsicMatrixConfigHandler.set_config_extrinsic_matrix(
            self.__extrinsic_initial_values.extrinsic_matrix,
            self.__calibration_file_path)

    def gui_calibrate_callback(self, event):
        ExtrinsicMatrixConfigHandler.set_config_extrinsic_matrix(
            self.__extrinsic_current_values.extrinsic_matrix,
            self.__operational_file_path)
