from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class TranslationCoordinate:
    x: float = 0
    y: float = 0
    z: float = 0

    @classmethod
    def from_translation_coordinate(cls, translation_coordinate: 'TranslationCoordinate'):
        return cls(translation_coordinate.x, translation_coordinate.y, translation_coordinate.z)


@dataclass(frozen=True)
class EulerAngles:
    roll: float = 0
    pitch: float = 0
    yaw: float = 0

    @classmethod
    def from_euler_angles(cls, euler_angles: 'EulerAngles'):
        return cls(euler_angles.roll, euler_angles.pitch, euler_angles.yaw)


@dataclass(frozen=True)
class ExtrinsicParams:
    translation_coordinate: TranslationCoordinate
    euler_angles: EulerAngles

    @classmethod
    def from_extrinsic_params(cls, extrinsic_params: 'ExtrinsicParams'):
        return cls(extrinsic_params.translation_coordinate, extrinsic_params.euler_angles)


@dataclass(frozen=True)
class ExtrinsicValues:
    extrinsic_params: ExtrinsicParams
    extrinsic_matrix: list = field(default_factory=list)

    @classmethod
    def from_extrinsic_values(cls, extrinsic_values: 'ExtrinsicValues'):
        return cls(extrinsic_values.extrinsic_params, extrinsic_values.extrinsic_matrix)


@dataclass(frozen=True)
class CallbacksAndTriggers:
    slider_callback: Callable
    restore_callback: Callable
    calibrate_callback: Callable
    sliders_trigger_type: str = '<B1-Motion>'
    buttons_trigger_type: str = '<ButtonRelease-1>'
