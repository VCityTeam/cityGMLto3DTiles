import os
import sys
import demo_workflow_static as workflow

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from run import run_demo_tiler


if __name__ == '__main__':
    run_demo_tiler(workflow.demo_tiler, workflow.demo_db_server)
