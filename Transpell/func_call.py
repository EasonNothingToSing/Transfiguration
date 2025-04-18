import pandas
import os
import re
import ast

# 自定义函数（与之前一致）
def Concat(a, b):
    return a + b


def Length(s):
    return len(s)


def Add(a, b):
    return int(a) + int(b)  # 支持字符串输入


def Multiply(a, b):
    return a * b


def Outer(x):
    return f"Result: {x}"


def Inner(a, b):
    return f"{a}_{b}"


def ListExtend(a):
    return [x for x in range(a)]





class ExpressionTransformer(ast.NodeTransformer):
    def __init__(self, database):
        self._database = database
        self._global_namepsace = globals()
        super().__init__()

    def visit_Call(self, node):
        self.generic_visit(node)

        if isinstance(node.func, ast.Name):
            valid_functions = {'Concat', 'Length', 'Add', 'Multiply', 'Outer', 'Inner', 'ListExtend'}
            if node.func.id not in valid_functions:
                print(f"Warning: Unknown function {node.func.id}")
                return node
            func = self._global_namepsace.get(node.func.id)
            if callable(func):
                args = [ast.literal_eval(arg) for arg in node.args]
                result = func(*args)

                return ast.Constant(value=result)
        return node
    
    def ReadExcel(excel: str, sheet: any, colnames):
        if isinstance(sheet, str):
            pass
        elif isinstance(sheet, list):
            for s in sheet:
                if isinstance(colnames, str):
                    colnames = [colnames]
                if isinstance(colnames, list):
                    pass


# def _get_excel_cols_data(excel: str, sheet: str, colname):
#     col = []
#     try:
#         # TODO: need beast function
#         if colname == "Class":
#             raise SyntaxError('')
#         colname = eval(colname)

#         for name in colname:
#             col.append(__locate_sheet(excel, sheet, name))
#     except SyntaxError:
#             col.append(__locate_sheet(excel, sheet, colname))

#     d = pandas.read_excel(os.path.join(_database, excel), sheet_name=sheet, usecols=col, header=0)

#     d = d.iloc[:, [sorted(col).index(i) for i in col]]
#     d = d.dropna()

#     return d.values.tolist()

# def _get_excel_cols_data2(excel: str, sheet: str, cols):
#     try:
#         cols = eval(cols)
#     except SyntaxError:
#         cols = [cols]
    
#     d = pandas.read_excel(os.path.join(_database, excel), sheet_name=sheet, usecols=cols, header=0)
#     return d.values.tolist()

# def _get_excel_cols_data3(excel: str, sheet: str, skip_row: int, cols):
#     try:
#         cols = eval(cols)
#     except SyntaxError:
#         cols = [cols]
    
#     d = pandas.read_excel(os.path.join(_database, excel), sheet_name=sheet, usecols=cols, header=0, skiprows=skip_row)
#     return d.values.tolist()

# def _deduplicate_modules_name(modules: list):
#     deduped_modules = []
#     for i in modules:
#         if i[0] not in deduped_modules and not pandas.isna(i[0]) and i[0] != 'Reserved':
#             deduped_modules.extend(i)
#     return deduped_modules

# def __locate_sheet(excel, sheet, colname):
#     d = pandas.read_excel(os.path.join(_database, excel), sheet_name=sheet, header=0, nrows=1)
#     for i, c in enumerate(d.columns):
#         if c == colname:
#             return i
        
#     return None

# def _list_extend(*_list):
#     o_list = []

#     for __list in _list:
#         o_list.extend(__list)
#     return o_list

# def _str_filter(_string, func_list, *_list):
#     def _str_to_num(_string):
#         return _string.split('_')[1]

#     def _str_brackets(_string):
#         return re.sub(r'\[(\d+)\]', r'_\1', _string)
    
#     def find_string_in_list(lst):
#         # 递归函数，检查列表及其嵌套列表是否部分包含 _string
#         result_lists = []
        
#         # 如果当前对象不是列表，跳过
#         if not isinstance(lst, list):
#             return result_lists
        
#         # 检查当前列表中的每个元素是否部分包含 _string
#         for item in lst:
#             if isinstance(item, str) and _string in item:
#                 __o_list = []

#                 if func_list:
#                     for _num, _item in enumerate(lst):
#                         if func_list[_num] is not None:
#                             __o_list.append(func_list[_num](_item))
#                         else:
#                             __o_list.append(_item)

#                     lst = __o_list
#                 result_lists.append(lst)
#                 break  # 找到一个匹配就跳出，避免重复添加
        
#         # 递归检查每个子列表
#         for item in lst:
#             if isinstance(item, list):
#                 result_lists.extend(find_string_in_list(item))
        
#         return result_lists

#     func_list = eval(func_list)
#     o_list = []  # 用于存储符合条件的列表
    
#     # 处理传入的每个 _list
#     for sub_list in _list:
#         result = find_string_in_list(sub_list)
#         o_list.extend(result)
    
#     return o_list