from jinja2 import Environment, FileSystemLoader
from Transpell.transfiguration import Transfiguration
import os
import json

# 获取当前目录
current_dir = os.path.dirname(__file__)  # 假设脚本在某个目录下运行
# 计算父父目录路径
parent_parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..', "Template"))

# 配置 Environment，指定多个搜索路径
env = Environment(loader=FileSystemLoader([current_dir, parent_parent_dir]))

# 定义模板字符串
template_string = """
{% import 'comlib-bsp.jinja' as bsp -%}
{% import 'comlib.jinja' as cmn -%}
{{cmn.H_File_Header_Macro_Filter_Start(Input.Target_Name)}}

{% for device in Input.Item.module_name -%}
{{bsp.Include_File_Generate_Macro(device)}}
{%- endfor %}

{% for device in Input.Item.device_name %}
{{bsp.IP_Define_Macro(device[1], device[2])}}
{%- endfor %}

{{cmn.H_File_Header_Macro_Filter_End(Input.Target_Name)}}
"""

template = env.from_string(template_string)

with open("../../Template/VenusA/Bsp/configure.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

        trs = Transfiguration(json_data, "a")

print(trs.get_result())

output = template.render(
    Input=trs.get_result()
)

print(output)
