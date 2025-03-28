from jinja2 import Environment, FileSystemLoader
import os

# 获取当前目录
current_dir = os.path.dirname(__file__)  # 假设脚本在某个目录下运行
# 计算父父目录路径
parent_parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..', "Template"))

# 配置 Environment，指定多个搜索路径
env = Environment(loader=FileSystemLoader([current_dir, parent_parent_dir]))

# 定义模板字符串
template_string = """
{% import 'comlib-cmu.jinja' as cmu%}
调用宏并测试输出 
{{ cmu.source_header_src_name_decalre_macro(src_name_list) }}
{{ cmu.source_header_pll_para_decalre_macro(pll_name, para_list) }}
"""

template = env.from_string(template_string)

# 动态传递变量
output = template.render(
    src_name_list=["SysPLLUsb", "SysPLLFreq"],
    pll_name="SysPLLUsb",
    para_list=[{"div": 3, "value": 4}, {"div": 4, "value": 5}]
)

print(output)