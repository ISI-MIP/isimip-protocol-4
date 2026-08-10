import argparse
import copy

import yaml

parser = argparse.ArgumentParser()
parser.add_argument('file_path')

args = parser.parse_args()

TEMPLATE = {
    'specifier': '',
    'long_name': '',
    'standard_name': '',
    'group': 'tropical-cyclones',
    'mandatory': True,
    'units': '',
    'frequency': '',
    'resolution': '',
    'comment': '',
    'path': {
        'ISIMIP4a': 'ISIMIP4a/InputData/climate/tropical_cyclones/obsclim/tracks/3hr/historical/ibtracs_obsclim_historical_1950_2025.nc',  # noqa: E501
        'ISIMIP4b': 'ISIMIP4b/InputData/climate/tropical_cyclones/obsclim/tracks/3hr/historical/ibtracs_obsclim_historical_1950_2025.nc',  # noqa: E501
    },
    'sectors': [
        'coastal'
    ]
}

try:
    from netCDF4 import Dataset
except ImportError:
    parser.error('No module named "netCDF4" Use "pip install netCDF4" to install it.')

definitions = []
with Dataset(args.file_path) as ds:
    for variable_name, variable in ds.variables.items():
        definition = copy.deepcopy(TEMPLATE)
        definition['specifier'] = variable_name

        for attribute_name in ['long_name', 'standard_name', 'units']:
            if attribute_name in variable.ncattrs():
                definition[attribute_name] = variable.getncattr(attribute_name)
            else:
                del definition[attribute_name]

        if 'description' in variable.ncattrs():
            definition['comment'] = variable.getncattr('description')
        else:
            del definition['comment']

        if variable.dimensions == ('storm', ):
            definition['resolution'] = 'per storm'
            del definition['frequency']
        else:
            definition['resolution'] = 'along-track'
            definition['frequency'] = 'at least 3-hourly'

        definitions.append(definition)

yaml_string = yaml.dump(definitions, sort_keys=False)
yaml_string = yaml_string.replace('\n- ', '\n\n- ')

print(yaml_string)
