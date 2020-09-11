import os
import sys
import logging
from docker_py3dtiles import DockerPy3dtiles


class DockerTemporalTiler(DockerPy3dtiles):
    def __init__(self):
        super().__init__()
        self.vintages = list()
        self.db_config_filenames = list()

    def assert_ready_for_run(self):
        if not self.vintages:
            logging.info('Missing vintages for running. Please specify at '
                         'least two vintages.')
            sys.exit(1)
        if not self.db_config_filenames:
            logging.info('Missing database configuration files for running. '
                         'Please set up at least two of them.')
            sys.exit(1)
        if len(self.db_config_filenames) != len(self.vintages):
            logging.info('Please specify as many database configuration '
                         'files as vintages.')
            sys.exit(1)

    def set_vintages(self, vintages):
        if not isinstance(vintages, list):
            logging.info('set_vintages() waits for a list of vintages.')
            sys.exit(1)
        if len(vintages) < 2:
            logging.info('You must provide at list two vintages.')
            sys.exit(1)
        self.vintages = vintages

    def add_vintage(self, vintage):
        self.vintages.append(vintage)

    def set_db_config_filenames(self, db_config_files):
        if not isinstance(db_config_files, list):
            logging.info('set_db_config_files() waits for a list of vintages.')
            sys.exit(1)
        if len(db_config_files) < 2:
            logging.info('You must provide at list two database configuration '
                         'files.')
            sys.exit(1)
        self.db_config_filenames = db_config_files

    def add_db_config_file(self, db_config_file):
        if not os.path.isfile(db_config_file):
            logging.info(f'Database configuration file'
                         f' {db_config_file} not found. Exiting')
            sys.exit(1)
        self.db_config_filenames.append(db_config_file)

    def get_command(self):
        self.assert_ready_for_run()
        # The Tiler to run, see ../Docker/CityTiler-DockerContext/entrypoint.py
        command = 'TemporalTiler '
        command += '--db_config_path '
        for db_config in self.db_config_filenames:
            command += '/Input/' + db_config + ' '
        command += '--time_stamp '
        for vintage in self.vintages:
            command += str(vintage) + ' '
        return command

    def generate_configuration_file(self, vintage, db_config, output_file_basename):
        """
        The Tiler requires a configuration file describing the database
        access it will use. This file has an ad-hoc xml format that this
        method generates out .  
        """
        target_file = os.path.join(self.get_mounted_input_directory(),
                                   output_file_basename)
        with open(target_file, 'w') as output:
            output.write(f'PG_HOST: {db_config["PG_HOST"]}\n')
            output.write(f'PG_PORT: {db_config["PG_PORT"]}\n')
            output.write(f'PG_NAME: {db_config["PG_NAME"]}\n')
            output.write(f'PG_USER: {db_config["PG_USER"]}\n')
            output.write(f'PG_PASSWORD: {db_config["PG_PASSWORD"]}\n')
            output.write(f'PG_VINTAGE: {vintage}\n')
