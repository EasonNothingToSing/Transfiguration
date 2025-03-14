import json
import jinja2


class Transfiguration:
    def __init__(self, configure: str) -> object:
        """

        :type configure: str
        """
        self._configure = configure
        self._traverse_configure(self._configure, "excel_module", None)

    def _traverse_configure(self, data, force_key, hook):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == force_key:
                    if hook:
                        hook(data)

                self._traverse_configure(value, force_key, hook)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                self._traverse_configure()

    def _get_excel_data(self, excel, sheet):
        pass