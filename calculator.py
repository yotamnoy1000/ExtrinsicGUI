import numpy as np
import transforms3d.euler as euler
from common import ExtrinsicValues, ExtrinsicParams, TranslationCoordinate, EulerAngles
import logging


class ExtrinsicMatrixCalculator:
    Mat_max_index: int = 3

    @classmethod
    def calc_initial_rotations(cls, extrinsic_matrix: list) -> ExtrinsicValues:
        logging.debug(f'extrinsic_matrix = {extrinsic_matrix}')
        # extracting R(3x3) rotation matrix from 3x4 extrinsic matrix, extrinsic_matrix = R(3x3)|T(3X1)
        rotation_matrix: np.array = np.array([x[:cls.Mat_max_index] for x in extrinsic_matrix[:cls.Mat_max_index]])
        logging.debug(f'rotation_matrix = {rotation_matrix}')
        # extracting T(3X1) translation vector from 3x4 extrinsic matrix, extrinsic_matrix = R(3x3)|T(3X1)
        translation_vector = (np.array(extrinsic_matrix)[:, [cls.Mat_max_index]][:cls.Mat_max_index]).tolist()
        x, y, z = [a for a in translation_vector]
        logging.debug(f'euler_angles x = {x} y ={y} z ={z}')
        roll, pitch, yaw = euler.mat2euler(rotation_matrix, axes='sxzy')
        logging.debug(f'euler_angles roll = {roll} pitch = {pitch}, yaw = {yaw}')
        extrinsic_params: ExtrinsicParams = ExtrinsicParams(TranslationCoordinate(z, x, y),
                                                            EulerAngles(np.rad2deg(roll), np.rad2deg(pitch),
                                                                        np.rad2deg(yaw)))
        return ExtrinsicValues(
            extrinsic_params,
            extrinsic_matrix
        )

    @classmethod
    def calc_extrinsic_matrix(cls, extrinsic_params: ExtrinsicParams) -> list:
        logging.debug(
            f'euler_angles roll = {extrinsic_params.euler_angles.roll} pitch = {extrinsic_params.euler_angles.pitch} z = {extrinsic_params.euler_angles.yaw}')
        rotation_matrix = euler.euler2mat(np.deg2rad(extrinsic_params.euler_angles.roll),
                                          np.deg2rad(extrinsic_params.euler_angles.pitch),
                                          np.deg2rad(extrinsic_params.euler_angles.yaw), axes='sxzy')
        translation_vector: list = [extrinsic_params.translation_coordinate.y,
                                    extrinsic_params.translation_coordinate.z,
                                    extrinsic_params.translation_coordinate.x]
        return cls.__calc_extrinsic_matrix(rotation_matrix, translation_vector)

    @classmethod
    def __calc_extrinsic_matrix(cls, rotation_matrix: np.ndarray, translation_vector: list) -> list:
        identity_4th_row: [] = [0, 0, 0, 1]
        extrinsic_matrix_extended: np.ndarray = np.vstack(
            (np.hstack((rotation_matrix, np.array(translation_vector)[:, None])), identity_4th_row))
        extrinsic_matrix: list = np.around(extrinsic_matrix_extended[:cls.Mat_max_index], cls.Mat_max_index).tolist()
        return extrinsic_matrix
