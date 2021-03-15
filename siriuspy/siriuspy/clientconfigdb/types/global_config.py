"""AS Global configuration."""
from copy import deepcopy as _dcopy

from siriuspy.pwrsupply.csdev import DEFAULT_WFM_FBP as \
    _DEFAULT_WFM_FBP
from siriuspy.pwrsupply.csdev import DEFAULT_WFM_OTHERS as \
    _DEFAULT_WFM_OTHERS


_OFF = 0
_ON = 1
_SLOWREF = 0


def get_dict():
    """Return configuration type dictionary."""
    module_name = __name__.split('.')[-1]
    _dict = {
        'config_type_name': module_name,
        'value': _dcopy(_template_dict),
        'check': False,
    }
    return _dict


# When using this type of configuration to set the machine,
# the list of PVs should be processed in the same order they are stored
# in the configuration. The second numeric parameter in the pair is the
# delay [s] the client should wait before setting the next PV.


_pvs_li_egunmod = [
    ['LI-01:EG-BiasPS:switch', 0, 0],
    ['LI-01:EG-BiasPS:voltoutsoft', -60.0, 0.0],  # [V]
    ['LI-01:EG-FilaPS:switch', 0, 0],
    ['LI-01:EG-HVPS:currentoutsoft', 0.003, 0.0],  # [mA]
    ['LI-01:EG-HVPS:enable', 0, 0.0],
    ['LI-01:EG-PulsePS:multiselect', 0, 0.0],
    ['LI-01:EG-PulsePS:multiswitch', 0, 0.0],
    ['LI-01:EG-PulsePS:singleselect', 0, 0.0],
    ['LI-01:EG-PulsePS:singleswitch', 0, 0.0],
    ['LI-01:EG-PulsePS:poweroutsoft', 0.0, 0.0],  # [V]
    ['LI-01:PU-Modltr-1:WRITE_I', 100.0, 0.0],  # [mA]
    ['LI-01:PU-Modltr-2:WRITE_I', 100.0, 0.0],  # [mA]
    ['LI-01:PU-Modltr-1:WRITE_V', 0.0, 0.0],  # [kV]
    ['LI-01:PU-Modltr-2:WRITE_V', 0.0, 0.0],  # [kV]
    ]


