# Extron provides a different class for their file I/O. The following try construct
# ensures that no matter where we run this (our local PC, or an Extron processor),
# the "File" object contains the proper mechanism to successfully engage in file I/O
try:
    from extronlib.system import File, ProgramLog
except ModuleNotFoundError:
    print('INFO: Not running on Extron ControlScript, so using native Python file commands.')
    File = open

import json

# TODO:
#  - (DONE) add "data" section
#  - add "metadata" section
#  - add "descriptions" section
#  - add "types" section
#    -     types: string, boolean, integer, IP address, password


class ConfigManager:

    __version__ = '.9'

    def __init__(self, filename):

        self._config_dictionary = {}
        self.filename = filename
        self.changed = False

        self._load_from_file()

    def get_value(self, full_key_path, default_value=None, cast_as="string"):

        split_key_path = full_key_path.lower().split('/')
        tmp_object = self._config_dictionary['data']

        try:
            for single_key in split_key_path:
                tmp_object = tmp_object[single_key]

            value_to_return = tmp_object

        except (KeyError, TypeError, IndexError):
            value_to_return = default_value

        if cast_as.lower() == "str" or cast_as.lower() == "string":
            if value_to_return == "":
                return str(default_value)
            else:
                return str(value_to_return)

        elif cast_as.lower() == "bool" or cast_as.lower() == "boolean":
            if isinstance(value_to_return, bool):
                return value_to_return

            elif value_to_return is None:
                return False

            else:
                if value_to_return.lower() == 'true':
                    return True
                else:
                    return False

        elif cast_as.lower() == "int" or cast_as.lower() == "integer":
            return int(value_to_return)

    def set_value(self, full_key_path, value):

        self.changed = True
        split_key_path = full_key_path.lower().split('/')
        tmp_dictionary = self._config_dictionary['data']

        for key in split_key_path[:-1]:
            tmp_dictionary = tmp_dictionary.setdefault(key, {})

        tmp_dictionary[split_key_path[-1]] = value

    def commit(self):
        self.changed = False

        with File(self.filename, 'w') as f:
            f.write(json.dumps(self._config_dictionary, sort_keys=True, indent=4))

    def reload(self):
        self._load_from_file()

    def _load_from_file(self):
        self.changed = False

        with File(self.filename, 'r') as f:
            self._config_dictionary = json.loads(f.read())

    def print_config(self):
        print(self._config_dictionary)
