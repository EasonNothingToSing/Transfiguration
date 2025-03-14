{% import './Template/comlib' as comlib -%}

{{ comlib.H_File_Header_Macro_Filter_Start(confile.Target_Name) }}

{{ comlib.Include_File_Bundle_Filter(confile.Item.driver_macro)}}

{{ comlib.H_File_Header_Macro_Filter_End(confile.Target_Name) }}
