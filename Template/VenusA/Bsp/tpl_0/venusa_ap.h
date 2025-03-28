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