import os
import sys
import logging
import demo_configuration
from abc import ABC, abstractmethod


class Demo(ABC):
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the various derived demonstration classes in order to designate
    their respective input/output directories and filenames
    """
    def __init__(self,
                 results_dir = None,
                 all_demos_output_dir =demo_configuration.output_dir,
                 city=demo_configuration.city,
                 vintages=demo_configuration.vintages,
                 boroughs=demo_configuration.boroughs):

        # The all_demos_output_dir directory is the directory within which all the 
        # demos (i.e. demonstatrion classes inheriting from this Demo class) will 
        # place their outputs. Note that the actual outputs of a particular demo
        # can be in a sub-directory of all_demos_output_dir (refer to Demo.get_output_dir() 
        # method)
        # FIXME: this should be a class variable
        self.all_demos_output_dir = all_demos_output_dir
        # When self.results_dir is set this Demo will outputs/results will be located in 
        # the "results_dir" sub-directory of self.all_demos_output_dir (refer to 
        # Demo.get_ouput_dir() method).
        self.results_dir = results_dir
        self.city = city
        self.vintages = vintages
        self.boroughs = boroughs
        self.input_demo = None

    def __init_databases__(self):
        if not demo_configuration.databases:
            logging.info(f'Databases configurations not found. Exiting')
            sys.exit(1)
        
        self.databases = demo_configuration.databases
        
        for vintage in self.vintages:
            if not self.databases[vintage]:
                logging.info(f'Database configuration for vintage {vintage} was not '
                            f'found. You must specify one database configuration '
                            f'per vintage. Exiting')
                sys.exit(1)

    def set_results_dir(self, results_dir):
        self.results_dir = results_dir

    def get_output_dir(self, create=False):
        output_dir = self.all_demos_output_dir
        if self.results_dir:
            output_dir = os.path.join(self.all_demos_output_dir, self.results_dir)
        if create and not os.path.isdir(output_dir):
            logging.info(f'Creating demo output directory {output_dir}.')
            os.mkdir(output_dir)
        return output_dir

    def set_input_demo(self, input_demo):
        """
        The Demo that stands upstream in the workflow and that this Demo
        will get its input from.
        """
        self.input_demo = input_demo

    def get_input_demo(self):
        if not self.input_demo:
            logging.error(f'Input demo was not set: exiting.')
            return sys.exit(1)
        return self.input_demo

    @abstractmethod
    def get_vintage_borough_output_file_basename(self, vintage, borough):
        raise NotImplementedError()

    def get_vintage_borough_output_directory_name(self, vintage, borough):
        return os.path.join(self.get_output_dir(), borough + '_' + str(vintage))

    def get_vintage_borough_output_filename(self, vintage, borough):
        """
        :return: the filename for the given vintage and borough as layed out after the 
                 download and patch. This function result DOES include the directory 
                 name in which the output file lies.
        """
        return os.path.join(self.get_vintage_borough_output_directory_name(vintage, borough),
                            self.get_vintage_borough_output_file_basename(vintage, borough))

    @abstractmethod
    def get_resulting_filenames(self):
        raise NotImplementedError()

    def assert_output_files_exist(self):
        """
        :return: True when all the strip produced files exist in the default
                 place (i.e. when an alternate output_dir was not specified)
                 False otherwise.
        """
        for filename in self.get_resulting_filenames():
            if not os.path.isfile(filename):
                logging.error(f'Output file {filename} not found.')
                return False
        return True