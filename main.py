# import ast
# import pandas


# # 自定义函数（与之前一致）
# def Concat(a, b):
#     return a + b


# def Length(s):
#     return len(s)


# def Add(a, b):
#     return int(a) + int(b)  # 支持字符串输入


# def Multiply(a, b):
#     return a * b


# def Outer(x):
#     return f"Result: {x}"


# def Inner(a, b):
#     return f"{a}_{b}"


# def _get_excel_cols_data():
#     d = pandas.read_excel("VenusA_SoC_Memory_Mapping.xlsx", sheet_name="cmn_aon_peri", usecols=['Module', 'Sheet name', 'Address Start'], header=0)

#     d = d.dropna()

#     return d.values.tolist()


# # JSON 数据（使用 Python 语法）
# json_data = {
#     "App_Name": "MyApp",
#     "Version": "2.0",
#     "Expressions": [
#         "context['CustomVar'] = 'Hello'",
#         "context['Counter'] = 5",
#         "Concat(context['App_Name'], context['CustomVar'])",
#         "Multiply(Length(context['Version']), Add(2, context['Counter']))",
#         "context['Counter'] = '3'",
#         "Outer(Inner(context['App_Name'], Length(context['CustomVar'])))",
#         "context['Excel_Data'] = _get_excel_cols_data()"
#     ]
# }


# # AST 转换器：验证或修改函数调用
# class ExpressionTransformer(ast.NodeTransformer):
#     def visit_Call(self, node):
#         if isinstance(node.func, ast.Name):
#             valid_functions = {'Concat', 'Length', 'Add', 'Multiply', 'Outer', 'Inner', '_get_excel_cols_data'}
#             if node.func.id not in valid_functions:
#                 print(f"Warning: Unknown function {node.func.id}")
#         return self.generic_visit(node)


# # 处理 JSON 中的表达式
# def process_json_expressions(json_data):
#     results = []
#     # 初始化上下文
#     context = {
#         "App_Name": json_data["App_Name"],
#         "Version": json_data["Version"]
#     }

#     # 全局环境（包含自定义函数）
#     global_env = globals().copy()
#     global_env['context'] = context

#     # 处理每个表达式
#     for i, expr in enumerate(json_data["Expressions"], 1):
#         print(f"\nProcessing expression {i}:")
#         print(f"Original: {expr}")

#         # 解析为 AST
#         try:
#             # 表达式可能是赋值（exec）或表达式（eval）
#             tree = ast.parse(expr, mode='exec')  # 默认使用 exec 模式

#             # 应用 AST 转换
#             transformer = ExpressionTransformer()
#             new_tree = transformer.visit(tree)

#             # 修复 AST
#             ast.fix_missing_locations(new_tree)

#             # 转换为可读代码
#             transformed_code = ast.unparse(new_tree).strip()
#             print(f"Transformed code: {transformed_code}")

#             # 判断是赋值还是表达式
#             if isinstance(new_tree.body[0], ast.Assign):
#                 # 赋值语句（如 context['CustomVar'] = 'Hello'）
#                 exec(compile(new_tree, '<string>', 'exec'), global_env)
#                 print(f"Updated context: {context}")
#                 results.append({
#                     "type": "assign",
#                     "context": dict(context)
#                 })
#             else:
#                 # 表达式（如 Concat(...)）
#                 result = eval(expr, global_env)
#                 print(f"Execution result: {result}")
#                 results.append({
#                     "type": "expression",
#                     "code": transformed_code,
#                     "result": result
#                 })

#         except Exception as e:
#             print(f"Error in expression {i}: {e}")
#             results.append({"type": "error", "error": str(e)})

#     return results


# # 运行处理
# results = process_json_expressions(json_data)

# # 打印最终结果
# print("\nFinal results:")
# for i, result in enumerate(results, 1):
#     if result["type"] == "assign":
#         print(f"Expression {i}: Defined variable in context: {result['context']}")
#     elif result["type"] == "expression":
#         print(f"Expression {i}: {result['result']}")
#     else:
#         print(f"Expression {i}: Error - {result['error']}")

# import ast
# # code = ("x = 3 \r\n"
# #         "def hello(): return 'Hello, World!'")
# code = ("hello(['class', 'var'])")
# tree = ast.parse(code)
# print(ast.dump(tree, indent=2))
# for node in ast.walk(tree):
#     print(f"Node={node}")
#     if isinstance(node, ast.FunctionDef):
#         print(f"Found function: {node.name}")
#     elif isinstance(node, ast.Call):
#         print(f"Function call: {node.func}")


from Transpell import *
from global_env import *

if __name__ == "__main__":
    global_var_init()
    tmake = Transmake("VenusA", "./Template/VenusA/Bsp")
    tmake.tmake()
