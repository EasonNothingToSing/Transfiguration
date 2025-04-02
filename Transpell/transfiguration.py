import json
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import pandas
import re
import os

from global_env import *


class Transfiguration:
    _TEMPLATE_PATH = os.path.join(os.getcwd(), "Template")

    def __init__(self):
        self._configure = None
        self._target = None
        self._database = None
        self._output = None
        self._available_funcs = {
            "Get_Excel_Data": self._get_excel_cols_data,
            "Get_Excel_Data_Col": self._get_excel_cols_data2,
            "Get_Excel_Data_Col_Skip_Row": self._get_excel_cols_data3,
            "Deduplicate_Modules_Name": self._deduplicate_modules_name
        }
        self._env = Environment(loader=FileSystemLoader([Transfiguration._TEMPLATE_PATH, os.getcwd()]))

    def process(self, configure: str):
        self._configure = configure
        with open(self._configure, "r", encoding="utf-8") as f:
            configure_json = json.load(f)
            self._target = configure_json['Target_Name']
            self._database_filter(configure_json['Datebase'])
            # preprocess
            self._output = self._traverse_recursive(configure_json)

        for _target in self._target:
            self._output["Target_Name"] = _target
            t_path = Path(os.path.normpath(os.path.join(os.path.dirname(self._configure), _target))).as_posix()
            template = self._env.get_template(t_path)
            print(template.render(Input=self._output))

    def _database_filter(self, database : str):
        database_string = ""
        if database == "~/database":
            self._database = os.path.join(Transfiguration._TEMPLATE_PATH, "database")

    def _traverse_recursive(self, config):
        if isinstance(config, dict):
            return {k: self._traverse_recursive(v) for k, v in config.items()}
        if isinstance(config, list):
            return [self._traverse_recursive(i) for i in config]
        if isinstance(config, str) and config.startswith('$func:'):
            func_call = config[len('$func:'):]
            func_name, args_str = re.match(r'(\w+)\((.*)\)', func_call).groups()

            args = []
            current_arg = ''
            parentheses_count = 0
            brackets_count = 0
            for char in args_str:
                if char == ',' and parentheses_count == 0 and brackets_count == 0:
                    args.append(current_arg.strip())
                    current_arg = ''
                else:
                    current_arg += char
                    if char == '(':
                        parentheses_count += 1
                    elif char == ')':
                        parentheses_count -= 1
                    if char == '[':
                        brackets_count += 1
                    elif char == ']':
                        brackets_count -= 1
            if current_arg:
                args.append(current_arg.strip())

            processed_args = []
            for arg in args:
                arg = arg.strip("'")
                if arg.startswith('$func:'):
                    processed_args.append(self._traverse_recursive(arg.strip("'")))
                else:
                    processed_args.append(arg)
            
            # 调用函数
            return self._available_funcs[func_name](*processed_args)
        return config

    def _get_excel_cols_data(self, excel: str, sheet: str, colname):
        col = []
        try:
            colname = eval(colname)

            for name in colname:
                col.append(self.__locate_sheet(excel, sheet, name))
        except SyntaxError:
                col.append(self.__locate_sheet(excel, sheet, colname))

        d = pandas.read_excel(os.path.join(self._database, excel), sheet_name=sheet, usecols=col, header=0)

        d = d.iloc[:, [sorted(col).index(i) for i in col]]
        d = d.dropna()

        return d.values.tolist()
    
    def _get_excel_cols_data2(self, excel: str, sheet: str, cols):
        try:
            cols = eval(cols)
        except SyntaxError:
            cols = [cols]
        
        d = pandas.read_excel(os.path.join(self._database, excel), sheet_name=sheet, usecols=cols, header=0)
        return d.values.tolist()
    
    def _get_excel_cols_data3(self, excel: str, sheet: str, skip_row: int, cols):
        try:
            cols = eval(cols)
        except SyntaxError:
            cols = [cols]
        
        d = pandas.read_excel(os.path.join(self._database, excel), sheet_name=sheet, usecols=cols, header=0, skiprows=skip_row)
        return d.values.tolist()
    
    def _deduplicate_modules_name(self, modules: list):
        deduped_modules = []
        for i in modules:
            if i[0] not in deduped_modules and not pandas.isna(i[0]) and i[0] != 'Reserved':
                deduped_modules.extend(i)
        return deduped_modules
    
    def __locate_sheet(self, excel, sheet, colname):
        d = pandas.read_excel(os.path.join(self._database, excel), sheet_name=sheet, header=0, nrows=1)
        for i, c in enumerate(d.columns):
            if c == colname:
                return i
            
        return None