_pvs_li_llrf = [
    ['LA-RF:LLRF:BUN1:SET_STREAM', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH1_DELAY', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH2_DELAY', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH7_DELAY', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH8_DELAY', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_TRIGGER_DELAY', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_AMP', 0.0, 0.0],  # [%]
    ['LA-RF:LLRF:BUN1:SET_PHASE', 0.0, 0.0],  # [deg]
    ['LA-RF:LLRF:BUN1:SET_KP', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_KI', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH1_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH2_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH7_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH8_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_FBLOOP_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_FBLOOP_AMP_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH1_ADT', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH2_ADT', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH7_ADT', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH8_ADT', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_VM_ADT', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH1_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH2_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH7_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH8_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_PID_KP', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_PID_KI', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_STREAM', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH1_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH2_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH3_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH4_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH5_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH6_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH7_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH8_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH9_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_TRIGGER_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_AMP', 0.0, 0.0],  # [%]
    ['LA-RF:LLRF:KLY1:SET_PHASE', 0.0, 0.0],  # [deg]
    ['LA-RF:LLRF:KLY1:SET_REFL_POWER_LIMIT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_KP', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_KI', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_FBLOOP_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_FBLOOP_AMP_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH1_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH2_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH3_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH4_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH5_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH6_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH7_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH8_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH9_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH1_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH2_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH3_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH4_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH5_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH6_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH7_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH8_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_VM_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH1_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH2_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH3_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH4_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH5_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH6_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH7_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH8_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_CH9_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_SHIF_MOTOR_ANGLE', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_STREAM', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH1_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH2_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH3_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH4_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH5_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH6_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH7_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH8_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH9_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_TRIGGER_DELAY', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_AMP', 0.0, 0.0],  # [%]
    ['LA-RF:LLRF:KLY2:SET_PHASE', 0.0, 0.0],  # [deg]
    ['LA-RF:LLRF:KLY2:SET_REFL_POWER_LIMIT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_KP', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_KI', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_FBLOOP_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_FBLOOP_AMP_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH1_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH2_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH3_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH4_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH5_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH6_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH7_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH8_PHASE_CORR', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH1_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH2_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH3_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH4_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH5_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH6_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH7_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH8_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_VM_ADT', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH1_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH2_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH3_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH4_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH5_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH6_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH7_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH8_ATT', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_CH9_ATT', 0.0, 0.0],
    ]


_pvs_as_ti = [
    # Clocks
    ['AS-RaMO:TI-EVG:Clk0MuxDiv-SP', 0, 0.0],
    ['AS-RaMO:TI-EVG:Clk0MuxEnbl-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:Clk1MuxDiv-SP', 0, 0.0],
    ['AS-RaMO:TI-EVG:Clk1MuxEnbl-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:Clk2MuxDiv-SP', 0, 0.0],
    ['AS-RaMO:TI-EVG:Clk2MuxEnbl-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:Clk3MuxDiv-SP', 0, 0.0],
    ['AS-RaMO:TI-EVG:Clk3MuxEnbl-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:Clk4MuxDiv-SP', 0, 0.0],
    ['AS-RaMO:TI-EVG:Clk4MuxEnbl-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:Clk5MuxDiv-SP', 0, 0.0],
    ['AS-RaMO:TI-EVG:Clk5MuxEnbl-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:Clk6MuxDiv-SP', 0, 0.0],
    ['AS-RaMO:TI-EVG:Clk6MuxEnbl-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:Clk7MuxDiv-SP', 0, 0.0],
    ['AS-RaMO:TI-EVG:Clk7MuxEnbl-Sel', 0, 0.0],

    # Events
    ['AS-RaMO:TI-EVG:CplSIDelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:CplSIDelayType-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:CplSIMode-Sel', 0, 0.0],

    ['AS-RaMO:TI-EVG:CycleDelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:CycleDelayType-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:CycleMode-Sel', 0, 0.0],

    ['AS-RaMO:TI-EVG:DigBODelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:DigBODelayType-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:DigBOMode-Sel', 0, 0.0],

    ['AS-RaMO:TI-EVG:DigLIDelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:DigLIDelayType-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:DigLIMode-Sel', 0, 0.0],

    ['AS-RaMO:TI-EVG:DigSIDelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:DigSIDelayType-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:DigSIMode-Sel', 0, 0.0],

    ['AS-RaMO:TI-EVG:DigTBDelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:DigTBDelayType-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:DigTBMode-Sel', 0, 0.0],

    ['AS-RaMO:TI-EVG:DigTSDelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:DigTSDelayType-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:DigTSMode-Sel', 0, 0.0],

    ['AS-RaMO:TI-EVG:InjBODelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:InjBODelayType-Sel', 0, 0.0],
    # ['AS-RaMO:TI-EVG:InjBOMode-Sel', 0, 0.0],

    ['AS-RaMO:TI-EVG:InjSIDelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:InjSIDelayType-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:InjSIMode-Sel', 0, 0.0],

    ['AS-RaMO:TI-EVG:LinacDelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:LinacDelayType-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:LinacMode-Sel', 0, 0.0],

    ['AS-RaMO:TI-EVG:MigSIDelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:MigSIDelayType-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:MigSIMode-Sel', 0, 0.0],

    ['AS-RaMO:TI-EVG:OrbBODelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:OrbBODelayType-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:OrbBOMode-Sel', 0, 0.0],

    ['AS-RaMO:TI-EVG:OrbSIDelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:OrbSIDelayType-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:OrbSIMode-Sel', 0, 0.0],

    ['AS-RaMO:TI-EVG:RmpBODelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:RmpBODelayType-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:RmpBOMode-Sel', 0, 0.0],

    ['AS-RaMO:TI-EVG:StudyDelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:StudyDelayType-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:StudyMode-Sel', 0, 0.0],

    ['AS-RaMO:TI-EVG:TunSIDelayRaw-SP', 0, 0],
    ['AS-RaMO:TI-EVG:TunSIDelayType-Sel', 0, 0.0],
    ['AS-RaMO:TI-EVG:TunSIMode-Sel', 0, 0.0],

    # Triggers
    ['AS-Fam:TI-Scrn-TBBO:DelayRaw-SP', 0, 0],
    ['AS-Fam:TI-Scrn-TBBO:Duration-SP', 0, 0.0],  # [us]
    ['AS-Fam:TI-Scrn-TBBO:NrPulses-SP', 0, 0.0],
    ['AS-Fam:TI-Scrn-TBBO:Polarity-Sel', 0, 0.0],
    ['AS-Fam:TI-Scrn-TBBO:RFDelayType-Sel', 0, 0.0],
    ['AS-Fam:TI-Scrn-TBBO:Src-Sel', 0, 0.0],
    ['AS-Fam:TI-Scrn-TBBO:State-Sel', 0, 0.0],
    ['AS-Fam:TI-Scrn-TBBO:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['AS-Fam:TI-Scrn-TBBO:LowLvlLock-Sel', 0, 0.0],

    ['AS-Glob:TI-FCT:DelayRaw-SP', 0, 0],
    ['AS-Glob:TI-FCT:Duration-SP', 0, 0.0],  # [us]
    ['AS-Glob:TI-FCT:NrPulses-SP', 0, 0.0],
    ['AS-Glob:TI-FCT:Polarity-Sel', 0, 0.0],
    ['AS-Glob:TI-FCT:RFDelayType-Sel', 0, 0.0],
    ['AS-Glob:TI-FCT:Src-Sel', 0, 0.0],
    ['AS-Glob:TI-FCT:State-Sel', 0, 0.0],
    ['AS-Glob:TI-FCT:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['AS-Glob:TI-FCT:LowLvlLock-Sel', 0, 0.0],

    ['AS-Glob:TI-FillPtrnMon:DelayRaw-SP', 0, 0],
    ['AS-Glob:TI-FillPtrnMon:Duration-SP', 0, 0.0],  # [us]
    ['AS-Glob:TI-FillPtrnMon:NrPulses-SP', 0, 0.0],
    ['AS-Glob:TI-FillPtrnMon:Polarity-Sel', 0, 0.0],
    ['AS-Glob:TI-FillPtrnMon:RFDelayType-Sel', 0, 0.0],
    ['AS-Glob:TI-FillPtrnMon:Src-Sel', 0, 0.0],
    ['AS-Glob:TI-FillPtrnMon:State-Sel', 0, 0.0],
    ['AS-Glob:TI-FillPtrnMon:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['AS-Glob:TI-FillPtrnMon:LowLvlLock-Sel', 0, 0.0],

    ['AS-Glob:TI-Osc-EjeBO:DelayRaw-SP', 0, 0],
    ['AS-Glob:TI-Osc-EjeBO:Duration-SP', 0, 0.0],  # [us]
    ['AS-Glob:TI-Osc-EjeBO:NrPulses-SP', 0, 0.0],
    ['AS-Glob:TI-Osc-EjeBO:Polarity-Sel', 0, 0.0],
    ['AS-Glob:TI-Osc-EjeBO:RFDelayType-Sel', 0, 0.0],
    ['AS-Glob:TI-Osc-EjeBO:Src-Sel', 0, 0.0],
    ['AS-Glob:TI-Osc-EjeBO:State-Sel', 0, 0.0],
    ['AS-Glob:TI-Osc-EjeBO:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['AS-Glob:TI-Osc-EjeBO:LowLvlLock-Sel', 0, 0.0],

    ['AS-Glob:TI-Osc-InjBO:DelayRaw-SP', 0, 0],
    ['AS-Glob:TI-Osc-InjBO:Duration-SP', 0, 0.0],  # [us]
    ['AS-Glob:TI-Osc-InjBO:NrPulses-SP', 0, 0.0],
    ['AS-Glob:TI-Osc-InjBO:Polarity-Sel', 0, 0.0],
    ['AS-Glob:TI-Osc-InjBO:Src-Sel', 0, 0.0],
    ['AS-Glob:TI-Osc-InjBO:State-Sel', 0, 0.0],
    ['AS-Glob:TI-Osc-InjBO:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['AS-Glob:TI-Osc-InjBO:LowLvlLock-Sel', 0, 0.0],

    ['AS-Glob:TI-Osc-InjSI:DelayRaw-SP', 0, 0],
    ['AS-Glob:TI-Osc-InjSI:Duration-SP', 0, 0.0],  # [us]
    ['AS-Glob:TI-Osc-InjSI:NrPulses-SP', 0, 0.0],
    ['AS-Glob:TI-Osc-InjSI:Polarity-Sel', 0, 0.0],
    ['AS-Glob:TI-Osc-InjSI:Src-Sel', 0, 0.0],
    ['AS-Glob:TI-Osc-InjSI:State-Sel', 0, 0.0],
    ['AS-Glob:TI-Osc-InjSI:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['AS-Glob:TI-Osc-InjSI:LowLvlLock-Sel', 0, 0.0],

    ['BO-01D:TI-InjKckr:DelayRaw-SP', 0, 0],
    ['BO-01D:TI-InjKckr:Duration-SP', 0, 0.0],  # [us]
    ['BO-01D:TI-InjKckr:NrPulses-SP', 0, 0.0],
    ['BO-01D:TI-InjKckr:Polarity-Sel', 0, 0.0],
    ['BO-01D:TI-InjKckr:Src-Sel', 0, 0.0],
    ['BO-01D:TI-InjKckr:State-Sel', 0, 0.0],
    ['BO-01D:TI-InjKckr:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['BO-01D:TI-InjKckr:LowLvlLock-Sel', 0, 0.0],

    ['BO-35D:TI-DCCT:DelayRaw-SP', 0, 0],
    ['BO-35D:TI-DCCT:Duration-SP', 0, 0.0],  # [us]
    ['BO-35D:TI-DCCT:NrPulses-SP', 0, 0.0],
    ['BO-35D:TI-DCCT:Polarity-Sel', 0, 0.0],
    ['BO-35D:TI-DCCT:RFDelayType-Sel', 0, 0.0],
    ['BO-35D:TI-DCCT:Src-Sel', 0, 0.0],
    ['BO-35D:TI-DCCT:State-Sel', 0, 0.0],
    ['BO-35D:TI-DCCT:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['BO-35D:TI-DCCT:LowLvlLock-Sel', 0, 0.0],

    ['BO-48D:TI-EjeKckr:DelayRaw-SP', 0, 0],
    ['BO-48D:TI-EjeKckr:Duration-SP', 0, 0.0],  # [us]
    ['BO-48D:TI-EjeKckr:NrPulses-SP', 0, 0.0],
    ['BO-48D:TI-EjeKckr:Polarity-Sel', 0, 0.0],
    ['BO-48D:TI-EjeKckr:RFDelayType-Sel', 0, 0.0],
    ['BO-48D:TI-EjeKckr:Src-Sel', 0, 0.0],
    ['BO-48D:TI-EjeKckr:State-Sel', 0, 0.0],
    ['BO-48D:TI-EjeKckr:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['BO-48D:TI-EjeKckr:LowLvlLock-Sel', 0, 0.0],

    ['BO-50U:TI-VLightCam:DelayRaw-SP', 0, 0],
    ['BO-50U:TI-VLightCam:Duration-SP', 0, 0.0],  # [us]
    ['BO-50U:TI-VLightCam:NrPulses-SP', 0, 0.0],
    ['BO-50U:TI-VLightCam:Polarity-Sel', 0, 0.0],
    ['BO-50U:TI-VLightCam:RFDelayType-Sel', 0, 0.0],
    ['BO-50U:TI-VLightCam:Src-Sel', 0, 0.0],
    ['BO-50U:TI-VLightCam:State-Sel', 0, 0.0],
    ['BO-50U:TI-VLightCam:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['BO-50U:TI-VLightCam:LowLvlLock-Sel', 0, 0.0],

    ['BO-Fam:TI-BPM:DelayRaw-SP', 0, 0],
    ['BO-Fam:TI-BPM:Duration-SP', 0, 0.0],  # [us]
    ['BO-Fam:TI-BPM:NrPulses-SP', 0, 0.0],
    ['BO-Fam:TI-BPM:Polarity-Sel', 0, 0.0],
    ['BO-Fam:TI-BPM:Src-Sel', 0, 0.0],
    ['BO-Fam:TI-BPM:State-Sel', 0, 0.0],
    ['BO-Fam:TI-BPM:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['BO-Fam:TI-BPM:LowLvlLock-Sel', 0, 0.0],

    ['BO-Glob:TI-LLRF-PsMtn:DelayRaw-SP', 0, 0],
    ['BO-Glob:TI-LLRF-PsMtn:Duration-SP', 0, 0.0],  # [us]
    ['BO-Glob:TI-LLRF-PsMtn:NrPulses-SP', 0, 0.0],
    ['BO-Glob:TI-LLRF-PsMtn:Polarity-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-PsMtn:Src-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-PsMtn:State-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-PsMtn:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['BO-Glob:TI-LLRF-PsMtn:LowLvlLock-Sel', 0, 0.0],

    ['BO-Glob:TI-LLRF-Rmp:DelayRaw-SP', 0, 0],
    ['BO-Glob:TI-LLRF-Rmp:Duration-SP', 0, 0.0],  # [us]
    ['BO-Glob:TI-LLRF-Rmp:NrPulses-SP', 0, 0.0],
    ['BO-Glob:TI-LLRF-Rmp:Polarity-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-Rmp:Src-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-Rmp:State-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-Rmp:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['BO-Glob:TI-LLRF-Rmp:LowLvlLock-Sel', 0, 0.0],

    ['BO-Glob:TI-Mags-Corrs:DelayRaw-SP', 0, 0],
    ['BO-Glob:TI-Mags-Corrs:Duration-SP', 0, 0.0],  # [us]
    ['BO-Glob:TI-Mags-Corrs:NrPulses-SP', 0, 0.0],
    ['BO-Glob:TI-Mags-Corrs:Polarity-Sel', 0, 0.0],
    ['BO-Glob:TI-Mags-Corrs:Src-Sel', 0, 0.0],
    # ['BO-Glob:TI-Mags-Corrs:State-Sel', 0, 0.0],
    ['BO-Glob:TI-Mags-Corrs:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['BO-Glob:TI-Mags-Corrs:LowLvlLock-Sel', 0, 0.0],

    ['BO-Glob:TI-Mags-Fams:DelayRaw-SP', 0, 0],
    ['BO-Glob:TI-Mags-Fams:Duration-SP', 0, 0.0],  # [us]
    ['BO-Glob:TI-Mags-Fams:NrPulses-SP', 0, 0.0],
    ['BO-Glob:TI-Mags-Fams:Polarity-Sel', 0, 0.0],
    ['BO-Glob:TI-Mags-Fams:Src-Sel', 0, 0.0],
    # ['BO-Glob:TI-Mags-Fams:State-Sel', 0, 0.0],
    ['BO-Glob:TI-Mags-Fams:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['BO-Glob:TI-Mags-Fams:LowLvlLock-Sel', 0, 0.0],

    ['BO-Glob:TI-TuneProc:DelayRaw-SP', 0, 0],
    ['BO-Glob:TI-TuneProc:Duration-SP', 0, 0.0],  # [us]
    ['BO-Glob:TI-TuneProc:NrPulses-SP', 0, 0.0],
    ['BO-Glob:TI-TuneProc:Polarity-Sel', 0, 0.0],
    ['BO-Glob:TI-TuneProc:RFDelayType-Sel', 0, 0.0],
    ['BO-Glob:TI-TuneProc:Src-Sel', 0, 0.0],
    ['BO-Glob:TI-TuneProc:State-Sel', 0, 0.0],
    ['BO-Glob:TI-TuneProc:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['BO-Glob:TI-TuneProc:LowLvlLock-Sel', 0, 0.0],

    ['LI-01:TI-Osc-Modltr:DelayRaw-SP', 0, 0],
    ['LI-01:TI-Osc-Modltr:Duration-SP', 0, 0.0],  # [us]
    ['LI-01:TI-Osc-Modltr:NrPulses-SP', 0, 0.0],
    ['LI-01:TI-Osc-Modltr:Polarity-Sel', 0, 0.0],
    ['LI-01:TI-Osc-Modltr:Src-Sel', 0, 0.0],
    ['LI-01:TI-Osc-Modltr:State-Sel', 0, 0.0],
    ['LI-01:TI-Osc-Modltr:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['LI-01:TI-Osc-Modltr:LowLvlLock-Sel', 0, 0.0],

    ['LI-01:TI-EGun-MultBun:DelayRaw-SP', 0, 0],
    ['LI-01:TI-EGun-MultBun:Duration-SP', 0, 0.0],  # [us]
    ['LI-01:TI-EGun-MultBun:NrPulses-SP', 0, 0.0],
    ['LI-01:TI-EGun-MultBun:Polarity-Sel', 0, 0.0],
    ['LI-01:TI-EGun-MultBun:RFDelayType-Sel', 0, 0.0],
    ['LI-01:TI-EGun-MultBun:Src-Sel', 0, 0.0],
    ['LI-01:TI-EGun-MultBun:State-Sel', 0, 0.0],
    ['LI-01:TI-EGun-MultBun:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['LI-01:TI-EGun-MultBun:LowLvlLock-Sel', 0, 0.0],

    ['LI-01:TI-EGun-MultBunPre:DelayRaw-SP', 0, 0],
    ['LI-01:TI-EGun-MultBunPre:Duration-SP', 0, 0.0],  # [us]
    ['LI-01:TI-EGun-MultBunPre:NrPulses-SP', 0, 0.0],
    ['LI-01:TI-EGun-MultBunPre:Polarity-Sel', 0, 0.0],
    ['LI-01:TI-EGun-MultBunPre:RFDelayType-Sel', 0, 0.0],
    ['LI-01:TI-EGun-MultBunPre:Src-Sel', 0, 0.0],
    ['LI-01:TI-EGun-MultBunPre:State-Sel', 0, 0.0],
    ['LI-01:TI-EGun-MultBunPre:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['LI-01:TI-EGun-MultBunPre:LowLvlLock-Sel', 0, 0.0],

    ['LI-01:TI-EGun-SglBun:DelayRaw-SP', 0, 0],
    ['LI-01:TI-EGun-SglBun:Duration-SP', 0, 0.0],  # [us]
    ['LI-01:TI-EGun-SglBun:NrPulses-SP', 0, 0.0],
    ['LI-01:TI-EGun-SglBun:Polarity-Sel', 0, 0.0],
    ['LI-01:TI-EGun-SglBun:RFDelayType-Sel', 0, 0.0],
    ['LI-01:TI-EGun-SglBun:Src-Sel', 0, 0.0],
    ['LI-01:TI-EGun-SglBun:State-Sel', 0, 0.0],
    ['LI-01:TI-EGun-SglBun:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['LI-01:TI-EGun-SglBun:LowLvlLock-Sel', 0, 0.0],

    ['LI-01:TI-Modltr-1:DelayRaw-SP', 0, 0],
    ['LI-01:TI-Modltr-1:Duration-SP', 0, 0.0],  # [us]
    ['LI-01:TI-Modltr-1:NrPulses-SP', 0, 0.0],
    ['LI-01:TI-Modltr-1:Polarity-Sel', 0, 0.0],
    ['LI-01:TI-Modltr-1:Src-Sel', 0, 0.0],
    ['LI-01:TI-Modltr-1:State-Sel', 0, 0.0],
    ['LI-01:TI-Modltr-1:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['LI-01:TI-Modltr-1:LowLvlLock-Sel', 0, 0.0],

    ['LI-01:TI-Modltr-2:DelayRaw-SP', 0, 0],
    ['LI-01:TI-Modltr-2:Duration-SP', 0, 0.0],  # [us]
    ['LI-01:TI-Modltr-2:NrPulses-SP', 0, 0.0],
    ['LI-01:TI-Modltr-2:Polarity-Sel', 0, 0.0],
    ['LI-01:TI-Modltr-2:Src-Sel', 0, 0.0],
    ['LI-01:TI-Modltr-2:State-Sel', 0, 0.0],
    ['LI-01:TI-Modltr-2:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['LI-01:TI-Modltr-2:LowLvlLock-Sel', 0, 0.0],

    ['LI-Fam:TI-BPM:DelayRaw-SP', 0, 0],
    ['LI-Fam:TI-BPM:Duration-SP', 0, 0.0],  # [us]
    ['LI-Fam:TI-BPM:NrPulses-SP', 0, 0.0],
    ['LI-Fam:TI-BPM:Polarity-Sel', 0, 0.0],
    ['LI-Fam:TI-BPM:RFDelayType-Sel', 0, 0.0],
    ['LI-Fam:TI-BPM:Src-Sel', 0, 0.0],
    ['LI-Fam:TI-BPM:State-Sel', 0, 0.0],
    ['LI-Fam:TI-BPM:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['LI-Fam:TI-BPM:LowLvlLock-Sel', 0, 0.0],

    ['LI-Fam:TI-ICT:DelayRaw-SP', 0, 0],
    ['LI-Fam:TI-ICT:Duration-SP', 0, 0.0],  # [us]
    ['LI-Fam:TI-ICT:NrPulses-SP', 0, 0.0],
    ['LI-Fam:TI-ICT:Polarity-Sel', 0, 0.0],
    ['LI-Fam:TI-ICT:RFDelayType-Sel', 0, 0.0],
    ['LI-Fam:TI-ICT:Src-Sel', 0, 0.0],
    ['LI-Fam:TI-ICT:State-Sel', 0, 0.0],
    ['LI-Fam:TI-ICT:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['LI-Fam:TI-ICT:LowLvlLock-Sel', 0, 0.0],

    ['LI-Fam:TI-Scrn:DelayRaw-SP', 0, 0],
    ['LI-Fam:TI-Scrn:Duration-SP', 0, 0.0],  # [us]
    ['LI-Fam:TI-Scrn:NrPulses-SP', 0, 0.0],
    ['LI-Fam:TI-Scrn:Polarity-Sel', 0, 0.0],
    ['LI-Fam:TI-Scrn:RFDelayType-Sel', 0, 0.0],
    ['LI-Fam:TI-Scrn:Src-Sel', 0, 0.0],
    ['LI-Fam:TI-Scrn:State-Sel', 0, 0.0],
    ['LI-Fam:TI-Scrn:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['LI-Fam:TI-Scrn:LowLvlLock-Sel', 0, 0.0],

    ['LI-Glob:TI-LLRF-Kly1:DelayRaw-SP', 0, 0],
    ['LI-Glob:TI-LLRF-Kly1:Duration-SP', 0, 0.0],  # [us]
    ['LI-Glob:TI-LLRF-Kly1:NrPulses-SP', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly1:Polarity-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly1:Src-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly1:State-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly1:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['LI-Glob:TI-LLRF-Kly1:LowLvlLock-Sel', 0, 0.0],

    ['LI-Glob:TI-LLRF-Kly2:DelayRaw-SP', 0, 0],
    ['LI-Glob:TI-LLRF-Kly2:Duration-SP', 0, 0.0],  # [us]
    ['LI-Glob:TI-LLRF-Kly2:NrPulses-SP', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly2:Polarity-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly2:Src-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly2:State-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly2:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['LI-Glob:TI-LLRF-Kly2:LowLvlLock-Sel', 0, 0.0],

    ['LI-Glob:TI-LLRF-SHB:DelayRaw-SP', 0, 0],
    ['LI-Glob:TI-LLRF-SHB:Duration-SP', 0, 0.0],  # [us]
    ['LI-Glob:TI-LLRF-SHB:NrPulses-SP', 0, 0.0],
    ['LI-Glob:TI-LLRF-SHB:Polarity-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-SHB:Src-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-SHB:State-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-SHB:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['LI-Glob:TI-LLRF-SHB:LowLvlLock-Sel', 0, 0.0],

    ['LI-Glob:TI-SSAmp-Kly1:DelayRaw-SP', 0, 0],
    ['LI-Glob:TI-SSAmp-Kly1:Duration-SP', 0, 0.0],  # [us]
    ['LI-Glob:TI-SSAmp-Kly1:NrPulses-SP', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly1:Polarity-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly1:Src-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly1:State-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly1:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['LI-Glob:TI-SSAmp-Kly1:LowLvlLock-Sel', 0, 0.0],

    ['LI-Glob:TI-SSAmp-Kly2:DelayRaw-SP', 0, 0],
    ['LI-Glob:TI-SSAmp-Kly2:Duration-SP', 0, 0.0],  # [us]
    ['LI-Glob:TI-SSAmp-Kly2:NrPulses-SP', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly2:Polarity-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly2:Src-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly2:State-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly2:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['LI-Glob:TI-SSAmp-Kly2:LowLvlLock-Sel', 0, 0.0],

    ['LI-Glob:TI-SSAmp-SHB:DelayRaw-SP', 0, 0],
    ['LI-Glob:TI-SSAmp-SHB:Duration-SP', 0, 0.0],  # [us]
    ['LI-Glob:TI-SSAmp-SHB:NrPulses-SP', 0, 0.0],
    ['LI-Glob:TI-SSAmp-SHB:Polarity-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-SHB:Src-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-SHB:State-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-SHB:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['LI-Glob:TI-SSAmp-SHB:LowLvlLock-Sel', 0, 0.0],

    ['SI-01SA:TI-InjDpKckr:DelayRaw-SP', 0, 0],
    ['SI-01SA:TI-InjDpKckr:Duration-SP', 0, 0.0],  # [us]
    ['SI-01SA:TI-InjDpKckr:NrPulses-SP', 0, 0.0],
    ['SI-01SA:TI-InjDpKckr:Polarity-Sel', 0, 0.0],
    ['SI-01SA:TI-InjDpKckr:Src-Sel', 0, 0.0],
    ['SI-01SA:TI-InjDpKckr:State-Sel', 0, 0.0],
    ['SI-01SA:TI-InjDpKckr:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-01SA:TI-InjDpKckr:LowLvlLock-Sel', 0, 0.0],

    ['SI-01SA:TI-InjNLKckr:DelayRaw-SP', 0, 0],
    ['SI-01SA:TI-InjNLKckr:Duration-SP', 0, 0.0],  # [us]
    ['SI-01SA:TI-InjNLKckr:NrPulses-SP', 0, 0.0],
    ['SI-01SA:TI-InjNLKckr:Polarity-Sel', 0, 0.0],
    ['SI-01SA:TI-InjNLKckr:Src-Sel', 0, 0.0],
    ['SI-01SA:TI-InjNLKckr:State-Sel', 0, 0.0],
    ['SI-01SA:TI-InjNLKckr:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-01SA:TI-InjNLKckr:LowLvlLock-Sel', 0, 0.0],

    ['SI-01SA:TI-PingH:DelayRaw-SP', 0, 0],
    ['SI-01SA:TI-PingH:Duration-SP', 0, 0.0],  # [us]
    ['SI-01SA:TI-PingH:NrPulses-SP', 0, 0.0],
    ['SI-01SA:TI-PingH:Polarity-Sel', 0, 0.0],
    ['SI-01SA:TI-PingH:Src-Sel', 0, 0.0],
    ['SI-01SA:TI-PingH:State-Sel', 0, 0.0],
    ['SI-01SA:TI-PingH:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-01SA:TI-PingH:LowLvlLock-Sel', 0, 0.0],

    ['SI-13C4:TI-DCCT:DelayRaw-SP', 0, 0],
    ['SI-13C4:TI-DCCT:Duration-SP', 0, 0.0],  # [us]
    ['SI-13C4:TI-DCCT:NrPulses-SP', 0, 0.0],
    ['SI-13C4:TI-DCCT:Polarity-Sel', 0, 0.0],
    ['SI-13C4:TI-DCCT:RFDelayType-Sel', 0, 0.0],
    ['SI-13C4:TI-DCCT:Src-Sel', 0, 0.0],
    ['SI-13C4:TI-DCCT:State-Sel', 0, 0.0],
    ['SI-13C4:TI-DCCT:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-13C4:TI-DCCT:LowLvlLock-Sel', 0, 0.0],

    ['SI-14C4:TI-DCCT:DelayRaw-SP', 0, 0],
    ['SI-14C4:TI-DCCT:Duration-SP', 0, 0.0],  # [us]
    ['SI-14C4:TI-DCCT:NrPulses-SP', 0, 0.0],
    ['SI-14C4:TI-DCCT:Polarity-Sel', 0, 0.0],
    ['SI-14C4:TI-DCCT:RFDelayType-Sel', 0, 0.0],
    ['SI-14C4:TI-DCCT:Src-Sel', 0, 0.0],
    ['SI-14C4:TI-DCCT:State-Sel', 0, 0.0],
    ['SI-14C4:TI-DCCT:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-14C4:TI-DCCT:LowLvlLock-Sel', 0, 0.0],

    ['SI-19C4:TI-PingV:DelayRaw-SP', 0, 0],
    ['SI-19C4:TI-PingV:Duration-SP', 0, 0.0],  # [us]
    ['SI-19C4:TI-PingV:NrPulses-SP', 0, 0.0],
    ['SI-19C4:TI-PingV:Polarity-Sel', 0, 0.0],
    ['SI-19C4:TI-PingV:RFDelayType-Sel', 0, 0.0],
    ['SI-19C4:TI-PingV:Src-Sel', 0, 0.0],
    ['SI-19C4:TI-PingV:State-Sel', 0, 0.0],
    ['SI-19C4:TI-PingV:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-19C4:TI-PingV:LowLvlLock-Sel', 0, 0.0],

    ['SI-Fam:TI-BPM:DelayRaw-SP', 0, 0],
    ['SI-Fam:TI-BPM:Duration-SP', 0, 0.0],  # [us]
    ['SI-Fam:TI-BPM:NrPulses-SP', 0, 0.0],
    ['SI-Fam:TI-BPM:Polarity-Sel', 0, 0.0],
    ['SI-Fam:TI-BPM:Src-Sel', 0, 0.0],
    ['SI-Fam:TI-BPM:State-Sel', 0, 0.0],
    ['SI-Fam:TI-BPM:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Fam:TI-BPM:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-BbBProcH-Fid:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-BbBProcH-Fid:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-BbBProcH-Fid:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-BbBProcH-Fid:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcH-Fid:RFDelayType-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcH-Fid:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcH-Fid:State-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcH-Fid:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-BbBProcH-Fid:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-BbBProcH-Trig1:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-BbBProcH-Trig1:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-BbBProcH-Trig1:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-BbBProcH-Trig1:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcH-Trig1:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcH-Trig1:State-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcH-Trig1:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-BbBProcH-Trig1:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-BbBProcH-Trig2:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-BbBProcH-Trig2:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-BbBProcH-Trig2:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-BbBProcH-Trig2:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcH-Trig2:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcH-Trig2:State-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcH-Trig2:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-BbBProcH-Trig2:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-BbBProcL-Fid:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-BbBProcL-Fid:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-BbBProcL-Fid:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-BbBProcL-Fid:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcL-Fid:RFDelayType-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcL-Fid:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcL-Fid:State-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcL-Fid:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-BbBProcL-Fid:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-BbBProcL-Trig1:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-BbBProcL-Trig1:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-BbBProcL-Trig1:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-BbBProcL-Trig1:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcL-Trig1:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcL-Trig1:State-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcL-Trig1:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-BbBProcL-Trig1:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-BbBProcL-Trig2:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-BbBProcL-Trig2:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-BbBProcL-Trig2:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-BbBProcL-Trig2:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcL-Trig2:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcL-Trig2:State-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcL-Trig2:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-BbBProcL-Trig2:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-BbBProcV-Fid:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-BbBProcV-Fid:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-BbBProcV-Fid:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-BbBProcV-Fid:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcV-Fid:RFDelayType-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcV-Fid:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcV-Fid:State-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcV-Fid:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-BbBProcV-Fid:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-BbBProcV-Trig1:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-BbBProcV-Trig1:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-BbBProcV-Trig1:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-BbBProcV-Trig1:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcV-Trig1:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcV-Trig1:State-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcV-Trig1:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-BbBProcV-Trig1:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-BbBProcV-Trig2:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-BbBProcV-Trig2:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-BbBProcV-Trig2:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-BbBProcV-Trig2:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcV-Trig2:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcV-Trig2:State-Sel', 0, 0.0],
    ['SI-Glob:TI-BbBProcV-Trig2:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-BbBProcV-Trig2:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-LLRF-PsMtn:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-LLRF-PsMtn:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-LLRF-PsMtn:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-LLRF-PsMtn:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-LLRF-PsMtn:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-LLRF-PsMtn:State-Sel', 0, 0.0],
    ['SI-Glob:TI-LLRF-PsMtn:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-LLRF-PsMtn:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-LLRF-Rmp:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-LLRF-Rmp:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-LLRF-Rmp:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-LLRF-Rmp:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-LLRF-Rmp:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-LLRF-Rmp:State-Sel', 0, 0.0],
    ['SI-Glob:TI-LLRF-Rmp:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-LLRF-Rmp:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-Mags-Bends:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-Mags-Bends:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-Mags-Bends:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-Mags-Bends:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-Bends:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-Bends:State-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-Bends:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-Mags-Bends:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-Mags-Corrs:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-Mags-Corrs:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-Mags-Corrs:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-Mags-Corrs:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-Corrs:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-Corrs:State-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-Corrs:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-Mags-Corrs:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-Mags-Quads:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-Mags-Quads:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-Mags-Quads:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-Mags-Quads:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-Quads:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-Quads:State-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-Quads:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-Mags-Quads:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-Mags-QTrims:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-Mags-QTrims:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-Mags-QTrims:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-Mags-QTrims:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-QTrims:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-QTrims:State-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-QTrims:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-Mags-QTrims:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-Mags-Sexts:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-Mags-Sexts:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-Mags-Sexts:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-Mags-Sexts:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-Sexts:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-Sexts:State-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-Sexts:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-Mags-Sexts:LowLvlLock-Sel', 0, 0.0],

    ['SI-Glob:TI-Mags-Skews:DelayRaw-SP', 0, 0],
    ['SI-Glob:TI-Mags-Skews:Duration-SP', 0, 0.0],  # [us]
    ['SI-Glob:TI-Mags-Skews:NrPulses-SP', 0, 0.0],
    ['SI-Glob:TI-Mags-Skews:Polarity-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-Skews:Src-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-Skews:State-Sel', 0, 0.0],
    ['SI-Glob:TI-Mags-Skews:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['SI-Glob:TI-Mags-Skews:LowLvlLock-Sel', 0, 0.0],

# NOTE: This trigger is not present yet in timing IOC:
#     ['SI-Glob:TI-StrkCam-Trig1:DelayRaw-SP', 0, 0],
#     ['SI-Glob:TI-StrkCam-Trig1:Duration-SP', 0, 0.0],  # [us]
#     ['SI-Glob:TI-StrkCam-Trig1:NrPulses-SP', 0, 0.0],
#     ['SI-Glob:TI-StrkCam-Trig1:Polarity-Sel', 0, 0.0],
#     ['SI-Glob:TI-StrkCam-Trig1:RFDelayType-Sel', 0, 0.0],
#     ['SI-Glob:TI-StrkCam-Trig1:Src-Sel', 0, 0.0],
#     ['SI-Glob:TI-StrkCam-Trig1:State-Sel', 0, 0.0],
#     ['SI-Glob:TI-StrkCam-Trig1:DeltaDelay-SP', 30*[0.0, ], 0.0],
#     ['SI-Glob:TI-StrkCam-Trig1:LowLvlLock-Sel', 0, 0.0],

#     ['SI-Glob:TI-StrkCam-Trig2:DelayRaw-SP', 0, 0],
#     ['SI-Glob:TI-StrkCam-Trig2:Duration-SP', 0, 0.0],  # [us]
#     ['SI-Glob:TI-StrkCam-Trig2:NrPulses-SP', 0, 0.0],
#     ['SI-Glob:TI-StrkCam-Trig2:Polarity-Sel', 0, 0.0],
#     ['SI-Glob:TI-StrkCam-Trig2:RFDelayType-Sel', 0, 0.0],
#     ['SI-Glob:TI-StrkCam-Trig2:Src-Sel', 0, 0.0],
#     ['SI-Glob:TI-StrkCam-Trig2:State-Sel', 0, 0.0],
#     ['SI-Glob:TI-StrkCam-Trig2:DeltaDelay-SP', 30*[0.0, ], 0.0],
#     ['SI-Glob:TI-StrkCam-Trig2:LowLvlLock-Sel', 0, 0.0],

    ['TB-04:TI-InjSept:DelayRaw-SP', 0, 0],
    ['TB-04:TI-InjSept:Duration-SP', 0, 0.0],  # [us]
    ['TB-04:TI-InjSept:NrPulses-SP', 0, 0.0],
    ['TB-04:TI-InjSept:Polarity-Sel', 0, 0.0],
    ['TB-04:TI-InjSept:Src-Sel', 0, 0.0],
    ['TB-04:TI-InjSept:State-Sel', 0, 0.0],
    ['TB-04:TI-InjSept:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['TB-04:TI-InjSept:LowLvlLock-Sel', 0, 0.0],

    ['TB-Fam:TI-BPM:DelayRaw-SP', 0, 0],
    ['TB-Fam:TI-BPM:Duration-SP', 0, 0.0],  # [us]
    ['TB-Fam:TI-BPM:NrPulses-SP', 0, 0.0],
    ['TB-Fam:TI-BPM:Polarity-Sel', 0, 0.0],
    ['TB-Fam:TI-BPM:Src-Sel', 0, 0.0],
    ['TB-Fam:TI-BPM:State-Sel', 0, 0.0],
    ['TB-Fam:TI-BPM:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['TB-Fam:TI-BPM:LowLvlLock-Sel', 0, 0.0],

    ['TB-Fam:TI-ICT-Digit:DelayRaw-SP', 0, 0],
    ['TB-Fam:TI-ICT-Digit:Duration-SP', 0, 0.0],  # [us]
    ['TB-Fam:TI-ICT-Digit:NrPulses-SP', 0, 0.0],
    ['TB-Fam:TI-ICT-Digit:Polarity-Sel', 0, 0.0],
    ['TB-Fam:TI-ICT-Digit:Src-Sel', 0, 0.0],
    ['TB-Fam:TI-ICT-Digit:State-Sel', 0, 0.0],
    ['TB-Fam:TI-ICT-Digit:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['TB-Fam:TI-ICT-Digit:LowLvlLock-Sel', 0, 0.0],

    ['TB-Fam:TI-ICT-Integ:DelayRaw-SP', 0, 0],
    ['TB-Fam:TI-ICT-Integ:Duration-SP', 0, 0.0],  # [us]
    ['TB-Fam:TI-ICT-Integ:NrPulses-SP', 0, 0.0],
    ['TB-Fam:TI-ICT-Integ:Polarity-Sel', 0, 0.0],
    ['TB-Fam:TI-ICT-Integ:Src-Sel', 0, 0.0],
    ['TB-Fam:TI-ICT-Integ:State-Sel', 0, 0.0],
    ['TB-Fam:TI-ICT-Integ:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['TB-Fam:TI-ICT-Integ:LowLvlLock-Sel', 0, 0.0],

    ['TB-Glob:TI-Mags:DelayRaw-SP', 0, 0],
    ['TB-Glob:TI-Mags:Duration-SP', 0, 0.0],  # [us]
    ['TB-Glob:TI-Mags:NrPulses-SP', 0, 0.0],
    ['TB-Glob:TI-Mags:Polarity-Sel', 0, 0.0],
    ['TB-Glob:TI-Mags:Src-Sel', 0, 0.0],
    ['TB-Glob:TI-Mags:State-Sel', 0, 0.0],
    ['TB-Glob:TI-Mags:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['TB-Glob:TI-Mags:LowLvlLock-Sel', 0, 0.0],

    ['TS-01:TI-EjeSeptF:DelayRaw-SP', 0, 0],
    ['TS-01:TI-EjeSeptF:Duration-SP', 0, 0.0],  # [us]
    ['TS-01:TI-EjeSeptF:NrPulses-SP', 0, 0.0],
    ['TS-01:TI-EjeSeptF:Polarity-Sel', 0, 0.0],
    ['TS-01:TI-EjeSeptF:RFDelayType-Sel', 0, 0.0],
    ['TS-01:TI-EjeSeptF:Src-Sel', 0, 0.0],
    ['TS-01:TI-EjeSeptF:State-Sel', 0, 0.0],
    ['TS-01:TI-EjeSeptF:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['TS-01:TI-EjeSeptF:LowLvlLock-Sel', 0, 0.0],

    ['TS-01:TI-EjeSeptG:DelayRaw-SP', 0, 0],
    ['TS-01:TI-EjeSeptG:Duration-SP', 0, 0.0],  # [us]
    ['TS-01:TI-EjeSeptG:NrPulses-SP', 0, 0.0],
    ['TS-01:TI-EjeSeptG:Polarity-Sel', 0, 0.0],
    ['TS-01:TI-EjeSeptG:RFDelayType-Sel', 0, 0.0],
    ['TS-01:TI-EjeSeptG:Src-Sel', 0, 0.0],
    ['TS-01:TI-EjeSeptG:State-Sel', 0, 0.0],
    ['TS-01:TI-EjeSeptG:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['TS-01:TI-EjeSeptG:LowLvlLock-Sel', 0, 0.0],

    ['TS-04:TI-InjSeptF:DelayRaw-SP', 0, 0],
    ['TS-04:TI-InjSeptF:Duration-SP', 0, 0.0],  # [us]
    ['TS-04:TI-InjSeptF:NrPulses-SP', 0, 0.0],
    ['TS-04:TI-InjSeptF:Polarity-Sel', 0, 0.0],
    ['TS-04:TI-InjSeptF:Src-Sel', 0, 0.0],
    ['TS-04:TI-InjSeptF:State-Sel', 0, 0.0],
    ['TS-04:TI-InjSeptF:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['TS-04:TI-InjSeptF:LowLvlLock-Sel', 0, 0.0],

    ['TS-04:TI-InjSeptG-1:DelayRaw-SP', 0, 0],
    ['TS-04:TI-InjSeptG-1:Duration-SP', 0, 0.0],  # [us]
    ['TS-04:TI-InjSeptG-1:NrPulses-SP', 0, 0.0],
    ['TS-04:TI-InjSeptG-1:Polarity-Sel', 0, 0.0],
    ['TS-04:TI-InjSeptG-1:Src-Sel', 0, 0.0],
    ['TS-04:TI-InjSeptG-1:State-Sel', 0, 0.0],
    ['TS-04:TI-InjSeptG-1:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['TS-04:TI-InjSeptG-1:LowLvlLock-Sel', 0, 0.0],

    ['TS-04:TI-InjSeptG-2:DelayRaw-SP', 0, 0],
    ['TS-04:TI-InjSeptG-2:Duration-SP', 0, 0.0],  # [us]
    ['TS-04:TI-InjSeptG-2:NrPulses-SP', 0, 0.0],
    ['TS-04:TI-InjSeptG-2:Polarity-Sel', 0, 0.0],
    ['TS-04:TI-InjSeptG-2:Src-Sel', 0, 0.0],
    ['TS-04:TI-InjSeptG-2:State-Sel', 0, 0.0],
    ['TS-04:TI-InjSeptG-2:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['TS-04:TI-InjSeptG-2:LowLvlLock-Sel', 0, 0.0],

    ['TS-Fam:TI-BPM:DelayRaw-SP', 0, 0],
    ['TS-Fam:TI-BPM:Duration-SP', 0, 0.0],  # [us]
    ['TS-Fam:TI-BPM:NrPulses-SP', 0, 0.0],
    ['TS-Fam:TI-BPM:Polarity-Sel', 0, 0.0],
    ['TS-Fam:TI-BPM:Src-Sel', 0, 0.0],
    ['TS-Fam:TI-BPM:State-Sel', 0, 0.0],
    ['TS-Fam:TI-BPM:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['TS-Fam:TI-BPM:LowLvlLock-Sel', 0, 0.0],

    ['TS-Fam:TI-ICT-Digit:DelayRaw-SP', 0, 0],
    ['TS-Fam:TI-ICT-Digit:Duration-SP', 0, 0.0],  # [us]
    ['TS-Fam:TI-ICT-Digit:NrPulses-SP', 0, 0.0],
    ['TS-Fam:TI-ICT-Digit:Polarity-Sel', 0, 0.0],
    ['TS-Fam:TI-ICT-Digit:Src-Sel', 0, 0.0],
    ['TS-Fam:TI-ICT-Digit:State-Sel', 0, 0.0],
    ['TS-Fam:TI-ICT-Digit:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['TS-Fam:TI-ICT-Digit:LowLvlLock-Sel', 0, 0.0],

    ['TS-Fam:TI-ICT-Integ:DelayRaw-SP', 0, 0],
    ['TS-Fam:TI-ICT-Integ:Duration-SP', 0, 0.0],  # [us]
    ['TS-Fam:TI-ICT-Integ:NrPulses-SP', 0, 0.0],
    ['TS-Fam:TI-ICT-Integ:Polarity-Sel', 0, 0.0],
    ['TS-Fam:TI-ICT-Integ:Src-Sel', 0, 0.0],
    ['TS-Fam:TI-ICT-Integ:State-Sel', 0, 0.0],
    ['TS-Fam:TI-ICT-Integ:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['TS-Fam:TI-ICT-Integ:LowLvlLock-Sel', 0, 0.0],

    ['TS-Fam:TI-Scrn:DelayRaw-SP', 0, 0],
    ['TS-Fam:TI-Scrn:Duration-SP', 0, 0.0],  # [us]
    ['TS-Fam:TI-Scrn:NrPulses-SP', 0, 0.0],
    ['TS-Fam:TI-Scrn:Polarity-Sel', 0, 0.0],
    ['TS-Fam:TI-Scrn:RFDelayType-Sel', 0, 0.0],
    ['TS-Fam:TI-Scrn:Src-Sel', 0, 0.0],
    ['TS-Fam:TI-Scrn:State-Sel', 0, 0.0],
    ['TS-Fam:TI-Scrn:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['TS-Fam:TI-Scrn:LowLvlLock-Sel', 0, 0.0],

    ['TS-Glob:TI-Mags:DelayRaw-SP', 0, 0],
    ['TS-Glob:TI-Mags:Duration-SP', 0, 0.0],  # [us]
    ['TS-Glob:TI-Mags:NrPulses-SP', 0, 0.0],
    ['TS-Glob:TI-Mags:Polarity-Sel', 0, 0.0],
    ['TS-Glob:TI-Mags:Src-Sel', 0, 0.0],
    ['TS-Glob:TI-Mags:State-Sel', 0, 0.0],
    ['TS-Glob:TI-Mags:DeltaDelay-SP', 30*[0.0, ], 0.0],
    ['TS-Glob:TI-Mags:LowLvlLock-Sel', 0, 0.0],

    ]


_pvs_li_ps = [
    ['LI-01:PS-LensRev:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Lens-1:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Lens-2:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Lens-3:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Lens-4:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Slnd-1:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Slnd-2:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Slnd-3:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Slnd-4:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Slnd-5:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Slnd-6:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Slnd-7:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Slnd-8:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Slnd-9:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Slnd-10:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Slnd-11:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Slnd-12:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Slnd-13:Current-SP', 0.0, 0.0],  # [A]
    ['LI-Fam:PS-Slnd-14:Current-SP', 0.0, 0.0],  # [A]
    ['LI-Fam:PS-Slnd-15:Current-SP', 0.0, 0.0],  # [A]
    ['LI-Fam:PS-Slnd-16:Current-SP', 0.0, 0.0],  # [A]
    ['LI-Fam:PS-Slnd-17:Current-SP', 0.0, 0.0],  # [A]
    ['LI-Fam:PS-Slnd-18:Current-SP', 0.0, 0.0],  # [A]
    ['LI-Fam:PS-Slnd-19:Current-SP', 0.0, 0.0],  # [A]
    ['LI-Fam:PS-Slnd-20:Current-SP', 0.0, 0.0],  # [A]
    ['LI-Fam:PS-Slnd-21:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-CH-1:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-CH-2:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-CV-3:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-CH-3:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-CV-4:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-CH-4:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-CV-5:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-CH-5:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-CV-6:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-CH-6:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-CV-7:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-CH-7:Current-SP', 0.0, 0.0],  # [A]
    ['LI-Fam:PS-QF1:Current-SP', 0.0, 0.0],  # [A]
    ['LI-Fam:PS-QF2:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-QF3:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-QD1:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-QD2:Current-SP', 0.0, 0.0],  # [A]
    ['LI-01:PS-Spect:Current-SP', 0.0, 0.0],  # [A]
    ]


_pvs_as_pu = [
    ['TB-04:PU-InjSept:Voltage-SP', 0.0, 0.0],   # [V]
    ['BO-01D:PU-InjKckr:Voltage-SP', 0.0, 0.0],  # [V]
    ['BO-48D:PU-EjeKckr:Voltage-SP', 0.0, 0.0],  # [V]
    ['SI-01SA:PU-InjDpKckr:Voltage-SP', 0.0, 0.0],  # [V]
    ['SI-01SA:PU-InjNLKckr:Voltage-SP', 0.0, 0.0],  # [V]
    ['TS-04:PU-InjSeptG-1:Voltage-SP', 0.0, 0.0],  # [V]
    ['TS-04:PU-InjSeptG-2:Voltage-SP', 0.0, 0.0],  # [V]
    ['TS-04:PU-InjSeptF:Voltage-SP', 0.0, 0.0],  # [V]
    ['TS-01:PU-EjeSeptG:Voltage-SP', 0.0, 0.0],  # [V]
    ['TS-01:PU-EjeSeptF:Voltage-SP', 0.0, 0.1],  # [V]
    ]


_pvs_as_rf = [
    ['RF-Gen:FreqPhsCont-Sel', 0, 0.0],
    ['RF-Gen:GeneralFreq-SP', 0.0, 0.0],  # [Hz]
    ]


_pvs_tb_ps = [
    ['TB-Fam:PS-B:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-01:PS-QD1:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-01:PS-QF1:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-02:PS-QD2A:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-02:PS-QF2A:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-02:PS-QF2B:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-02:PS-QD2B:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-03:PS-QF3:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-03:PS-QD3:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-04:PS-QF4:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-04:PS-QD4:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-01:PS-CH-1:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-01:PS-CV-1:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-01:PS-CH-2:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-01:PS-CV-2:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-02:PS-CH-1:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-02:PS-CV-1:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-02:PS-CH-2:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-02:PS-CV-2:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-04:PS-CH-1:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-04:PS-CH-2:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-04:PS-CV-1:OpMode-Sel', _SLOWREF, 0.0],
    ['TB-04:PS-CV-2:OpMode-Sel', _SLOWREF, 0.05],

    ['TB-Fam:PS-B:Current-SP', 0.0, 0.0],    # [A]
    ['TB-01:PS-QD1:Current-SP', 0.0, 0.0],   # [A]
    ['TB-01:PS-QF1:Current-SP', 0.0, 0.0],   # [A]
    ['TB-02:PS-QD2A:Current-SP', 0.0, 0.0],  # [A]
    ['TB-02:PS-QF2A:Current-SP', 0.0, 0.0],  # [A]
    ['TB-02:PS-QF2B:Current-SP', 0.0, 0.0],  # [A]
    ['TB-02:PS-QD2B:Current-SP', 0.0, 0.0],  # [A]
    ['TB-03:PS-QF3:Current-SP', 0.0, 0.0],   # [A]
    ['TB-03:PS-QD3:Current-SP', 0.0, 0.0],   # [A]
    ['TB-04:PS-QF4:Current-SP', 0.0, 0.0],   # [A]
    ['TB-04:PS-QD4:Current-SP', 0.0, 0.0],   # [A]
    ['TB-01:PS-CH-1:Current-SP', 0.0, 0.0],  # [A]
    ['TB-01:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['TB-01:PS-CH-2:Current-SP', 0.0, 0.0],  # [A]
    ['TB-01:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['TB-02:PS-CH-1:Current-SP', 0.0, 0.0],  # [A]
    ['TB-02:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['TB-02:PS-CH-2:Current-SP', 0.0, 0.0],  # [A]
    ['TB-02:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['TB-04:PS-CH-1:Current-SP', 0.0, 0.0],  # [A]
    ['TB-04:PS-CH-2:Current-SP', 0.0, 0.0],  # [A]
    ['TB-04:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['TB-04:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ]


_pvs_bo_ps = [
    ['BO-Fam:PS-B-1:Wfm-SP', _DEFAULT_WFM_OTHERS, 0.0],  # [A]
    ['BO-Fam:PS-B-2:Wfm-SP', _DEFAULT_WFM_OTHERS, 0.0],  # [A]
    ['BO-Fam:PS-QD:Wfm-SP', _DEFAULT_WFM_OTHERS, 0.0],  # [A]
    ['BO-Fam:PS-QF:Wfm-SP', _DEFAULT_WFM_OTHERS, 0.0],  # [A]
    ['BO-Fam:PS-SD:Wfm-SP', _DEFAULT_WFM_OTHERS, 0.0],  # [A]
    ['BO-Fam:PS-SF:Wfm-SP', _DEFAULT_WFM_OTHERS, 0.0],  # [A]
    ['BO-02D:PS-QS:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-01U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-03U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-05U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-07U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-09U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-11U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-13U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-15U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-17U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-19U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-21U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-23U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-25U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-27U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-29U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-31U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-33U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-35U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-37U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-39U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-41U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-43U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-45U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-47U:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-49D:PS-CH:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-01U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-03U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-05U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-07U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-09U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-11U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-13U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-15U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-17U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-19U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-21U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-23U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-25U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-27U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-29U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-31U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-33U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-35U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-37U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-39U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-41U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-43U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-45U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-47U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ['BO-49U:PS-CV:Wfm-SP', _DEFAULT_WFM_FBP, 0.0],  # [A]
    ]


_pvs_ts_ps = [
    ['TS-Fam:PS-B:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-01:PS-QF1A:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-01:PS-QF1B:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-02:PS-QF2:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-03:PS-QF3:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-04:PS-QF4:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-02:PS-QD2:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-04:PS-QD4A:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-04:PS-QD4B:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-01:PS-CH:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-02:PS-CH:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-03:PS-CH:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-04:PS-CH:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-01:PS-CV-1:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-01:PS-CV-1E2:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-01:PS-CV-2:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-02:PS-CV-0:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-02:PS-CV:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-03:PS-CV:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-04:PS-CV-0:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-04:PS-CV-1:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-04:PS-CV-1E2:OpMode-Sel', _SLOWREF, 0.0],
    ['TS-04:PS-CV-2:OpMode-Sel', _SLOWREF, 0.05],

    ['TS-Fam:PS-B:Current-SP', 0.0, 0.0],    # [A]
    ['TS-01:PS-QF1A:Current-SP', 0.0, 0.0],   # [A]
    ['TS-01:PS-QF1B:Current-SP', 0.0, 0.0],   # [A]
    ['TS-02:PS-QF2:Current-SP', 0.0, 0.0],  # [A]
    ['TS-03:PS-QF3:Current-SP', 0.0, 0.0],  # [A]
    ['TS-04:PS-QF4:Current-SP', 0.0, 0.0],  # [A]
    ['TS-02:PS-QD2:Current-SP', 0.0, 0.0],  # [A]
    ['TS-04:PS-QD4A:Current-SP', 0.0, 0.0],   # [A]
    ['TS-04:PS-QD4B:Current-SP', 0.0, 0.0],   # [A]
    ['TS-01:PS-CH:Current-SP', 0.0, 0.0],   # [A]
    ['TS-02:PS-CH:Current-SP', 0.0, 0.0],   # [A]
    ['TS-03:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['TS-04:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['TS-01:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['TS-01:PS-CV-1E2:Current-SP', 0.0, 0.0],  # [A]
    ['TS-01:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['TS-02:PS-CV-0:Current-SP', 0.0, 0.0],  # [A]
    ['TS-02:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['TS-03:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['TS-04:PS-CV-0:Current-SP', 0.0, 0.0],  # [A]
    ['TS-04:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['TS-04:PS-CV-1E2:Current-SP', 0.0, 0.0],  # [A]
    ['TS-04:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ]


_pvs_si_ps_fam = [
    ['SI-Fam:PS-B1B2-1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-B1B2-2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-QFA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-QFP:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-QDA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-QDP1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-QDP2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SFA0:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SFA1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SFA2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SFB0:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SFB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SFB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SFP0:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SFP1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SFP2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SDA0:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SDA1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SDA2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SDA3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SDB0:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SDB3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SDP0:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SDP1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SDP2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-Fam:PS-SDP3:OpMode-Sel', _SLOWREF, 0.05],

    ['SI-Fam:PS-B1B2-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-B1B2-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-QFA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-QFP:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-QDA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-QDP1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-QDP2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SFA0:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SFA1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SFA2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SFB0:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SFB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SFB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SFP0:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SFP1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SFP2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SDA0:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SDA1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SDA2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SDA3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SDB0:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SDB3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SDP0:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SDP1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SDP2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-Fam:PS-SDP3:Current-SP', 0.0, 0.0],  # [A]
    ]


_pvs_si_ps_ch = [
    ['SI-01M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20M2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C2:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C3:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C4:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01M1:PS-CH:Current-SP', 0.0, 0.0],  # [A]
    ]


_pvs_si_ps_cv = [
    ['SI-01M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20M2:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C2:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C2:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C3:PS-CV-1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C3:PS-CV-2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C4:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01M1:PS-CV:Current-SP', 0.0, 0.0],  # [A]
    ]


_pvs_si_ps_qs = [
    ['SI-01M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-01C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-01C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-01C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20M1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20M2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20C1:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20C2:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20C3:PS-QS:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-01M1:PS-QS:OpMode-Sel', _SLOWREF, 0.05],

    ['SI-01M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20M2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C2:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C3:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01M1:PS-QS:Current-SP', 0.0, 0.0],  # [A]
    ]


_pvs_si_ps_qn = [
    ['SI-01M2:PS-QDA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-01M2:PS-QFA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-01C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-01C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-01C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-01C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-01C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-01C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-01C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-01C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02M1:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02M1:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02M1:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02M2:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02M2:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02M2:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-02C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03M1:PS-QDP1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03M1:PS-QDP2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03M1:PS-QFP:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03M2:PS-QDP1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03M2:PS-QDP2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03M2:PS-QFP:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-03C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04M1:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04M1:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04M1:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04M2:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04M2:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04M2:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-04C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05M1:PS-QDA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05M1:PS-QFA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05M2:PS-QDA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05M2:PS-QFA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-05C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06M1:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06M1:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06M1:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06M2:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06M2:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06M2:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-06C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07M1:PS-QDP1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07M1:PS-QDP2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07M1:PS-QFP:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07M2:PS-QDP1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07M2:PS-QDP2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07M2:PS-QFP:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-07C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08M1:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08M1:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08M1:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08M2:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08M2:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08M2:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-08C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09M1:PS-QDA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09M1:PS-QFA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09M2:PS-QDA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09M2:PS-QFA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-09C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10M1:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10M1:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10M1:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10M2:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10M2:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10M2:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-10C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11M1:PS-QDP1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11M1:PS-QDP2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11M1:PS-QFP:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11M2:PS-QDP1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11M2:PS-QDP2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11M2:PS-QFP:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-11C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12M1:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12M1:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12M1:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12M2:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12M2:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12M2:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-12C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13M1:PS-QDA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13M1:PS-QFA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13M2:PS-QDA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13M2:PS-QFA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-13C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14M1:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14M1:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14M1:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14M2:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14M2:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14M2:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-14C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15M1:PS-QDP1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15M1:PS-QDP2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15M1:PS-QFP:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15M2:PS-QDP1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15M2:PS-QDP2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15M2:PS-QFP:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-15C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16M1:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16M1:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16M1:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16M2:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16M2:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16M2:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-16C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17M1:PS-QDA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17M1:PS-QFA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17M2:PS-QDA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17M2:PS-QFA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-17C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18M1:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18M1:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18M1:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18M2:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18M2:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18M2:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-18C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19M1:PS-QDP1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19M1:PS-QDP2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19M1:PS-QFP:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19M2:PS-QDP1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19M2:PS-QDP2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19M2:PS-QFP:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-19C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20M1:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20M1:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20M1:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20M2:PS-QDB1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20M2:PS-QDB2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20M2:PS-QFB:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20C1:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20C1:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20C2:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20C2:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20C3:PS-Q3:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20C3:PS-Q4:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20C4:PS-Q1:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-20C4:PS-Q2:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-01M1:PS-QDA:OpMode-Sel', _SLOWREF, 0.0],
    ['SI-01M1:PS-QFA:OpMode-Sel', _SLOWREF, 0.05],

    ['SI-01M2:PS-QDA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01M2:PS-QFA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02M1:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02M1:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02M1:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02M2:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02M2:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02M2:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-02C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03M1:PS-QDP1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03M1:PS-QDP2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03M1:PS-QFP:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03M2:PS-QDP1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03M2:PS-QDP2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03M2:PS-QFP:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-03C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04M1:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04M1:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04M1:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04M2:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04M2:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04M2:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-04C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05M1:PS-QDA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05M1:PS-QFA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05M2:PS-QDA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05M2:PS-QFA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-05C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06M1:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06M1:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06M1:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06M2:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06M2:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06M2:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-06C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07M1:PS-QDP1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07M1:PS-QDP2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07M1:PS-QFP:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07M2:PS-QDP1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07M2:PS-QDP2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07M2:PS-QFP:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-07C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08M1:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08M1:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08M1:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08M2:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08M2:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08M2:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-08C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09M1:PS-QDA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09M1:PS-QFA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09M2:PS-QDA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09M2:PS-QFA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-09C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10M1:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10M1:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10M1:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10M2:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10M2:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10M2:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-10C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11M1:PS-QDP1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11M1:PS-QDP2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11M1:PS-QFP:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11M2:PS-QDP1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11M2:PS-QDP2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11M2:PS-QFP:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-11C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12M1:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12M1:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12M1:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12M2:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12M2:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12M2:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-12C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13M1:PS-QDA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13M1:PS-QFA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13M2:PS-QDA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13M2:PS-QFA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-13C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14M1:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14M1:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14M1:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14M2:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14M2:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14M2:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-14C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15M1:PS-QDP1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15M1:PS-QDP2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15M1:PS-QFP:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15M2:PS-QDP1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15M2:PS-QDP2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15M2:PS-QFP:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-15C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16M1:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16M1:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16M1:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16M2:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16M2:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16M2:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-16C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17M1:PS-QDA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17M1:PS-QFA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17M2:PS-QDA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17M2:PS-QFA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-17C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18M1:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18M1:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18M1:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18M2:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18M2:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18M2:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-18C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19M1:PS-QDP1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19M1:PS-QDP2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19M1:PS-QFP:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19M2:PS-QDP1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19M2:PS-QDP2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19M2:PS-QFP:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-19C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20M1:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20M1:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20M1:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20M2:PS-QDB1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20M2:PS-QDB2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20M2:PS-QFB:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C1:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C1:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C2:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C2:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C3:PS-Q3:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C3:PS-Q4:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C4:PS-Q1:Current-SP', 0.0, 0.0],  # [A]
    ['SI-20C4:PS-Q2:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01M1:PS-QDA:Current-SP', 0.0, 0.0],  # [A]
    ['SI-01M1:PS-QFA:Current-SP', 0.0, 0.0],  # [A]
    ]


_template_dict = {
    'pvs':
    _pvs_as_ti +
    _pvs_li_egunmod + _pvs_li_llrf + _pvs_li_ps +
    _pvs_as_pu +
    _pvs_as_rf +
    _pvs_tb_ps + _pvs_bo_ps + _pvs_ts_ps +
    _pvs_si_ps_fam +
    _pvs_si_ps_ch + _pvs_si_ps_cv +
    _pvs_si_ps_qs + _pvs_si_ps_qn
    }
