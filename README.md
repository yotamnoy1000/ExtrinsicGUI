# Extrinsic Calibration

## Intro:

1.This application is a python script manual extrinsic matrix calibration tool.

2.The purpose of this application is to calibrate the extrinsic matrix for the cameras.

## Prerequisite python packages installation:

Install all packages used in the python application:

```sh
pip3 install -r requirements.txt
```

## calibration operation manual

1. change dynamic_trajectory.json -> calibrate_extrinsic_matrix to true.

2. run npm command for server and frontend, according to root project [README.md](../../README.md).

3. run the calibration GUI application:

```sh
cd ~/workspace/ottoplay-UI-server/scripts/extrinsic_calibration/

python extrinsic_calibration_gui.py
```

GUI application includes 6 sliders:

1. Translation:
    1. "X" - forward/backward direction.
    2. "Y" - left/right.
    3. "Z" - up/down.

2. Rotation
    1. "roll" - rotation around the "X" axis.
    2. "pitch" - rotation around the "Y" axis.
    3. "yaw" - rotation around the "Z" axis.

3. Move the sliders ,until the rectangle projected shape in laying on the road in front of the car.

4. When done click the "calibrate" button, the new extrinsic matrix will be writen to the proper configuration file.

5. To restore initial rectangle position click the "restore" button.
