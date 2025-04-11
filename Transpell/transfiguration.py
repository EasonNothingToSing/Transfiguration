import json
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import pandas
import re
import os
import ast

from global_env import *


class Transfiguration:
    _TEMPLATE_PATH = os.path.join(os.getcwd(), "Template")

    def __init__(self):
        self._configure_name = None
        self._configure = None
        self._target = None
        self._target_name = None
        self._database = None
        self._template_output = None
        self._available_funcs = {
            "Get_Excel_Data": self._get_excel_cols_data,
            "Get_Excel_Data_Col": self._get_excel_cols_data2,
            "Get_Excel_Data_Col_Skip_Row": self._get_excel_cols_data3,
            "Deduplicate_Modules_Name": self._deduplicate_modules_name,
            "Extend": self._list_extend,
            "String_Filter": self._str_filter,
        }
        self._env = Environment(loader=FileSystemLoader([Transfiguration._TEMPLATE_PATH, os.getcwd()]))

    def process(self, configure: str):
        self._configure_name = configure
        json_out = []
        with open(self._configure_name, "r", encoding="utf-8") as f:
            configure_json = json.load(f)
            self._configure = configure_json
            # Get the target name and it is a list
            self._target = configure_json['Target_Name']
            self._database_filter(configure_json['Datebase'])
            # preprocess
            self._template_output = self._traverse_recursive(configure_json)

        for _target in self._target:
            self._template_output["Target_Name"] = _target
            self._target_name = _target
            t_path = Path(os.path.normpath(os.path.join(os.path.dirname(self._configure_name), _target))).as_posix()
            template = self._env.get_template(t_path)
            json_out.append(template.render(Input=self._template_output))

        return json_out

    def get_target_name(self):
        return self._target

    def _database_filter(self, database : str):
        database_string = ""
        if database == "~/database":
            self._database = os.path.join(Transfiguration._TEMPLATE_PATH, "database")

    def _traverse_recursive(self, config):
        # Handle dictionaries
        if isinstance(config, dict):
            return {k: self._traverse_recursive(v) for k, v in config.items()}
        # Handle lists
        if isinstance(config, list):
            return [self._traverse_recursive(i) for i in config]
        # Handle strings
        if isinstance(config, str):
            # Handle variable references with $var:
            if config.startswith('$var:'):
                var_key = config[len('$var:'):]
                if var_key in self._configure:
                    # Recursively process the variable value, as it might contain $func: or $var:
                    return self._traverse_recursive(self._configure[var_key])
                else:
                    raise ValueError(f"Variable '{var_key}' not found in JSON variables")
            # Handle function calls with $func:
            if config.startswith('$func:'):
                func_call = config[len('$func:'):]
                match = re.match(r'(\w+)\((.*)\)', func_call)
                if not match:
                    raise ValueError(f"Invalid function call format: {func_call}")
                func_name, args_str = match.groups()

                # Parse function arguments
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

                # Process arguments (recursively handle nested $func: or $var:)
                processed_args = []
                for arg in args:
                    arg = arg.strip("'")
                    # If the argument starts with $func: or $var:, process it recursively
                    if arg.startswith('$func:') or arg.startswith('$var:'):
                        processed_args.append(self._traverse_recursive(arg))
                    else:
                        processed_args.append(arg)

                # Check if the function exists and call it
                if func_name not in self._available_funcs:
                    raise ValueError(f"Function '{func_name}' not found")
                return self._available_funcs[func_name](*processed_args)
        # Return the original value if it's not a string or doesn't start with $func:/$var:
        return config

    def _get_excel_cols_data(self, excel: str, sheet: str, colname):
        col = []
        try:
            # TODO: need beast function
            if colname == "Class":
                raise SyntaxError('')
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

    def _list_extend(self, *_list):
        o_list = []

        for __list in _list:
            o_list.extend(__list)
        return o_list
    
    def _str_filter(self, _string, func_list, *_list):
        def _str_to_num(_string):
            return _string.split('_')[1]
    
        def _str_brackets(_string):
            return re.sub(r'\[(\d+)\]', r'_\1', _string)
        
        def find_string_in_list(lst):
            # 递归函数，检查列表及其嵌套列表是否部分包含 _string
            result_lists = []
            
            # 如果当前对象不是列表，跳过
            if not isinstance(lst, list):
                return result_lists
            
            # 检查当前列表中的每个元素是否部分包含 _string
            for item in lst:
                if isinstance(item, str) and _string in item:
                    __o_list = []

                    if func_list:
                        for _num, _item in enumerate(lst):
                            if func_list[_num] is not None:
                                __o_list.append(func_list[_num](_item))
                            else:
                                __o_list.append(_item)

                        lst = __o_list
                    result_lists.append(lst)
                    break  # 找到一个匹配就跳出，避免重复添加
            
            # 递归检查每个子列表
            for item in lst:
                if isinstance(item, list):
                    result_lists.extend(find_string_in_list(item))
            
            return result_lists

        func_list = eval(func_list)
        o_list = []  # 用于存储符合条件的列表
        
        # 处理传入的每个 _list
        for sub_list in _list:
            result = find_string_in_list(sub_list)
            o_list.extend(result)
        
        return o_list
