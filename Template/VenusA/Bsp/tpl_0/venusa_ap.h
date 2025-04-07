{% import 'comlib-bsp.jinja' as bsp -%}
{% import 'comlib.jinja' as cmn -%}
{{cmn.H_File_Header_Macro_Filter_Start(Input.Target_Name)}}

#include <stddef.h>
#include <stdint.h>
#include <nmsis_core.h>                         /*!< Nuclei N/NX class processor and core peripherals */
/* ToDo: include your system_mars.h file
         replace 'Device' with your device name */
#include <nmsis_core.h>                         /*!< Nuclei N/NX class processor and core peripherals */
/* ToDo: include your system_mars.h file
         replace 'Device' with your device name */
#include "system_RISCVN300.h"                    /*!< riscv N300 System */
#include "venusa_ap_base.h"

{% for device in Input.Item.module_name -%}
{{bsp.Include_File_Generate_Macro(device)}}
{%- endfor %}

{% for device in Input.Item.device_name %}
{{bsp.IP_Define_Macro(device[0], device[1])}}
{%- endfor %}

typedef struct IRegion_Info {
    unsigned long iregion_base;         /*!< Internal region base address */
    unsigned long eclic_base;           /*!< eclic base address */
    unsigned long systimer_base;        /*!< system timer base address */
    unsigned long smp_base;             /*!< smp base address */
    unsigned long idu_base;             /*!< idu base address */
} IRegion_Info_Type;

typedef enum EXCn {
    /* =======================================  Nuclei N/NX Specific Exception Code  ======================================== */
    InsUnalign_EXCn          =   0,              /*!<  Instruction address misaligned */
    InsAccFault_EXCn         =   1,              /*!<  Instruction access fault */
    IlleIns_EXCn             =   2,              /*!<  Illegal instruction */
    Break_EXCn               =   3,              /*!<  Beakpoint */
    LdAddrUnalign_EXCn       =   4,              /*!<  Load address misaligned */
    LdFault_EXCn             =   5,              /*!<  Load access fault */
    StAddrUnalign_EXCn       =   6,              /*!<  Store or AMO address misaligned */
    StAccessFault_EXCn       =   7,              /*!<  Store or AMO access fault */
    UmodeEcall_EXCn          =   8,              /*!<  Environment call from User mode */
    SmodeEcall_EXCn          =   9,              /*!<  Environment call from S-mode */
    MmodeEcall_EXCn          =  11,              /*!<  Environment call from Machine mode */
    InsPageFault_EXCn        =  12,              /*!<  Instruction page fault */
    LdPageFault_EXCn         =  13,              /*!<  Load page fault */
    StPageFault_EXCn         =  15,              /*!<  Store or AMO page fault */
    NMI_EXCn                 =  0xfff,           /*!<  NMI interrupt */
} EXCn_Type;

#if __riscv_xlen == 32

#ifndef __NUCLEI_CORE_REV
#define __NUCLEI_N_REV            0x0104    /*!< Core Revision r1p4 */
#else
#define __NUCLEI_N_REV            __NUCLEI_CORE_REV
#endif

#elif __riscv_xlen == 64

#ifndef __NUCLEI_CORE_REV
#define __NUCLEI_NX_REV           0x0100    /*!< Core Revision r1p0 */
#else
#define __NUCLEI_NX_REV           __NUCLEI_CORE_REV
#endif

#endif /* __riscv_xlen == 64 */


extern volatile IRegion_Info_Type SystemIRegionInfo;


/* ToDo: define the correct core features for the mars */
#define __ECLIC_PRESENT           1                     /*!< Set to 1 if ECLIC is present */
#define __ECLIC_BASEADDR          SystemIRegionInfo.eclic_base          /*!< Set to ECLIC baseaddr of your device */

//#define __ECLIC_INTCTLBITS        3                     /*!< Set to 1 - 8, the number of hardware bits are actually implemented in the clicintctl registers. */
#define __ECLIC_INTNUM            67                    /*!< Set to 1 - 1024, total interrupt number of ECLIC Unit */
#define __SYSTIMER_PRESENT        1                     /*!< Set to 1 if System Timer is present */
#define __SYSTIMER_BASEADDR       SystemIRegionInfo.systimer_base          /*!< Set to SysTimer baseaddr of your device */

