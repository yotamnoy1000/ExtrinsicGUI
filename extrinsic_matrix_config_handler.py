import json
import logging


class ExtrinsicMatrixConfigHandler:
    @classmethod
    def get_config_extrinsic_matrix(cls, file_path, json_field_name: str = 'extrinsic_matrix') -> list:
        with open(file_path, 'r') as json_file:
            trajectory_data: dict = json.load(json_file)
        extrinsic_matrix: list = trajectory_data[json_field_name]
        cls.__initial_extrinsic_matrix = extrinsic_matrix
        return extrinsic_matrix

    @classmethod
    def set_config_extrinsic_matrix(cls, extrinsic_matrix: list, file_path: str,
                                    json_field_name: str = 'extrinsic_matrix'):
        cls.__final_extrinsic_matrix = extrinsic_matrix
        logging.debug('set_config_extrinsic_matrix')
        logging.debug(f'extrinsic_matrix = {extrinsic_matrix}')
        with open(file_path, 'r') as jsonFile:
            trajectory_data: dict = json.load(jsonFile)
        trajectory_data[json_field_name] = extrinsic_matrix

        with open(file_path, 'w') as jsonFile:
            jsonFile.write(json.dumps(trajectory_data, indent=4) + '\n')
