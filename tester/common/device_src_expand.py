from jinja2 import Environment, FileSystemLoader
import os

# 获取当前目录
current_dir = os.path.dirname(__file__)  # 假设脚本在某个目录下运行
# 计算父父目录路径
parent_parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..', "Template"))

# 配置 Environment，指定多个搜索路径
env = Environment(loader=FileSystemLoader([current_dir, parent_parent_dir]))

# 定义一个字符串作为模板
template_string = """
{% import 'comlib-cmu.jinja' as cmu%}
 调用宏并测试输出 
{{ cmu.device_src_setting_decalre_macro(device_name) }}
{{ cmu.device_src_setting_define_macro(device_name, cmu.device_peri_extend("base", reg, num), choice) }}

"""

# 从字符串创建模板
template = env.from_string(template_string)

# 动态传递变量
output = template.render(
    base="IP_SYS",
    num=1,
    device_name="flash",
    reg="SEL_FLASHC_CLK",
    choice=['CRM_IpSrcXtalClk', 'CRM_IpSrcCoreClk']

)

print(output)