#define __CIDU_PRESENT            1 // 0                     /*!< Set to 1 if CIDU is present */
#define __CIDU_BASEADDR           SystemIRegionInfo.idu_base              /*!< Set to cidu baseaddr of your device */


/*!< Set to 0, 1, or 2, 0 not present, 1 single floating point unit present, 2 double floating point unit present */
#if !defined(__riscv_flen)
#define __FPU_PRESENT             0
#elif __riscv_flen == 32
#define __FPU_PRESENT             1
#else
#define __FPU_PRESENT             2
#endif


/* __riscv_bitmanip/__riscv_dsp/__riscv_vector is introduced
 * in nuclei gcc 10.2 when b/p/v extension compiler option is selected.
 * For example:
 * -march=rv32imacb -mabi=ilp32 : __riscv_bitmanip macro will be defined
 * -march=rv32imacp -mabi=ilp32 : __riscv_dsp macro will be defined
 * -march=rv64imacv -mabi=lp64 : __riscv_vector macro will be defined
 */
#if defined(__riscv_bitmanip)
#define __BITMANIP_PRESENT        1                     /*!< Set to 1 if Bitmainpulation extension is present */
#else
#define __BITMANIP_PRESENT        0                     /*!< Set to 1 if Bitmainpulation extension is present */
#endif
#if defined(__riscv_dsp)
#define __DSP_PRESENT             1                     /*!< Set to 1 if Partial SIMD(DSP) extension is present */
#else
#define __DSP_PRESENT             0                     /*!< Set to 1 if Partial SIMD(DSP) extension is present */
#endif
#if defined(__riscv_vector)
#define __VECTOR_PRESENT          1                     /*!< Set to 1 if Vector extension is present */
#else
#define __VECTOR_PRESENT          0                     /*!< Set to 1 if Vector extension is present */
#endif

#define __PMP_PRESENT             1                     /*!< Set to 1 if PMP is present */
#define __PMP_ENTRY_NUM           8                    /*!< Set to 8 or 16, the number of PMP entries */

#define __SPMP_PRESENT            0                     /*!< Set to 1 if SPMP is present */
#define __SPMP_ENTRY_NUM          16                    /*!< Set to 8 or 16, the number of SPMP entries */

#ifndef __TEE_PRESENT
#define __TEE_PRESENT             0                     /*!< Set to 1 if TEE is present */
#endif

#ifndef RUNMODE_CONTROL
#define __ICACHE_PRESENT          1                     /*!< Set to 1 if I-Cache is present */
#define __DCACHE_PRESENT          1                     /*!< Set to 1 if D-Cache is present */
#define __CCM_PRESENT             1                     /*!< Set to 1 if Cache Control and Mantainence Unit is present */
#endif

/* TEE feature depends on PMP */
#if defined(__TEE_PRESENT) && (__TEE_PRESENT == 1)
#if !defined(__PMP_PRESENT) || (__PMP_PRESENT != 1)
#error "__PMP_PRESENT must be defined as 1!"
#endif /* !defined(__PMP_PRESENT) || (__PMP_PRESENT != 1) */
#if !defined(__SPMP_PRESENT) || (__SPMP_PRESENT != 1)
#error "__SPMP_PRESENT must be defined as 1!"
#endif /* !defined(__SPMP_PRESENT) || (__SPMP_PRESENT != 1) */
#endif /* defined(__TEE_PRESENT) && (__TEE_PRESENT == 1) */

#ifndef __INC_INTRINSIC_API
#define __INC_INTRINSIC_API       0                     /*!< Set to 1 if intrinsic api header files need to be included */
#endif

#define __Vendor_SysTickConfig    0                     /*!< Set to 1 if different SysTick Config is used */
#define __Vendor_EXCEPTION        0                     /*!< Set to 1 if vendor exception hander is present */

/** @} */ /* End of group Configuration_of_NMSIS */


/* Define boot hart id */
#ifndef BOOT_HARTID
#define BOOT_HARTID               0                     /*!< Choosen boot hart id in current cluster when in soc system, need to align with the value defined in startup_<Device>.S, should start from 0, taken the mhartid bit 0-7 value */
#endif

