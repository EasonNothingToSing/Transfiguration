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
{{ cmu.device_div_setting_decalre_macro(device_name, n_reg, m_reg) }}
{{ cmu.device_div_setting_define_macro(device_name, n_reg, n_max, m_reg, m_max) }}
"""

# 从字符串创建模板
template = env.from_string(template_string)

# 动态传递变量
output = template.render(
    device_name="Uart",
    n_reg="IP_SYSCTRL->REG_CLK_CTRL.bit.N",
    n_max="0x3ff",
    m_reg="IP_SYSCTRL->REG_CLK_CTRL.bit.M",
    m_max="0x3ff",
)

print(output)

# 动态传递变量
output = template.render(
    device_name="Uart",
    n_reg=None,
    n_max="0x3ff",
    m_reg="IP_SYSCTRL->REG_CLK_CTRL.bit.M",
    m_max="0x3ff",
)

print(output)

# 动态传递变量
output = template.render(
    device_name="Uart",
    n_reg=None,
    n_max="0x3ff",
    m_reg=None,
    m_max="0x3ff",
)

print(output)