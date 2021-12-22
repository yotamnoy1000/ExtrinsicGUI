from application import ExtrinsicCalibrationGuiApp
import logging
import sys

calibration_file_path = './configs/calibration_extrinsic_matrix.json'
operational_file_path = './configs/kia_dynamic_trajectory.json'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]

)


def main():
    extrinsic_calibration_gui_app = ExtrinsicCalibrationGuiApp(calibration_file_path, operational_file_path)
    extrinsic_calibration_gui_app.run_gui()


if __name__ == '__main__':
    main()
