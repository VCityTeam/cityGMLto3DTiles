import os
import sys
import logging
import time

import demo_configuration
from docker_3dcitydb_server import Docker3DCityDBServer
from demo import Demo

class Demo3dCityDBServer(Demo):
    

    def __init__(self):
        Demo.__init__(self)
        Demo.__init_databases__(self)
        self.active_databases = list()

    def get_databases_dir(self, create=True):
        """
        The placeholder directory for database contents in order for them to persist
        as files (persistence in the container being a little trickier)
        """
        postgres_output_path = os.path.join(os.getcwd(),
                                            self.output_dir,
                                            'postgres-data')
        if create and not os.path.isdir(postgres_output_path):
            logging.info(f'Creating local output dir {postgres_output_path} in order '
                        f'to hold the various postgres databases contents.')
            os.mkdir(postgres_output_path)
        return postgres_output_path
    
    def get_vintage_database_dir(self, vintage, create=True):
        """
        :return: The placeholder directory for the database contents persisting the
        corresponding vintage data.
        """
        # The following "knowledge" is drawn both from 
        #  - the Docker3DCityDBServer() constructor that sets the container_name
        #    attribute for the considered vintage
        #  - the start_single_database() function of docker_3dcitydb_server.py
        #    that calls Docker3DCityDBServer.set_mounted_output_directory()
        data_base_container_name = 'citydb-container-' + str(self.vintage)
        vintage_path_output_dir = os.path.join(self.get_databases_dir(),
                                                data_base_container_name)

        if create and not os.path.isdir(vintage_path_output_dir):
            logging.info(f'Creating directory {vintage_path_output_dir} to '
                         f'store postgres database content for vintage {vintage}.')
            os.mkdir(vintage_path_output_dir)
        return vintage_path_output_dir

    def run(self):
        for vintage in self.vintages:
            db_config = self.databases[vintage]
        
            vintaged_db = Docker3DCityDBServer.start_single_database(vintage,
                                                                    db_config, 
                                                                    self.get_databases_dir())
            self.active_databases.append(vintaged_db)

    def halt(self):
        logging.info(f'Halting database containers: begining')
        for server in self.active_databases:
            logging.info(f'   Halting container {server.get_container().name}.')
            server.halt_service()
        logging.info(f'Halting containers: done')


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    demo_servers = Demo3dCityDBServer()
    demo_servers.run()
    logging.info('Enjoying the databases hum for 10 seconds.')
    time.sleep(10)
    demo_servers.halt()