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
{{ cmu.device_header_expend_loop(device_list) }}
{{ cmu.device_source_expend_loop(device_list) }}
"""

template = env.from_string(template_string)

# 动态传递变量
output = template.render(
    device_list=[
        {
        "base":"IP_SYS",
        "num":1,
        "name": "Uart0",
        "mudule": None,
        "gate_reg": None,
        "gate_def": None,
        "src_reg": "SEL_UART0_CLK",
        "src_choice": ['CRM_IpSrcXtalClk', 'CRM_IpSrcCoreClk'],
        "n_reg": "DIV_UART0_CLK_N",
        "n_def": 1,
        "n_mask": "0x3ff",
        "m_reg": "DIV_UART0_CLK_M",
        "m_def": 1,
        "m_mask": "0x3ff",
        "ld_reg": "DIV_UART0_CLK_LD",
        "clock_born": None
      },
      {
        "base":"IP_SYS",
        "num":1,
        "name": "Uart1",
        "mudule": None,
        "gate_reg": None,
        "gate_def": None,
        "src_reg": "SEL_UART1_CLK",
        "src_choice": ['CRM_IpSrcXtalClk', 'CRM_IpSrcCoreClk'],
        "n_reg": "DIV_UART1_CLK_N",
        "n_def": 1,
        "n_mask": "0x3ff",
        "m_reg": "DIV_UART1_CLK_M",
        "m_def": 1,
        "m_mask": "0x3ff",
        "ld_reg": "DIV_UART1_CLK_LD",
        "clock_born": None
      },
    ]
)

print(output)