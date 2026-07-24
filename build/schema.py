from pathlib import Path

from utils import (
    filter_rows,
    get_commit_hash,
    get_specifier_list,
    read_definitions,
    read_yaml_file,
    setup_logs,
    write_json,
)

URL = 'https://protocol.isimip.org/schema/'
EXCLUDE = ['model']

setup_logs()


def main():
    commit_hash = get_commit_hash()

    definitions = read_definitions()

    for schema_path in Path('schema').rglob('**/*.yaml'):
        schema_path_components = schema_path.with_suffix('').parts
        output_path = (Path('output') / schema_path).with_suffix('.json')

        simulation_round = schema_path_components[1]
        product = schema_path_components[2]
        if product.endswith('InputData'):
            category = schema_path_components[3]
            sector = None
        else:
            category = None
            sector = schema_path_components[3]

        # read schema template
        schema_template = read_yaml_file(schema_path)

        # create schema dict
        schema = {
            '$schema': 'http://json-schema.org/draft-07/schema#',
            '$id': URL + schema_path.as_posix(),
            'commit': commit_hash,
        }
        schema.update(schema_template)

        # loop over properties/specifiers/properties and add enums from definition files
        for identifier, properties in schema['properties']['specifiers']['properties'].items():
            if identifier in definitions:
                if identifier not in EXCLUDE:
                    rows = definitions[identifier]
                    enum = []

                    if product.endswith('InputData'):
                        for row in filter_rows(rows, simulation_round, product, category=category):
                            for specifier_value in get_specifier_list(row):
                                enum.append(specifier_value)
                    elif product == 'DerivedOutputData':
                        for row in filter_rows(rows, simulation_round, product):
                            for specifier_value in get_specifier_list(row):
                                enum.append(specifier_value)
                    else:
                        for row in filter_rows(rows, simulation_round, product, sector=sector):
                            for specifier_value in get_specifier_list(row):
                                enum.append(specifier_value)

                    properties['enum'] = list(set(enum))

        # write json schema
        write_json(output_path, schema)


if __name__ == '__main__':
    main()
