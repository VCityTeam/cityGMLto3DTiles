# This is an example of configuration file that must be customized to
# suit your specific needs.

# The output directory where all the results of the computational pipeline
# will be placed.
output_dir = 'junk'

# The considered vintage year among the Lyon Open data available ones
vintage = 2015

# The name to be given to the resulting aggregation of boroughs. Note that
# the name of this parameter is misleading and was historically chosen to
# be city because if the considered set of boroughs are the ones of Lyon,
# then it seems "natural" to call the aggregate by the name of the city.
# But when considering all the boroughs of the "Chemistry valley", then
# the resulting name would not be a name of a city (but of a commonly shared
# nickname like ChemistryValley).
city = 'LYON'

# The list of boroughs that should be extracted
boroughs = [
           'LYON_1ER',
           'LYON_2EME',
           'LYON_3EME',
           'LYON_4EME',
           'LYON_5EME',
           'LYON_6EME',
           'LYON_7EME',
           'LYON_8EME',
           'LYON_9EME',
           'FEYZIN',
           'GIVORS',
           'GRIGNY',
           'IRIGNY',
           'PIERRE_BENITE',
           'SOLAIZE',
           'SAINT_FONS',
           'LYON_7EME',
           'VERNAISON'
]

# At some stage the computational pipeline will make use of a 3DCityDB database.
# Except for PG_HOST, the following parameters are the "credentials" that will be
# used both for
#  * setting up the docker containerized database after its creation 
#  * the "client containers" to access it.
#
# PG_HOST should be IP number of host machine on which the pipeline gets 
# executed.
# Note: in order to configure `PG_HOST` you might use (on a linux machine) the 
#       `hostname -I` command.
# FIXME: why use an IP number in place of a symbolic name like localhost ?
database = {
  'PG_HOST': '192.168.1.14',
  'PG_PORT': '5435',
  'PG_NAME': 'citydb-lyon-chemistry-valley-2015-for_static',
  'PG_USER': 'postgres',
  'PG_PASSWORD': 'postgres'
}
