# import jinja2
# import json
# import transfiguration


# def Get_Excel_Data(name, sheet):
#     return ["uart", "i2c", "audio", "spi"]


# if __name__ == "__main__":

#     with open("./Template/VegaH/Bsp/configure.json", "r", encoding="utf-8") as f:
#         json_data = json.load(fp=f)
#         transfiguration.Transfiguration(json_data)

#         excel_func = json_data['Item']["driver_macro"]["excel_module"]
#         excel_name = f"'%s'" % (json_data['Item']["driver_macro"]["excel_name"], )
#         excel_sheet = f"'%s'" % (json_data['Item']["driver_macro"]["sheet"], )

#         json_data['Item']["driver_macro"]["excel_data"] = eval(f"{excel_func}({excel_name}, {excel_sheet})")

#         env = jinja2.environment.Environment(loader=jinja2.FileSystemLoader("."))

#         out = env.get_template("./Template/VegaH/Bsp/vegah_ap.h").render(confile=json_data)

#         print(out)
from jinja2 import Environment

# 创建 Jinja2 环境
env = Environment()

# 定义一个字符串作为模板
template_string = """
{# DEVICE DIVIDER SETTING #}
{%- macro device_div_setting_decalre_macro(name, n, m) -%}
    {# Check if both n and m are empty (None) -#}
    {%- if n is none and m is none -%}
        {# If both n and m are empty, do not generate the function #}
    {%- else -%}
        {# If either n or m has a value, generate the function #}
        int32_t HAL_CRM_Set{{name | title}}ClkDiv(
            {# Generate div_n parameter if n is not empty #}
            {%- if n is not none %}uint32_t div_n{% endif -%}
            {# Add a comma if both n and m are not empty #}
            {%- if n is not none and m is not none %}, {% endif -%}
            {# Generate div_m parameter if m is not empty #}
            {%- if m is not none %}uint32_t div_m{% endif -%}
        );
    {%- endif -%}
{%- endmacro -%}
 调用宏并测试输出 
{{ device_div_setting_decalre_macro(device_name, n_value, m_value) }}
"""

# 从字符串创建模板
template = env.from_string(template_string)

# 动态传递变量
output = template.render(
    device_name="motor",
    n_value=None,
    m_value=12
)

# 打印输出
print(output)
