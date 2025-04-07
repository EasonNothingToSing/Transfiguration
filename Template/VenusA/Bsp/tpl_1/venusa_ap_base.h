{% import 'comlib-bsp.jinja' as bsp -%}
{% import 'comlib.jinja' as cmn -%}
{{cmn.H_File_Header_Macro_Filter_Start(Input.Target_Name)}}

{% for device in Input.Item.device_name %}
{{bsp.Device_Address_Define_Macro(device[0], cmn.HexAddress_Format(device[2]))}}
{%- endfor %}

{% for device in Input.Item.irq_name %}
{{bsp.Device_IRQ_Define_Macro(device[0], device[1])}}
{%- endfor %}

typedef enum IRQn {
    /* =======================================  Nuclei Core Specific Interrupt Numbers  ======================================== */

    Reserved0_IRQn            =   0,              /*!<  Internal reserved */
    Reserved1_IRQn            =   1,              /*!<  Internal reserved */
    Reserved2_IRQn            =   2,              /*!<  Internal reserved */
    SysTimerSW_IRQn           =   3,              /*!<  System Timer SW interrupt */
    Reserved3_IRQn            =   4,              /*!<  Internal reserved */
    Reserved4_IRQn            =   5,              /*!<  Internal reserved */
    Reserved5_IRQn            =   6,              /*!<  Internal reserved */
    SysTimer_IRQn             =   7,              /*!<  System Timer Interrupt */
    Reserved6_IRQn            =   8,              /*!<  Internal reserved */
    Reserved7_IRQn            =   9,              /*!<  Internal reserved */
    Reserved8_IRQn            =  10,              /*!<  Internal reserved */
    Reserved9_IRQn            =  11,              /*!<  Internal reserved */
    Reserved10_IRQn           =  12,              /*!<  Internal reserved */
    Reserved11_IRQn           =  13,              /*!<  Internal reserved */
    Reserved12_IRQn           =  14,              /*!<  Internal reserved */
    Reserved13_IRQn           =  15,              /*!<  Internal reserved */
    InterCore_IRQn            =  16,              /*!<  CIDU Inter Core Interrupt */
    Reserved15_IRQn           =  17,              /*!<  Internal reserved */
    Reserved16_IRQn           =  18,              /*!<  Internal reserved */

    /* ===========================================  demosoc Specific Interrupt Numbers  ========================================= */
    /* ToDo: add here your device specific external interrupt numbers. 19~1023 is reserved number for user. Maxmum interrupt supported
             could get from clicinfo.NUM_INTERRUPT. According the interrupt handlers defined in startup_Device.s
             eg.: Interrupt for Timer#1       eclic_tim1_handler   ->   TIM1_IRQn */
    SOC_INT19_IRQn           = 19,                /*!< Device Interrupt */
    SOC_INT20_IRQn           = 20,                /*!< Device Interrupt */
    SOC_INT21_IRQn           = 21,                /*!< Device Interrupt */
    SOC_INT22_IRQn           = 22,                /*!< Device Interrupt */
    SOC_INT23_IRQn           = 23,                /*!< Device Interrupt */
    SOC_INT24_IRQn           = 24,                /*!< Device Interrupt */
    SOC_INT25_IRQn           = 25,                /*!< Device Interrupt */
    SOC_INT26_IRQn           = 26,                /*!< Device Interrupt */
    SOC_INT27_IRQn           = 27,                /*!< Device Interrupt */
    SOC_INT28_IRQn           = 28,                /*!< Device Interrupt */
    SOC_INT29_IRQn           = 29,                /*!< Device Interrupt */
    SOC_INT30_IRQn           = 30,                /*!< Device Interrupt */
    SOC_INT31_IRQn           = 31,                /*!< Device Interrupt */
    SOC_INT32_IRQn           = 32,                /*!< Device Interrupt */
    SOC_INT33_IRQn           = 33,                /*!< Device Interrupt */
    SOC_INT34_IRQn           = 34,                /*!< Device Interrupt */
    SOC_INT35_IRQn           = 35,                /*!< Device Interrupt */
    SOC_INT36_IRQn           = 36,                /*!< Device Interrupt */
    SOC_INT37_IRQn           = 37,                /*!< Device Interrupt */
    SOC_INT38_IRQn           = 38,                /*!< Device Interrupt */
    SOC_INT39_IRQn           = 39,                /*!< Device Interrupt */
    SOC_INT40_IRQn           = 40,                /*!< Device Interrupt */
    SOC_INT41_IRQn           = 41,                /*!< Device Interrupt */
    SOC_INT42_IRQn           = 42,                /*!< Device Interrupt */
    SOC_INT43_IRQn           = 43,                /*!< Device Interrupt */
    SOC_INT44_IRQn           = 44,                /*!< Device Interrupt */
    SOC_INT45_IRQn           = 45,                /*!< Device Interrupt */
    SOC_INT46_IRQn           = 46,                /*!< Device Interrupt */
    SOC_INT47_IRQn           = 47,                /*!< Device Interrupt */
    SOC_INT48_IRQn           = 48,                /*!< Device Interrupt */
    SOC_INT49_IRQn           = 49,                /*!< Device Interrupt */
    SOC_INT50_IRQn           = 50,                /*!< Device Interrupt */
    SOC_INT51_IRQn           = 51,                /*!< Device Interrupt */
    SOC_INT52_IRQn           = 52,                /*!< Device Interrupt */
    SOC_INT53_IRQn           = 53,                /*!< Device Interrupt */
    SOC_INT54_IRQn           = 54,                /*!< Device Interrupt */
    SOC_INT55_IRQn           = 55,                /*!< Device Interrupt */
    SOC_INT56_IRQn           = 56,                /*!< Device Interrupt */
    SOC_INT57_IRQn           = 57,                /*!< Device Interrupt */
    SOC_INT58_IRQn           = 58,                /*!< Device Interrupt */
    SOC_INT59_IRQn           = 59,                /*!< Device Interrupt */
    SOC_INT60_IRQn           = 60,                /*!< Device Interrupt */
    SOC_INT61_IRQn           = 61,                /*!< Device Interrupt */
    SOC_INT62_IRQn           = 62,                /*!< Device Interrupt */
    SOC_INT63_IRQn           = 63,                /*!< Device Interrupt */
    SOC_INT64_IRQn           = 64,                /*!< Device Interrupt */
    SOC_INT65_IRQn           = 65,                /*!< Device Interrupt */
    SOC_INT66_IRQn           = 66,                /*!< Device Interrupt */

    SOC_INT_MAX,
} IRQn_Type;

// External IRQn ID(intr_id) is from the hard-wired perspective,
// which has an offset mapped to the ECLIC IRQn
#define ECLIC_IRQn_OFFSET_CIDU_INTn     SOC_INT20_IRQn // IRQ_TIMER0_VECTOR

{{cmn.H_File_Header_Macro_Filter_End(Input.Target_Name)}}