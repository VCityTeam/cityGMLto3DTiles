## Pre-requisites
 - [install Python3.7](https://www.python.org/)
   - If on macos, [install from Brew](https://docs.python-guide.org/starting/install3/osx/)
 - [install docker](https://docs.docker.com/engine/install/)

## Installing dependencies

### The direnv method (recommendable)

If you are a `direnv` user and you already
[configured you shell](https://direnv.net/docs/hook.html)
then simply define a `.envrc` by using the given `.envrc.tpl` template file.
For example

```bash
$ cd `git rev-parse --show-toplevel`
$ cd cityGMLto3DTiles/PythonCallingDocker
$ ln -s .envrc.tpl .envrc
$ direnv allow
(venv)$          # You are all set
```

Note that if you wish to debug with vscode, and because vscode doesn't
recognize `.direnv` sub-directory, you will need to use a (python) virtual
environment (refer below)

### The hands on method

Create a python virtual environment and activate it

```bash
$ cd `git rev-parse --show-toplevel`
$ cd cityGMLto3DTiles/PythonCallingDocker
$ virtualenv -p python3 venv
$ . venv/bin/activate
(venv)$ pip install -r requirements.txt
```

If running on Windows replace line 4 with :
```bash
$ . venv\Script\activate
```
## Running the (static) tiler workflow

### Static case configuration step

First edit the `DemoStatic/demo_configuration_static.py` configuration file and
follow the documentation provided in that file to specify every required 
parameter.

### Note on the location of the (static) results

Be it with the single run of the full workflow or with the manual
steps (refer bellow) the resulting file hierarchies will be located
in the sub-directory configured by the `output_dir` parameter
of `demo_configuration_static.py` file (refer above) which is defaulted to
be `junk`
Within that output directory you should also find a `demo_full_workflow.log`
log file for troubleshooting.

### Running the (static) tiler full workflow

```bash
$ cd `git rev-parse --show-toplevel`
$ cd cityGMLto3DTiles/PythonCallingDocker/DemoStatic
(venv)$ python run_workflow_static.py
```

### Manual step by step run of the (static) tiler

The following manual steps should be applied in order:

```bash
$ cd `git rev-parse --show-toplevel`
$ cd cityGMLto3DTiles/PythonCallingDocker/DemoStatic
(venv)$ python run_lyon_metropole_dowload_and_sanitize_temporal.py   # result in junk/stage_1
(venv)$ python run_split_buildings_static.py                       # result in junk/stage_2
(venv)$ python run_strip_attributes_static.py                      # result in junk/stage_3 
(venv)$ python run_load_3dcitydb_static.py                         # result in junk/postgres-data-static/
(venv)$ python run_tiler_static.py
# final result in junk/stage_5/BuildingsTileset
```

## Running the temporal-tiler workflow

### Temporal case configuration step

First edit the `DemoTemporal/demo_configuration_temporal.py` configuration file.
For this follow the documentation provided for the **static** version
i.e. `DemoStatic/demo_configuration_static.py` and

### Note on the location of the (temporal) results

Be it with the single run of the full workflow or with the manual 
steps (refer bellow) the resulting file hierarchies will be located
in the `junk` sub-directory (as configured by the `output_dir` variable
of `demo_configuration.py`, refer above).
Within that output directory you should also find a `demo_full_workflow.log`
log file for troubleshooting.

### Running the temporal-tiler full workflow

```bash
$ cd `git rev-parse --show-toplevel`
$ cd cityGMLto3DTiles/PythonCallingDocker/DemoTemporal
(venv)$ python run_workflow_temporal.py 
```

### Manual step by step run of the temporal-tiler

The following manual steps should be applied in order:

```bash
$ cd `git rev-parse --show-toplevel`
$ cd cityGMLto3DTiles/PythonCallingDocker
(venv)$ python DemoTemporal/run_lyon_metropole_dowload_and_sanitize_temporal.py   # result in junk/stage_1
(venv)$ python DemoTemporal/run_split_buildings_temporal.py                       # result in junk/stage_2
(venv)$ python DemoTemporal/run_strip_attributes_temporal.py                      # result in junk/stage_3 
(venv)$ python DemoTemporal/run_demo_extract_building_dates.py                    # result in junk/stage_4
(venv)$ python DemoTemporal/run_3dcitydb_server_temporal.py                       # just a test: no output
(venv)$ python DemoTemporal/run_load_3dcitydb_temporal.py                         # result in postgres-data/ (not a junk/ subdir)
(venv)$ python DemoTemporal/run_tiler_temporal.py                                 # result in junk/stage_6
```

## Developers notes

## Running the unit tests

In order to test the containers:

```bash
$ cd `git rev-parse --show-toplevel`
$ cd cityGMLto3DTiles/PythonCallingDocker/
(venv)$ pip install pytest pytest-ordering pytest-dependency
(venv)$ pytest
```

### Debugging of a docker container notes:

Step in a container (i.e. activate a launch a shill within) with e.g.

```bash
docker run -v `pwd`/junk/LYON_1ER_2009/:/Input -v `pwd`/junk_split/:/Output -it liris:3DUse /bin/bash
```

Then at the shell prompt (i.e. the `/bin/bash` shell running within the 
container) launch e.g.

```bash
$(root) splitCityGMLBuildings --input-file /Input/LYON_1ER_BATI_2009.gml --output-file LYON_1ER_BATI_2009_splited.gml --output-dir /Output/
```

### Debugging with vscode caveat

If the application is well written (that's theory, right? :) then a script
should run independently of the Current Working Directory (cwd) from which
it was invoked. For example this way of invoking the temporal tiler

```bash
$ cd `git rev-parse --show-toplevel`
$ cd cityGMLto3DTiles/PythonCallingDocker
(venv)$ python demo_full_workflow.py
```

should be as effective as this way (mind the working directory difference)

```bash
$ cd `git rev-parse --show-toplevel`
$ cd cityGMLto3DTiles/PythonCallingDocker
(venv)$ python demo_full_workflow.py
```

(although the outputs will always be placed in the `junk` directory created in the
 CWD, which is an expected behavior).

Yet, in practice, one of the two commandes might fail (because, for example, a
subscript will look for a configuration file in the wrong directory). In order
to debug such a mistake one must configure the debugger in order to establish
the failing context: in this application case this means stating the "properly
failing" Current Working Directory.

Because when working on the (say) `PythonCallingDocker/DemoTemporal/*.py`
scripts one will also need to traverse/access some of the
`PythonCallingDocker/*.py` scripts it is more convenient to launch vscode with `PythonCallingDocker` as CWD (i.e. `${workspaceFolder} in vscode terminology).

Re-establishing the "properly failing" CWD for the python debugger as launched
by vscode can then be obtained by using the (repository provide)
[`PythonCallingDocker/.vscode/launch.json`](.vscode/launch.json) configuration
file (look for the 'cwd' entries).
