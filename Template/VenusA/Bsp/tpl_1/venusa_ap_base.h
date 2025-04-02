{% import 'comlib-bsp.jinja' as bsp -%}
{% import 'comlib.jinja' as cmn -%}
{{cmn.H_File_Header_Macro_Filter_Start(Input.Target_Name)}}

{% for device in Input.Item.device_name %}
{{bsp.Device_Address_Define_Macro(device[0], cmn.HexAddress_Format(device[2]))}}
{%- endfor %}

{% for device in Input.Item.irq_name %}
{{bsp.Device_IRQ_Define_Macro(device[0], device[1])}}
{%- endfor %}

{{cmn.H_File_Header_Macro_Filter_End(Input.Target_Name)}}