#ifndef   __COMPILER_BARRIER
  #define __COMPILER_BARRIER()                   __ASM volatile("":::"memory")
#endif

/************************************************************************************
 * Linker definitions
 ************************************************************************************/
#define _CORE0_ILM_TEXT_SEC              ".text.core0_ilm"

#define _CORE0_DLM_DATA_SEC              ".data.core0_dlm"
#define _CORE0_DLM_BSS_SEC               ".bss.core0_dlm"

#define _CORE1_ILM_TEXT_SEC              ".text.core1_ilm"

#define _CORE1_DLM_DATA_SEC              ".data.core1_dlm"
#define _CORE1_DLM_BSS_SEC               ".bss.core1_dlm"

#define _CMN_RAM0_TEXT_SEC               ".text.cmn_ram0"

#define _CMN_RAM0_DATA_SEC               ".data.cmn_ram0"
#define _CMN_RAM0_BSS_SEC                ".bss.cmn_ram0"

#define _CMN_RAM1_TEXT_SEC               ".text.cmn_ram1"

#define _CMN_RAM1_DATA_SEC               ".data.cmn_ram1"
#define _CMN_RAM1_BSS_SEC                ".bss.cmn_ram1"

#define _CMN_LUNA_RAM_TEXT_SEC           ".text.cmn_luna_ram"

#define _CMN_LUNA_RAM_DATA_SEC           ".data.cmn_luna_ram"
#define _CMN_LUNA_RAM_BSS_SEC            ".bss.cmn_luna_ram"

#define _CMN_PSRAM_TEXT_SEC              ".text.cmn_psram"

#define _CMN_PSRAM_DATA_SEC              ".data.cmn_psram"
#define _CMN_PSRAM_BSS_SEC               ".bss.cmn_psram"

#define _CORE0_ILM_TEXT                  __attribute__ ((section (_CORE0_ILM_TEXT_SEC)))
#define _CORE0_ILM_TEXT_TAG(tag)         __attribute__ ((section (_CORE0_ILM_TEXT_SEC"."#tag)))

#define _CORE0_DLM_DATA                  __attribute__ ((section (_CORE0_DLM_DATA_SEC)))
#define _CORE0_DLM_DATA_TAG(tag)         __attribute__ ((section (_CORE0_DLM_DATA_SEC"."#tag)))
#define _CORE0_DLM_BSS                   __attribute__ ((section (_CORE0_DLM_BSS_SEC)))
#define _CORE0_DLM_BSS_TAG(tag)          __attribute__ ((section (_CORE0_DLM_BSS_SEC"."#tag)))

#define _CORE1_ILM_TEXT                  __attribute__ ((section (_CORE1_ILM_TEXT_SEC)))
#define _CORE1_ILM_TEXT_TAG(tag)         __attribute__ ((section (_CORE1_ILM_TEXT_SEC"."#tag)))

#define _CORE1_DLM_DATA                  __attribute__ ((section (_CORE1_DLM_DATA_SEC)))
#define _CORE1_DLM_DATA_TAG(tag)         __attribute__ ((section (_CORE1_DLM_DATA_SEC"."#tag)))
#define _CORE1_DLM_BSS                   __attribute__ ((section (_CORE1_DLM_BSS_SEC)))
#define _CORE1_DLM_BSS_TAG(tag)          __attribute__ ((section (_CORE1_DLM_BSS_SEC"."#tag)))

#define _CMN_RAM0_TEXT                   __attribute__ ((section (_CMN_RAM0_TEXT_SEC)))
#define _CMN_RAM0_TEXT_TAG(tag)          __attribute__ ((section (_CMN_RAM0_TEXT_SEC"."#tag)))

#define _CMN_RAM0_DATA                   __attribute__ ((section (_CMN_RAM0_DATA_SEC)))
#define _CMN_RAM0_DATA_TAG(tag)          __attribute__ ((section (_CMN_RAM0_DATA_SEC"."#tag)))
#define _CMN_RAM0_BSS                    __attribute__ ((section (_CMN_RAM0_BSS_SEC)))
#define _CMN_RAM0_BSS_TAG(tag)           __attribute__ ((section (_CMN_RAM0_BSS_SEC"."#tag)))

