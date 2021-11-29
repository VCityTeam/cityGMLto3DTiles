## Pre-requisites
 - [install Python3.7](https://www.python.org/)

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

## Alive issues

### Bug

When the configuration file specifies an `output_dir` directory that is
an absolute path e.g.

- on a different partition (forcing the usage of a path starting
  at the root i.e. whose pathname starts with `/`)
- in a parent directory (yet specified in an absolut manner) then the command

  ```bash
  python run_demo_extract_building_dates.py
  ```
  
  fails with a message of the container of the form
  
  ```bash
  docker-stdout> b'Creating output directory /Input//Data/junk/stage_4/2009_2012_Differences/LYON_1ER_2009_2012
  terminate called after throwing an instance of \'boost::filesystem::filesystem_error\'
  what():  boost::filesystem::create_directory: No such file or directory:
  "/Input//Data/junk/stage_4/2009_2012_Differences/LYON_1ER_2009_2012"
  ```

Surprisingly enough, and once the process crashed, one can check that
this directory does indeed exist.

Note that in the context, previous stages that use docker containers (e.g. split
and/or strip) and that need to mount `/Data/` under `/Input` still run smoothly.

Suggestions:

- check whether the split and strip algorithms also use a call to
  boost::filesystem::create_directory. If they do then check the
  calling context at the Python level. If they don't you get some
  clue...
- Check whether the double slash (`/Input//Data/`) could be the
  source of the  issue.

### Bug: DemoLoad3DCityDB misplaces its output

demo_load places its output in `<output_dir>/postgres-data` directory instead of
`<output_dir>/stage_5/postgres-data`.

### Bug: extractBuildingDates stage fails on Villeurbanne data

The following run fails

```bash
docker run -v `pwd`:/Input --workdir /root/3DUSE/Build/src/utils/cmdline/ -t liris:3DUse extractBuildingDates --first_date 2009 --first_file /Input/junk/VILLEURBANNE_2009/VILLEURBANNE_BATI_2009.gml --second_date 2012 --second_file /Input/junk/VILLEURBANNE_2012/VILLEURBANNE_BATI_2012.gml --output_dir /Input/junk/2009_2012_Differences/VILLEURBANNE_2009-2012/
```

with the message:

```bash
CityGML first file loaded :/Input/junk/VILLEURBANNE_2009/VILLEURBANNE_BATI_2009.gml
CityGML second file loaded :/Input/junk/VILLEURBANNE_2012/VILLEURBANNE_BATI_2012.gml
Model 1: 
    Converting building: 455/455 
Done.
Model 2: 
    Converting building: 447/447 
Done.
Internal buildings pre-processing...
ERROR 1: TopologyException: found non-noded intersection between LINESTRING (1.8489e+06 5.17487e+06, 1.84892e+06 5.17488e+06) and LINESTRING (1.84891e+06 5.17488e+06, 1.84892e+06 5.17488e+06) at 1848907.2497562491 5174876.2345244605 191.31213515757889
```

This error seems related with postgis or gdal according to threads like:
- [R wrapping of gdal](https://stackoverflow.com/questions/13662448/what-does-the-following-error-mean-topologyexception-found-non-nonded-intersec)
- [r-spatial/sf issue](https://github.com/r-spatial/sf/issues/860)

### Running the workflow on Ubuntu with sudo docker 

<a name="UbuntuWithSudo"></a>

On an **Ubuntu platform** the default configuration of docker requires
any user to `sudo` (try running the `docker ps` command and refer to this
[Aks Ubuntu question](https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo)).
Because the workflow uses docker under the hood, running it, or running any
of its steps, also requires a common user to use the sudo command.
Yet when running a workflow step (refer above) with sudo

```bash
(venv)$ sudo python run_strip_attributes_static.py
```

one gets the following error message

```bash
Traceback (most recent call last):
  File "run_strip_attributes_static.py", line 3, in <module>
    import demo_workflow_static as workflow
  File "/home/vcity/Desktop/DemoValleeChimie/UD-Reproducibility/Computations/3DTiles/LyonTemporal/PythonCallingDocker/DemoStatic/demo_workflow_static.py", line 6, in <module>
    from demo_lyon_metropole_dowload_and_sanitize_static \
  File "/home/vcity/Desktop/DemoValleeChimie/UD-Reproducibility/Computations/3DTiles/LyonTemporal/PythonCallingDocker/DemoStatic/demo_lyon_metropole_dowload_and_sanitize_static.py", line 4, in <module>
    from demo_static import DemoStatic, DemoWithFileOutputStatic
  File "/home/vcity/Desktop/DemoValleeChimie/UD-Reproducibility/Computations/3DTiles/LyonTemporal/PythonCallingDocker/DemoStatic/demo_static.py", line 48
    logging.info(f'Database configuration not found. Exiting')
```

that after some inquiry is due to the fact that the **python command that gets
used when running in sudo mode is NOT the python of the virtual environment**
(you can assert this by running `sudo which python3` that does NOT return
the path to `venv/bin/python3`).

In this Ubuntu context where `sudoing` is required for using docker, you thus
need to workaround the sudo `PATH` shell environment to explicitly state that
it is the virtual environment version of python that must be used.
The command is thus

```bash
sudo venv/bin/python3 run_strip_attributes_static.py
```

### Working around Ubuntu docker access without sudo

On an **Ubuntu platform** the running of the workflow, or any of its steps, 
fails due to docker access rights limitations. For example when running 
(refer above)

```bash
python run_strip_attributes_static.py
```

one gets the following error message

```bash
File "<some-path>/venv/lib/python3.8/site-packages/urllib3/connectionpool.py", line 699, in urlopen
    httplib_response = self._make_request(
  File "<some-path>/venv/lib/python3.8/site-packages/urllib3/connectionpool.py", line 394, in _make_request
    conn.request(method, url, **httplib_request_kw)
[...]
    sock.connect(self.unix_socket)
PermissionError: [Errno 13] Permission denied
[...]
    raise DockerException(
docker.errors.DockerException: Error while fetching server API version: ('Connection aborted.', PermissionError(13, 'Permission denied'))
```

indicating that you cannot access/connect the Docker daemon because of
insufficient permissions (access rights).
You can asses this is the right diagnostic, by running

```bash
$ docker version
```

that should yield something similar to

```bash
[...]
Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get http://%2Fvar%2Frun%2Fdocker.sock/v1.24/version: dial unix /var/run/docker.sock: connect: permission denied
```

A straightforward workaround, that we do NOT recommend, would be to pre-prend 
the running script command with a `sudo` i.e. to use 

```bash
sudo python3 run_strip_attributes_static.py
```

Yet this cannot be recommend for two reasons

- using `sudo python3 ...` does 
  [NOT use the python interpreter that you would would think of](#UbuntuWithSudo)

- some portions of the resulting data directory will belong to root, and
  accessing them or deleting will also require you to used `sudo`

Instead what we advise is to configure your Ubuntu to allow for `docker` usage
without having to `sudo`, [that boils down to](https://askubuntu.com/questions/477551/how-can-i-use-docker-without-sudo) e.g.

```bash
$ sudo groupadd docker 
$ sudo gpasswd -a $USER docker
$ newgrp docker
```

### Concerning the "slow starting postgresql startup"

Refer to the [Debug_notes-Connection_refused.md](Debug_notes-Connection_refused.md).
