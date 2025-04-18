import pandas
import os
import re
import ast

class ExpressionTransformer(ast.NodeTransformer):
    def __init__(self, database):
        self._database = database
        self._global_namepsace = {
            "ReadExcel": self.ReadExcel,
            "DataExtend": self.DataExtend,
            "List2Dict": self.List2Dict
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
        
    def DataExtend(self, *data):
        if len(data) == 0:
            raise ValueError("No data provided")
        
        if len(data) == 1:
            return data[0]
        
        result = []

        t_len = len(data[0])
        for i in range(1, len(data)):
            if len(data[i]) != t_len:
                raise ValueError(f"Data length mismatch: {len(data[i])} != {t_len}")
            
        for i in range(t_len):
            row = []
            for j in range(len(data)):
                row.extend(data[j][i])
            result.append(row)

        return result
    
    def List2Dict(self, data: list, keys: list):
        if not isinstance(data, list):
            raise TypeError("Data must be a list")
        
        if not isinstance(keys, list):
            raise TypeError("Keys must be a list")

        if len(data) == 0:
            return []
        
        if len(data[0]) != len(keys):
            raise ValueError(f"Data length mismatch: {len(data[0])} != {len(keys)}")
        
        result = []
        for i in range(len(data)):
            result.append(dict(zip(keys, data[i])))
        
        return result
    
    def DeduplicateKey(self, data: list, keys: list):
        if not isinstance(data, list):
            raise TypeError("Data must be a list")
        
        if len(data) == 0:
            return []
        
        if not isinstance(data[0], dict):
            raise TypeError("Data must be a list of dictionaries")
        
        if not isinstance(keys, list):
            raise TypeError("Keys must be a list")
        
        result = []
        for i in range(len(data)):
            for k in range(len(result)):
                if all(data[i][key] == result[k][key] for key in keys):
                    break
            else:
                result.append(data[i])
        
        return result