#define _CMN_RAM1_TEXT                   __attribute__ ((section (_CMN_RAM1_TEXT_SEC)))
#define _CMN_RAM1_TEXT_TAG(tag)          __attribute__ ((section (_CMN_RAM1_TEXT_SEC"."#tag)))

#define _CMN_RAM1_DATA                   __attribute__ ((section (_CMN_RAM1_DATA_SEC)))
#define _CMN_RAM1_DATA_TAG(tag)          __attribute__ ((section (_CMN_RAM1_DATA_SEC"."#tag)))
#define _CMN_RAM1_BSS                    __attribute__ ((section (_CMN_RAM1_BSS_SEC)))
#define _CMN_RAM1_BSS_TAG(tag)           __attribute__ ((section (_CMN_RAM1_BSS_SEC"."#tag)))

#define _CMN_LUNA_RAM_TEXT               __attribute__ ((section (_CMN_LUNA_RAM_TEXT_SEC)))
#define _CMN_LUNA_RAM_TEXT_TAG(tag)      __attribute__ ((section (_CMN_LUNA_RAM_TEXT_SEC"."#tag)))

#define _CMN_LUNA_RAM_DATA               __attribute__ ((section (_CMN_LUNA_RAM_DATA_SEC)))
#define _CMN_LUNA_RAM_DATA_TAG(tag)      __attribute__ ((section (_CMN_LUNA_RAM_DATA_SEC"."#tag)))
#define _CMN_LUNA_RAM_BSS                __attribute__ ((section (_CMN_LUNA_RAM_BSS_SEC)))
#define _CMN_LUNA_RAM_BSS_TAG(tag)       __attribute__ ((section (_CMN_LUNA_RAM_BSS_SEC"."#tag)))

#define _CMN_PSRAM_TEXT                  __attribute__ ((section (_CMN_PSRAM_TEXT_SEC)))
#define _CMN_PSRAM_TEXT_TAG(tag)         __attribute__ ((section (_CMN_PSRAM_TEXT_SEC"."#tag)))

#define _CMN_PSRAM_DATA                  __attribute__ ((section (_CMN_PSRAM_DATA_SEC)))
#define _CMN_PSRAM_DATA_TAG(tag)         __attribute__ ((section (_CMN_PSRAM_DATA_SEC"."#tag)))
#define _CMN_PSRAM_BSS                   __attribute__ ((section (_CMN_PSRAM_BSS_SEC)))
#define _CMN_PSRAM_BSS_TAG(tag)          __attribute__ ((section (_CMN_PSRAM_BSS_SEC"."#tag)))

#if (BOOT_HARTID == 0) // Core0
#define _FAST_TEXT                       _CORE0_ILM_TEXT
#define _FAST_TEXT_TAG(tag)              _CORE0_ILM_TEXT_TAG(tag)
#define _FAST_DATA                       _CORE0_DLM_DATA
#define _FAST_DATA_TAG(tag)              _CORE0_DLM_DATA_TAG(tag)
#define _FAST_BSS                        _CORE0_DLM_BSS
#define _FAST_BSS_TAG(tag)               _CORE0_DLM_BSS_TAG(tag)
#else // Core1
#define _FAST_TEXT                       _CORE1_ILM_TEXT
#define _FAST_TEXT_TAG(tag)              _CORE1_ILM_TEXT_TAG(tag)
#define _FAST_DATA                       _CORE1_DLM_DATA
#define _FAST_DATA_TAG(tag)              _CORE1_DLM_DATA_TAG(tag)
#define _FAST_BSS                        _CORE1_DLM_BSS
#define _FAST_BSS_TAG(tag)               _CORE1_DLM_BSS_TAG(tag)
#endif

#define _DMA
#define _DMA_PRAM                         __attribute__((aligned(32)))

#define _FAST_FUNC_RO
#define _FAST_DATA_VI
#define _FAST_DATA_ZI

#ifndef __ASM
#define __ASM                   __asm     /*!< asm keyword for GNU Compiler */
#endif

#ifndef __INLINE
#define __INLINE                inline    /*!< inline keyword for GNU Compiler */
#endif

#ifndef __ALWAYS_STATIC_INLINE
#define __ALWAYS_STATIC_INLINE  __attribute__((always_inline)) static inline
#endif

#ifndef __STATIC_INLINE
#define __STATIC_INLINE         static inline
#endif

