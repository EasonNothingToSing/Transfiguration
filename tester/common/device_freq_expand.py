from jinja2 import Environment, FileSystemLoader
import os

# 获取当前目录
current_dir = os.path.dirname(__file__)  # 假设脚本在某个目录下运行
# 计算父父目录路径
parent_parent_dir = os.path.abspath(os.path.join(current_dir, '..', '..', "Template"))

# 配置 Environment，指定多个搜索路径
env = Environment(loader=FileSystemLoader([current_dir, parent_parent_dir]))

print(current_dir, parent_parent_dir)

# 定义模板字符串
template_string = """
{% import 'comlib-cmu.jinja' as cmu%}
调用宏并测试输出 
{{ cmu.device_get_frequence_define_macro(device_name, n_reg, m_reg, src_reg) }}
"""

# 从字符串创建模板
template = env.from_string(template_string)

# 动态传递变量
output = template.render(
    base="IP_SYS",
    num=1,
    device_name="flash",
    n_reg="HAL_CRM->REG_FLASH_CLK_CFG.bit.div_n",
    m_reg="HAL_CRM->REG_FLASH_CLK_CFG.bit.div_m",
    src_reg="HAL_CRM->REG_FLASH_CLK_CFG.bit.src",
    clock_born=None,
)

print(output)

output = template.render(
    base="IP_SYS",
    num=1,
    device_name="flash",
    n_reg=None,
    m_reg="HAL_CRM->REG_FLASH_CLK_CFG.bit.div_m",
    src_reg="HAL_CRM->REG_FLASH_CLK_CFG.bit.src",
    clock_born=None,
)

print(output)

output = template.render(
    base="IP_SYS",
    num=1,
    device_name="flash",
    n_reg="HAL_CRM->REG_FLASH_CLK_CFG.bit.div_n",
    m_reg=None,
    src_reg="HAL_CRM->REG_FLASH_CLK_CFG.bit.src",
    clock_born=None,
)

print(output)

output = template.render(
    base="IP_SYS",
    num=1,
    device_name="flash",
    n_reg=None,
    m_reg=None,
    src_reg="HAL_CRM->REG_FLASH_CLK_CFG.bit.src",
    clock_born=None,
)

print(output)