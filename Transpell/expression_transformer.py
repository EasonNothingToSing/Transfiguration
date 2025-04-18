import pandas
import os
import re
import ast

class ExpressionTransformer(ast.NodeTransformer):
    def __init__(self, database):
        self._database = database
        self._global_namepsace = {
            "ReadExcel": self.ReadExcel,
        }
        super().__init__()

    def visit_Call(self, node):
        self.generic_visit(node)

        if isinstance(node.func, ast.Name):
            if node.func.id not in self._global_namepsace.keys():
                print(f"Warning: Unknown function {node.func.id}")
                return node
            func = self._global_namepsace.get(node.func.id)
            if callable(func):
                args = [ast.literal_eval(arg) for arg in node.args]
                result = func(*args)

                return ast.Constant(value=result)
        return node

    def visit_Expression(self, node):
        self.generic_visit(node)

        return node

    def __locate_sheet(self, xlsx_handler, sheet, colname):
        d = pandas.read_excel(xlsx_handler, sheet_name=sheet, header=0, nrows=1)
        for i, c in enumerate(d.columns):
            if c == colname:
                return i

        xlsx_handler.close()
        raise ValueError(f"None of the specified columns found --> {colname}")
    
    def ReadExcel(self, excel: str, sheet: str, colnames: str or list):
        if not os.path.exists(os.path.join(self._database, excel)):
            raise FileNotFoundError(f"File {excel} not found in {self._database}")
        
        with pandas.ExcelFile(os.path.join(self._database, excel)) as xlsx_handler:

            if sheet not in xlsx_handler.sheet_names:
                raise ValueError(f"No sheet named {sheet} found in {excel}")            
            
            if not colnames:
                raise ValueError("Column names must be provided")            

            col = []
            if isinstance(colnames, str):
                col.append(self.__locate_sheet(xlsx_handler, sheet, colnames))
            elif isinstance(colnames, list):
                for name in colnames:
                    col.append(self.__locate_sheet(xlsx_handler, sheet, name))

            d = pandas.read_excel(xlsx_handler, sheet_name=sheet, usecols=col, header=0)

            d = d.iloc[:, [sorted(col).index(i) for i in col]]
            d = d.dropna()

            return d.values.tolist()