#define NMI_EXPn                (-2)      /* NMI Exception */

// IC_BOARD == 1 ---> ASIC
// IC_BOARD == 0 ---> FPGA

#if IC_BOARD // ASIC

#define DEF_MAIN_FREQUENCE    (300000000) // 300 MHz
//#define DEF_MAIN_FREQUENCE    (24000000) // 24 MHz

static inline uint32_t CPUFREQ() {
    extern uint32_t CRM_GetApFreq();
    return CRM_GetApFreq();
}

static inline uint32_t HCLKFREQ() {
    extern uint32_t CRM_GetApahbFreq();
    return CRM_GetApahbFreq();
}

static inline uint32_t PCLKFREQ() {
    extern uint32_t CRM_GetApperiapbFreq();
    return CRM_GetApperiapbFreq();
}

#else // FPGA

#define DEF_MAIN_FREQUENCE    (24000000) // 24MHZ

static inline uint32_t CPUFREQ() {
    return (DEF_MAIN_FREQUENCE);
}

static inline uint32_t HCLKFREQ() {
    return (DEF_MAIN_FREQUENCE);
}

static inline uint32_t PCLKFREQ() {
    return (DEF_MAIN_FREQUENCE);
}

#endif // IC_BOARD

/************************************************************************************
 * GI(Global Interrupt) and IRQ vector inline functions
 ************************************************************************************/
//The greater value of level, the higher priority
#define MAX_INTERRUPT_PRIORITY_RVAL     3
#define MID_INTERRUPT_PRIORITY          2
#define DEF_INTERRUPT_PRIORITY          0
#define DEF_INTERRUPT_LEVEL             0

// Is Global Interrupt enabled? 0 = disabled, 1 = enabled
static inline uint8_t GINT_enabled()
{
    //TODO:
    //uint32_t ret = __get_PRIMASK(); // based on PRIMASK
    //return (ret ? 0 : 1);
    uint32_t ret = 0;//__get_BASEPRI(); // based on BASEPRI
    return (ret == MAX_INTERRUPT_PRIORITY_RVAL ? 0 : 1);
}

// Enable GINT
static inline void enable_GINT()
{
	__RV_CSR_SET(CSR_MSTATUS, MSTATUS_MIE);
}

// Disable GINT
static inline void disable_GINT()
{
	__RV_CSR_CLEAR(CSR_MSTATUS, MSTATUS_MIE);
}

// ISR function prototype
typedef void (*ISR)(void);

// Register ISR into Interrupt Vector Table
void register_ISR(uint32_t irq_no, ISR isr, ISR* isr_old);


static inline uint8_t IRQ_enabled(uint32_t irq_no)
{
    return (uint8_t)ECLIC_GetEnableIRQ(irq_no);
}

static inline void enable_IRQ(uint32_t irq_no)
{
	ECLIC_EnableIRQ(irq_no);
}

static inline void disable_IRQ(uint32_t irq_no)
{
	ECLIC_DisableIRQ(irq_no);
}

static inline void clear_IRQ(uint32_t irq_no)
{
	ECLIC_ClearPendingIRQ(irq_no);
}

void non_cacheable_region_enable(uint32_t base_addr, uint32_t len);

void non_cacheable_region_disable(void);

extern void mpu_init( void );

{% for cmn_dma in Input.Item.cmn_dma_sel0 %}
{{bsp.Device_CMN_DMA_HS_Define_Macro(cmn_dma[1], 0, cmn_dma[0])}}
{%- endfor %}

{% for cmn_dma in Input.Item.cmn_dma_sel1 %}
{{bsp.Device_CMN_DMA_HS_Define_Macro(cmn_dma[1], 1, cmn_dma[0])}}
{%- endfor %}

{% for gp_dma in Input.Item.gp_dma_sel0 %}
{{bsp.Device_GP_DMA_HS_Define_Macro(gp_dma[1], 0, gp_dma[0])}}
{%- endfor %}

{% for gp_dma in Input.Item.gp_dma_sel1 %}
{{bsp.Device_GP_DMA_HS_Define_Macro(gp_dma[1], 1, gp_dma[0])}}
{%- endfor %}

{{cmn.H_File_Header_Macro_Filter_End(Input.Target_Name)}}