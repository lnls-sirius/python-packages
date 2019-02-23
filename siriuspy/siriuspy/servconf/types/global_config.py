"""LI low level RF configuration."""
from copy import deepcopy as _dcopy


_off = 0
_on = 1


def get_dict():
    """Return configuration type dictionary."""
    module_name = __name__.split('.')[-1]
    _dict = {
        'config_type_name': module_name,
        'value': _dcopy(_template_dict)
    }
    return _dict


# When using this type of configuration to set the machine,
# the list of PVs should be processed in the same order they are stored
# in the configuration. The second numeric parameter in the pair is the
# delay [s] the client should wait before setting the next PV.

_pvs_li_llrf = [
    ['LA-RF:LLRF:BUN1:SET_STREAM', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH1_DELAY', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH2_DELAY', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH7_DELAY', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_CH8_DELAY', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_TRIGGER_DELAY', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_AMP', 0.0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_PHASE', 0.0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_FB_MODE', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_KP', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_KI', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_EXTERNAL_TRIGGER_ENABLE', 0, 0.0],
    ['LA-RF:LLRF:BUN1:SET_INTEGRAL_ENABLE', 0, 0.0],
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
    ['LA-RF:LLRF:BUN1:SET_PID_MODE', 0, 0.0],
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
    ['LA-RF:LLRF:KLY1:SET_AMP', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_PHASE', 0.0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_FB_MODE', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_KP', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_KI', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_EXTERNAL_TRIGGER_ENABLE', 0, 0.0],
    ['LA-RF:LLRF:KLY1:SET_INTEGRAL_ENABLE', 0, 0.0],
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
    ['LA-RF:LLRF:KLY2:SET_AMP', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_PHASE', 0.0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_FB_MODE', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_KP', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_KI', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_EXTERNAL_TRIGGER_ENABLE', 0, 0.0],
    ['LA-RF:LLRF:KLY2:SET_INTEGRAL_ENABLE', 0, 0.0],
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

_pvs_li_hl_timing = [
    ['RA-RaMO:TI-EVG:LinacMode-Sel', 0, 0.0],
    ['RA-RaMO:TI-EVG:DigLIMode-Sel', 0, 0.0],

    ['RA-RaMO:TI-EVG:LinacDelayType-Sel', 0, 0.0],
    ['RA-RaMO:TI-EVG:DigLIDelayType-Sel', 0, 0.0],

    ['RA-RaMO:TI-EVG:LinacDelay-SP', 0.0, 0.0],
    ['RA-RaMO:TI-EVG:DigLIDelay-SP', 0.0, 0.0],

    ['LI-01:TI-EGun-MultBun:State-Sel', 0, 0.0],
    ['LI-01:TI-EGun-SglBun:State-Sel', 0, 0.0],
    ['LI-01:TI-Modltr-1:State-Sel', 0, 0.0],
    ['LI-01:TI-Modltr-2:State-Sel', 0, 0.0],
    ['LI-Fam:TI-BPM:State-Sel', 0, 0.0],
    ['LI-Fam:TI-ICT:State-Sel', 0, 0.0],
    ['LI-Fam:TI-Scrn:State-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly1:State-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly2:State-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-SHB:State-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly1:State-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly2:State-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-SHB:State-Sel', 0, 0.0],

    ['LI-01:TI-EGun-MultBun:Polarity-Sel', 0, 0.0],
    ['LI-01:TI-EGun-SglBun:Polarity-Sel', 0, 0.0],
    ['LI-01:TI-Modltr-1:Polarity-Sel', 0, 0.0],
    ['LI-01:TI-Modltr-2:Polarity-Sel', 0, 0.0],
    ['LI-Fam:TI-BPM:Polarity-Sel', 0, 0.0],
    ['LI-Fam:TI-ICT:Polarity-Sel', 0, 0.0],
    ['LI-Fam:TI-Scrn:Polarity-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly1:Polarity-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly2:Polarity-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-SHB:Polarity-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly1:Polarity-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly2:Polarity-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-SHB:Polarity-Sel', 0, 0.0],

    ['LI-01:TI-EGun-MultBun:Src-Sel', 0, 0.0],
    ['LI-01:TI-EGun-SglBun:Src-Sel', 0, 0.0],
    ['LI-01:TI-Modltr-1:Src-Sel', 0, 0.0],
    ['LI-01:TI-Modltr-2:Src-Sel', 0, 0.0],
    ['LI-Fam:TI-BPM:Src-Sel', 0, 0.0],
    ['LI-Fam:TI-ICT:Src-Sel', 0, 0.0],
    ['LI-Fam:TI-Scrn:Src-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly1:Src-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly2:Src-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-SHB:Src-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly1:Src-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly2:Src-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-SHB:Src-Sel', 0, 0.0],

    ['LI-01:TI-EGun-MultBun:NrPulses-SP', 0, 0.0],
    ['LI-01:TI-EGun-SglBun:NrPulses-SP', 0, 0.0],
    ['LI-01:TI-Modltr-1:NrPulses-SP', 0, 0.0],
    ['LI-01:TI-Modltr-2:NrPulses-SP', 0, 0.0],
    ['LI-Fam:TI-BPM:NrPulses-SP', 0, 0.0],
    ['LI-Fam:TI-ICT:NrPulses-SP', 0, 0.0],
    ['LI-Fam:TI-Scrn:NrPulses-SP', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly1:NrPulses-SP', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly2:NrPulses-SP', 0, 0.0],
    ['LI-Glob:TI-LLRF-SHB:NrPulses-SP', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly1:NrPulses-SP', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly2:NrPulses-SP', 0, 0.0],
    ['LI-Glob:TI-SSAmp-SHB:NrPulses-SP', 0, 0.0],

    ['LI-01:TI-EGun-MultBun:Duration-SP', 0.0, 0.0],
    ['LI-01:TI-EGun-SglBun:Duration-SP', 0.0, 0.0],
    ['LI-01:TI-Modltr-1:Duration-SP', 0.0, 0.0],
    ['LI-01:TI-Modltr-2:Duration-SP', 0.0, 0.0],
    ['LI-Fam:TI-BPM:Duration-SP', 0.0, 0.0],
    ['LI-Fam:TI-ICT:Duration-SP', 0.0, 0.0],
    ['LI-Fam:TI-Scrn:Duration-SP', 0.0, 0.0],
    ['LI-Glob:TI-LLRF-Kly1:Duration-SP', 0.0, 0.0],
    ['LI-Glob:TI-LLRF-Kly2:Duration-SP', 0.0, 0.0],
    ['LI-Glob:TI-LLRF-SHB:Duration-SP', 0.0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly1:Duration-SP', 0.0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly2:Duration-SP', 0.0, 0.0],
    ['LI-Glob:TI-SSAmp-SHB:Duration-SP', 0.0, 0.0],

    ['LI-01:TI-EGun-MultBun:Delay-SP', 0.0, 0.0],
    ['LI-01:TI-EGun-SglBun:Delay-SP', 0.0, 0.0],
    ['LI-01:TI-Modltr-1:Delay-SP', 0.0, 0.0],
    ['LI-01:TI-Modltr-2:Delay-SP', 0.0, 0.0],
    ['LI-Fam:TI-BPM:Delay-SP', 0.0, 0.0],
    ['LI-Fam:TI-ICT:Delay-SP', 0.0, 0.0],
    ['LI-Fam:TI-Scrn:Delay-SP', 0.0, 0.0],
    ['LI-Glob:TI-LLRF-Kly1:Delay-SP', 0.0, 0.0],
    ['LI-Glob:TI-LLRF-Kly2:Delay-SP', 0.0, 0.0],
    ['LI-Glob:TI-LLRF-SHB:Delay-SP', 0.0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly1:Delay-SP', 0.0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly2:Delay-SP', 0.0, 0.0],
    ['LI-Glob:TI-SSAmp-SHB:Delay-SP', 0.0, 0.0],

    ['LI-01:TI-EGun-MultBun:ByPassIntlk-Sel', 0, 0.0],
    ['LI-01:TI-EGun-SglBun:ByPassIntlk-Sel', 0, 0.0],
    ['LI-01:TI-Modltr-1:ByPassIntlk-Sel', 0, 0.0],
    ['LI-01:TI-Modltr-2:ByPassIntlk-Sel', 0, 0.0],
    ['LI-Fam:TI-BPM:ByPassIntlk-Sel', 0, 0.0],
    ['LI-Fam:TI-ICT:ByPassIntlk-Sel', 0, 0.0],
    ['LI-Fam:TI-Scrn:ByPassIntlk-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly1:ByPassIntlk-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-Kly2:ByPassIntlk-Sel', 0, 0.0],
    ['LI-Glob:TI-LLRF-SHB:ByPassIntlk-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly1:ByPassIntlk-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-Kly2:ByPassIntlk-Sel', 0, 0.0],
    ['LI-Glob:TI-SSAmp-SHB:ByPassIntlk-Sel', 0, 0.0],

    ['LI-01:TI-EGun-MultBun:RFDelayType-Sel', 0, 0.0],
    ['LI-01:TI-EGun-SglBun:RFDelayType-Sel', 0, 0.0],
    # ['LI-01:TI-Modltr-1:RFDelayType-Sel', 0, 0.0],
    # ['LI-01:TI-Modltr-2:RFDelayType-Sel', 0, 0.0],
    ['LI-Fam:TI-BPM:RFDelayType-Sel', 0, 0.0],
    ['LI-Fam:TI-ICT:RFDelayType-Sel', 0, 0.0],
    ['LI-Fam:TI-Scrn:RFDelayType-Sel', 0, 0.0],
    # ['LI-Glob:TI-LLRF-Kly1:RFDelayType-Sel', 0, 0.0],
    # ['LI-Glob:TI-LLRF-Kly2:RFDelayType-Sel', 0, 0.0],
    # ['LI-Glob:TI-LLRF-SHB:RFDelayType-Sel', 0, 0.0],
    # ['LI-Glob:TI-SSAmp-Kly1:RFDelayType-Sel', 0, 0.0],
    # ['LI-Glob:TI-SSAmp-Kly2:RFDelayType-Sel', 0, 0.0],
    # ['LI-Glob:TI-SSAmp-SHB:RFDelayType-Sel', 0, 0.0],
    ]

_pvs_li_pwrsupplies = [
    ['LA-CN:H1MLPS-1:seti', 0.0, 0.0],
    ['LA-CN:H1MLPS-2:seti', 0.0, 0.0],
    ['LA-CN:H1MLPS-3:seti', 0.0, 0.0],
    ['LA-CN:H1MLPS-4:seti', 0.0, 0.0],
    ['LA-CN:H1SCPS-1:seti', 0.0, 0.0],
    ['LA-CN:H1SCPS-2:seti', 0.0, 0.0],
    ['LA-CN:H1SCPS-3:seti', 0.0, 0.0],
    ['LA-CN:H1SCPS-4:seti', 0.0, 0.0],
    ['LA-CN:H1LCPS-1:seti', 0.0, 0.0],
    ['LA-CN:H1LCPS-2:seti', 0.0, 0.0],
    ['LA-CN:H1LCPS-3:seti', 0.0, 0.0],
    ['LA-CN:H1LCPS-4:seti', 0.0, 0.0],
    ['LA-CN:H1LCPS-5:seti', 0.0, 0.0],
    ['LA-CN:H1LCPS-6:seti', 0.0, 0.0],
    ['LA-CN:H1LCPS-7:seti', 0.0, 0.0],
    ['LA-CN:H1LCPS-8:seti', 0.0, 0.0],
    ['LA-CN:H1LCPS-9:seti', 0.0, 0.0],
    ['LA-CN:H1LCPS-10:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-1:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-2:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-3:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-4:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-5:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-6:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-7:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-8:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-9:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-10:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-11:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-12:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-13:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-14:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-15:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-16:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-17:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-18:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-19:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-20:seti', 0.0, 0.0],
    ['LA-CN:H1SLPS-21:seti', 0.0, 0.0],
    ['LA-CN:H1FQPS-1:seti', 0.0, 0.0],
    ['LA-CN:H1FQPS-2:seti', 0.0, 0.0],
    ['LA-CN:H1FQPS-3:seti', 0.0, 0.0],
    ['LA-CN:H1DQPS-1:seti', 0.0, 0.0],
    ['LA-CN:H1DQPS-2:seti', 0.0, 0.0],
    ['LA-CN:H1RCPS-1:seti', 0.0, 0.0],
    ['LA-CN:H1DPPS-1:seti', 0.0, 0.0],
    ]

_pvs_tb_ma = [
    ['TB-Fam:PS-B:PwrState-Sel', _off, 0.0],
    ['TB-01:PS-QD1:PwrState-Sel', _off, 0.0],
    ['TB-01:PS-QF1:PwrState-Sel', _off, 0.0],
    ['TB-02:PS-QD2A:PwrState-Sel', _off, 0.0],
    ['TB-02:PS-QF2A:PwrState-Sel', _off, 0.0],
    ['TB-02:PS-QF2B:PwrState-Sel', _off, 0.0],
    ['TB-02:PS-QD2B:PwrState-Sel', _off, 0.0],
    ['TB-03:PS-QF3:PwrState-Sel', _off, 0.0],
    ['TB-03:PS-QD3:PwrState-Sel', _off, 0.0],
    ['TB-04:PS-QF4:PwrState-Sel', _off, 0.0],
    ['TB-04:PS-QD4:PwrState-Sel', _off, 0.0],
    ['TB-01:PS-CH-1:PwrState-Sel', _off, 0.0],
    ['TB-01:PS-CV-1:PwrState-Sel', _off, 0.0],
    ['TB-01:PS-CH-2:PwrState-Sel', _off, 0.0],
    ['TB-01:PS-CV-2:PwrState-Sel', _off, 0.0],
    ['TB-02:PS-CH-1:PwrState-Sel', _off, 0.0],
    ['TB-02:PS-CV-1:PwrState-Sel', _off, 0.0],
    ['TB-02:PS-CH-2:PwrState-Sel', _off, 0.0],
    ['TB-02:PS-CV-2:PwrState-Sel', _off, 0.0],
    ['TB-04:PS-CH:PwrState-Sel', _off, 0.0],
    ['TB-04:PS-CV-1:PwrState-Sel', _off, 0.0],
    ['TB-04:PS-CV-2:PwrState-Sel', _off, 0.0],

    ['TB-Fam:PS-B:OpMode-Sel', _off, 0.0],
    ['TB-01:PS-QD1:OpMode-Sel', _off, 0.0],
    ['TB-01:PS-QF1:OpMode-Sel', _off, 0.0],
    ['TB-02:PS-QD2A:OpMode-Sel', _off, 0.0],
    ['TB-02:PS-QF2A:OpMode-Sel', _off, 0.0],
    ['TB-02:PS-QF2B:OpMode-Sel', _off, 0.0],
    ['TB-02:PS-QD2B:OpMode-Sel', _off, 0.0],
    ['TB-03:PS-QF3:OpMode-Sel', _off, 0.0],
    ['TB-03:PS-QD3:OpMode-Sel', _off, 0.0],
    ['TB-04:PS-QF4:OpMode-Sel', _off, 0.0],
    ['TB-04:PS-QD4:OpMode-Sel', _off, 0.0],
    ['TB-01:PS-CH-1:OpMode-Sel', _off, 0.0],
    ['TB-01:PS-CV-1:OpMode-Sel', _off, 0.0],
    ['TB-01:PS-CH-2:OpMode-Sel', _off, 0.0],
    ['TB-01:PS-CV-2:OpMode-Sel', _off, 0.0],
    ['TB-02:PS-CH-1:OpMode-Sel', _off, 0.0],
    ['TB-02:PS-CV-1:OpMode-Sel', _off, 0.0],
    ['TB-02:PS-CH-2:OpMode-Sel', _off, 0.0],
    ['TB-02:PS-CV-2:OpMode-Sel', _off, 0.0],
    ['TB-04:PS-CH:OpMode-Sel', _off, 0.0],
    ['TB-04:PS-CV-1:OpMode-Sel', _off, 0.0],
    ['TB-04:PS-CV-2:OpMode-Sel', _off, 0.0],

    ['TB-Fam:PS-B:BSMPComm-Sel', _on, 0.0],
    ['TB-01:PS-QD1:BSMPComm-Sel', _on, 0.0],
    ['TB-01:PS-QF1:BSMPComm-Sel', _on, 0.0],
    ['TB-02:PS-QD2A:BSMPComm-Sel', _on, 0.0],
    ['TB-02:PS-QF2A:BSMPComm-Sel', _on, 0.0],
    ['TB-02:PS-QF2B:BSMPComm-Sel', _on, 0.0],
    ['TB-02:PS-QD2B:BSMPComm-Sel', _on, 0.0],
    ['TB-03:PS-QF3:BSMPComm-Sel', _on, 0.0],
    ['TB-03:PS-QD3:BSMPComm-Sel', _on, 0.0],
    ['TB-04:PS-QF4:BSMPComm-Sel', _on, 0.0],
    ['TB-04:PS-QD4:BSMPComm-Sel', _on, 0.0],
    ['TB-01:PS-CH-1:BSMPComm-Sel', _on, 0.0],
    ['TB-01:PS-CV-1:BSMPComm-Sel', _on, 0.0],
    ['TB-01:PS-CH-2:BSMPComm-Sel', _on, 0.0],
    ['TB-01:PS-CV-2:BSMPComm-Sel', _on, 0.0],
    ['TB-02:PS-CH-1:BSMPComm-Sel', _on, 0.0],
    ['TB-02:PS-CV-1:BSMPComm-Sel', _on, 0.0],
    ['TB-02:PS-CH-2:BSMPComm-Sel', _on, 0.0],
    ['TB-02:PS-CV-2:BSMPComm-Sel', _on, 0.0],
    ['TB-04:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['TB-04:PS-CV-1:BSMPComm-Sel', _on, 0.0],
    ['TB-04:PS-CV-2:BSMPComm-Sel', _on, 0.0],

    ['TB-Fam:PS-B:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-01:PS-QD1:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-01:PS-QF1:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-02:PS-QD2A:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-02:PS-QF2A:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-02:PS-QF2B:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-02:PS-QD2B:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-03:PS-QF3:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-03:PS-QD3:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-04:PS-QF4:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-04:PS-QD4:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-01:PS-CH-1:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-01:PS-CV-1:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-01:PS-CH-2:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-01:PS-CV-2:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-02:PS-CH-1:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-02:PS-CV-1:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-02:PS-CH-2:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-02:PS-CV-2:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-04:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-04:PS-CV-1:RmpIncNrCycles-SP', 1, 0.0],
    ['TB-04:PS-CV-2:RmpIncNrCycles-SP', 1, 0.0],

    ['TB-Fam:PS-B:Current-SP', 0.0, 0.0],
    ['TB-01:PS-QD1:Current-SP', 0.0, 0.0],
    ['TB-01:PS-QF1:Current-SP', 0.0, 0.0],
    ['TB-02:PS-QD2A:Current-SP', 0.0, 0.0],
    ['TB-02:PS-QF2A:Current-SP', 0.0, 0.0],
    ['TB-02:PS-QF2B:Current-SP', 0.0, 0.0],
    ['TB-02:PS-QD2B:Current-SP', 0.0, 0.0],
    ['TB-03:PS-QF3:Current-SP', 0.0, 0.0],
    ['TB-03:PS-QD3:Current-SP', 0.0, 0.0],
    ['TB-04:PS-QF4:Current-SP', 0.0, 0.0],
    ['TB-04:PS-QD4:Current-SP', 0.0, 0.0],
    ['TB-01:PS-CH-1:Current-SP', 0.0, 0.0],
    ['TB-01:PS-CV-1:Current-SP', 0.0, 0.0],
    ['TB-01:PS-CH-2:Current-SP', 0.0, 0.0],
    ['TB-01:PS-CV-2:Current-SP', 0.0, 0.0],
    ['TB-02:PS-CH-1:Current-SP', 0.0, 0.0],
    ['TB-02:PS-CV-1:Current-SP', 0.0, 0.0],
    ['TB-02:PS-CH-2:Current-SP', 0.0, 0.0],
    ['TB-02:PS-CV-2:Current-SP', 0.0, 0.0],
    ['TB-04:PS-CH:Current-SP', 0.0, 0.0],
    ['TB-04:PS-CV-1:Current-SP', 0.0, 0.0],
    ['TB-04:PS-CV-2:Current-SP', 0.0, 0.0],
    ]

_pvs_tb_pu = [
    ['TB-04:PU-InjSept:PwrState-Sel', 0, 0.0],
    ['BO-01D:PU-InjKckr:PwrState-Sel', 0, 0.0],
    ['TB-04:PU-InjSept:Pulse-Sel', 0, 0.0],
    ['BO-01D:PU-InjKckr:Pulse-Sel', 0, 0.0],
    ['TB-04:PU-InjSept:Voltage-SP', 0.0, 0.0],
    ['BO-01D:PU-InjKckr:Voltage-SP', 0.0, 0.0],
]

_pvs_tb_hl_timing = [
    ['RA-RaMO:TI-EVG:InjBOMode-Sel', 0, 0.0],
    ['RA-RaMO:TI-EVG:DigTBMode-Sel', 0, 0.0],

    ['RA-RaMO:TI-EVG:InjBODelayType-Sel', 0, 0.0],
    ['RA-RaMO:TI-EVG:DigTBDelayType-Sel', 0, 0.0],

    ['RA-RaMO:TI-EVG:InjBODelay-SP', 0.0, 0.0],
    ['RA-RaMO:TI-EVG:DigTBDelay-SP', 0.0, 0.0],

    ['TB-Glob:TI-Mags:State-Sel', 0, 0.0],
    ['TB-04:TI-InjSept:State-Sel', 0, 0.0],
    ['AS-Fam:TI-Scrn-TBBO:State-Sel', 0, 0.0],
    ['AS-Glob:TI-BPM-TBTS:State-Sel', 0, 0.0],
    ['AS-Glob:TI-Osc-InjBO:State-Sel', 0, 0.0],
    ['TB-Fam:TI-ICT-Digit:State-Sel', 0, 0.0],
    ['TB-Fam:TI-ICT-Integ:State-Sel', 0, 0.0],
    ['BO-01D:TI-InjKckr:State-Sel', 0, 0.0],
    ['AS-Glob:TI-FCT:State-Sel', 0, 0.0],

    ['TB-Glob:TI-Mags:Polarity-Sel', 0, 0.0],
    ['TB-04:TI-InjSept:Polarity-Sel', 0, 0.0],
    ['AS-Fam:TI-Scrn-TBBO:Polarity-Sel', 0, 0.0],
    ['AS-Glob:TI-BPM-TBTS:Polarity-Sel', 0, 0.0],
    ['AS-Glob:TI-Osc-InjBO:Polarity-Sel', 0, 0.0],
    ['TB-Fam:TI-ICT-Digit:Polarity-Sel', 0, 0.0],
    ['TB-Fam:TI-ICT-Integ:Polarity-Sel', 0, 0.0],
    ['BO-01D:TI-InjKckr:Polarity-Sel', 0, 0.0],
    ['AS-Glob:TI-FCT:Polarity-Sel', 0, 0.0],

    ['TB-Glob:TI-Mags:Src-Sel', 0, 0.0],
    ['TB-04:TI-InjSept:Src-Sel', 0, 0.0],
    ['AS-Fam:TI-Scrn-TBBO:Src-Sel', 0, 0.0],
    ['AS-Glob:TI-BPM-TBTS:Src-Sel', 0, 0.0],
    ['AS-Glob:TI-Osc-InjBO:Src-Sel', 0, 0.0],
    ['TB-Fam:TI-ICT-Digit:Src-Sel', 0, 0.0],
    ['TB-Fam:TI-ICT-Integ:Src-Sel', 0, 0.0],
    ['BO-01D:TI-InjKckr:Src-Sel', 0, 0.0],
    ['AS-Glob:TI-FCT:Src-Sel', 0, 0.0],

    ['TB-Glob:TI-Mags:NrPulses-SP', 0, 0.0],
    ['TB-04:TI-InjSept:NrPulses-SP', 0, 0.0],
    ['AS-Fam:TI-Scrn-TBBO:NrPulses-SP', 0, 0.0],
    ['AS-Glob:TI-BPM-TBTS:NrPulses-SP', 0, 0.0],
    ['AS-Glob:TI-Osc-InjBO:NrPulses-SP', 0, 0.0],
    ['TB-Fam:TI-ICT-Digit:NrPulses-SP', 0, 0.0],
    ['TB-Fam:TI-ICT-Integ:NrPulses-SP', 0, 0.0],
    ['BO-01D:TI-InjKckr:NrPulses-SP', 0, 0.0],
    ['AS-Glob:TI-FCT:NrPulses-SP', 0, 0.0],

    ['TB-Glob:TI-Mags:Duration-SP', 0.0, 0.0],
    ['TB-04:TI-InjSept:Duration-SP', 0.0, 0.0],
    ['AS-Fam:TI-Scrn-TBBO:Duration-SP', 0.0, 0.0],
    ['AS-Glob:TI-BPM-TBTS:Duration-SP', 0.0, 0.0],
    ['AS-Glob:TI-Osc-InjBO:Duration-SP', 0.0, 0.0],
    ['TB-Fam:TI-ICT-Digit:Duration-SP', 0.0, 0.0],
    ['TB-Fam:TI-ICT-Integ:Duration-SP', 0.0, 0.0],
    ['BO-01D:TI-InjKckr:Duration-SP', 0.0, 0.0],
    ['AS-Glob:TI-FCT:Duration-SP', 0.0, 0.0],

    ['TB-Glob:TI-Mags:Delay-SP', 0.0, 0.0],
    ['TB-04:TI-InjSept:Delay-SP', 0.0, 0.0],
    ['AS-Fam:TI-Scrn-TBBO:Delay-SP', 0.0, 0.0],
    ['AS-Glob:TI-BPM-TBTS:Delay-SP', 0.0, 0.0],
    ['AS-Glob:TI-Osc-InjBO:Delay-SP', 0.0, 0.0],
    ['TB-Fam:TI-ICT-Digit:Delay-SP', 0.0, 0.0],
    ['TB-Fam:TI-ICT-Integ:Delay-SP', 0.0, 0.0],
    ['BO-01D:TI-InjKckr:Delay-SP', 0.0, 0.0],
    ['AS-Glob:TI-FCT:Delay-SP', 0.0, 0.0],

    # ['TB-Glob:TI-Mags:ByPassIntlk-Sel', 0, 0.0],
    ['TB-04:TI-InjSept:ByPassIntlk-Sel', 0, 0.0],
    ['AS-Fam:TI-Scrn-TBBO:ByPassIntlk-Sel', 0, 0.0],
    # ['AS-Glob:TI-BPM-TBTS:ByPassIntlk-Sel', 0, 0.0],
    ['AS-Glob:TI-Osc-InjBO:ByPassIntlk-Sel', 0, 0.0],
    ['TB-Fam:TI-ICT-Digit:ByPassIntlk-Sel', 0, 0.0],
    ['TB-Fam:TI-ICT-Integ:ByPassIntlk-Sel', 0, 0.0],
    ['BO-01D:TI-InjKckr:ByPassIntlk-Sel', 0, 0.0],
    ['AS-Glob:TI-FCT:ByPassIntlk-Sel', 0, 0.0],

    # ['TB-Glob:TI-Mags:RFDelayType-Sel', 0, 0.0],
    # ['TB-04:TI-InjSept:RFDelayType-Sel', 0, 0.0],
    ['AS-Fam:TI-Scrn-TBBO:RFDelayType-Sel', 0, 0.0],
    # ['AS-Glob:TI-BPM-TBTS:RFDelayType-Sel', 0, 0.0],
    # ['AS-Glob:TI-Osc-InjBO:RFDelayType-Sel', 0, 0.0],
    # ['TB-Fam:TI-ICT-Digit:RFDelayType-Sel', 0, 0.0],
    # ['TB-Fam:TI-ICT-Integ:RFDelayType-Sel', 0, 0.0],
    # ['BO-01D:TI-InjKckr:RFDelayType-Sel', 0, 0.0],
    ['AS-Glob:TI-FCT:RFDelayType-Sel', 0, 0.0],
    ]

_pvs_bo_ma = [
    ['BO-Fam:PS-B:PwrState-Sel', _off, 0.0],
    ['BO-Fam:PS-QD:PwrState-Sel', _off, 0.0],
    ['BO-Fam:PS-QF:PwrState-Sel', _off, 0.0],
    ['BO-02D:PS-QS:PwrState-Sel', _off, 0.0],
    ['BO-Fam:PS-SD:PwrState-Sel', _off, 0.0],
    ['BO-Fam:PS-SF:PwrState-Sel', _off, 0.0],
    ['BO-01U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-03U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-05U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-07U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-09U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-11U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-13U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-15U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-17U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-19U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-21U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-23U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-25U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-27U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-29U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-31U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-33U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-35U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-37U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-39U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-41U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-43U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-45U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-47U:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-49D:PS-CH:PwrState-Sel', _off, 0.0],
    ['BO-01U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-03U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-05U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-07U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-09U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-11U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-13U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-15U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-17U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-19U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-21U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-23U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-25U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-27U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-29U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-31U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-33U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-35U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-37U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-39U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-41U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-43U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-45U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-47U:PS-CV:PwrState-Sel', _off, 0.0],
    ['BO-49U:PS-CV:PwrState-Sel', _off, 0.0],

    ['BO-Fam:PS-B:OpMode-Sel', _off, 0.0],
    ['BO-Fam:PS-QD:OpMode-Sel', _off, 0.0],
    ['BO-Fam:PS-QF:OpMode-Sel', _off, 0.0],
    ['BO-02D:PS-QS:OpMode-Sel', _off, 0.0],
    ['BO-Fam:PS-SD:OpMode-Sel', _off, 0.0],
    ['BO-Fam:PS-SF:OpMode-Sel', _off, 0.0],
    ['BO-01U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-03U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-05U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-07U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-09U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-11U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-13U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-15U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-17U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-19U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-21U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-23U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-25U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-27U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-29U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-31U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-33U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-35U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-37U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-39U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-41U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-43U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-45U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-47U:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-49D:PS-CH:OpMode-Sel', _off, 0.0],
    ['BO-01U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-03U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-05U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-07U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-09U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-11U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-13U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-15U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-17U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-19U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-21U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-23U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-25U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-27U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-29U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-31U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-33U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-35U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-37U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-39U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-41U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-43U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-45U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-47U:PS-CV:OpMode-Sel', _off, 0.0],
    ['BO-49U:PS-CV:OpMode-Sel', _off, 0.0],

    ['BO-Fam:PS-B:BSMPComm-Sel', _on, 0.0],
    ['BO-Fam:PS-QD:BSMPComm-Sel', _on, 0.0],
    ['BO-Fam:PS-QF:BSMPComm-Sel', _on, 0.0],
    ['BO-02D:PS-QS:BSMPComm-Sel', _on, 0.0],
    ['BO-Fam:PS-SD:BSMPComm-Sel', _on, 0.0],
    ['BO-Fam:PS-SF:BSMPComm-Sel', _on, 0.0],
    ['BO-01U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-03U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-05U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-07U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-09U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-11U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-13U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-15U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-17U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-19U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-21U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-23U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-25U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-27U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-29U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-31U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-33U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-35U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-37U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-39U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-41U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-43U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-45U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-47U:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-49D:PS-CH:BSMPComm-Sel', _on, 0.0],
    ['BO-01U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-03U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-05U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-07U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-09U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-11U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-13U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-15U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-17U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-19U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-21U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-23U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-25U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-27U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-29U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-31U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-33U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-35U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-37U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-39U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-41U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-43U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-45U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-47U:PS-CV:BSMPComm-Sel', _on, 0.0],
    ['BO-49U:PS-CV:BSMPComm-Sel', _on, 0.0],

    ['BO-Fam:PS-B:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-Fam:PS-QD:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-Fam:PS-QF:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-02D:PS-QS:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-Fam:PS-SD:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-Fam:PS-SF:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-01U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-03U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-05U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-07U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-09U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-11U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-13U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-15U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-17U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-19U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-21U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-23U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-25U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-27U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-29U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-31U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-33U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-35U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-37U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-39U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-41U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-43U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-45U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-47U:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-49D:PS-CH:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-01U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-03U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-05U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-07U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-09U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-11U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-13U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-15U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-17U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-19U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-21U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-23U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-25U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-27U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-29U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-31U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-33U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-35U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-37U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-39U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-41U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-43U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-45U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-47U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],
    ['BO-49U:PS-CV:RmpIncNrCycles-SP', 1, 0.0],

    ['BO-Fam:PS-B-1:Current-SP', 0.0, 0.0],
    ['BO-Fam:PS-B-2:Current-SP', 0.0, 0.0],
    ['BO-Fam:PS-QD:Current-SP', 0.0, 0.0],
    ['BO-Fam:PS-QF:Current-SP', 0.0, 0.0],
    ['BO-02D:PS-QS:Current-SP', +0.0, 0.0],
    ['BO-Fam:PS-SD:Current-SP', 0.0, 0.0],
    ['BO-Fam:PS-SF:Current-SP', 0.0, 0.0],
    ['BO-01U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-03U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-05U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-07U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-09U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-11U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-13U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-15U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-17U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-19U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-21U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-23U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-25U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-27U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-29U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-31U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-33U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-35U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-37U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-39U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-41U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-43U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-45U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-47U:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-49D:PS-CH:Current-SP', +0.0, 0.0],
    ['BO-01U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-03U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-05U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-07U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-09U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-11U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-13U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-15U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-17U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-19U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-21U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-23U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-25U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-27U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-29U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-31U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-33U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-35U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-37U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-39U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-41U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-43U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-45U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-47U:PS-CV:Current-SP', +0.0, 0.0],
    ['BO-49U:PS-CV:Current-SP', +0.0, 0.0],
    ]

_pvs_bo_hl_timing = [
    ['RA-RaMO:TI-EVG:RmpBOMode-Sel', 0, 0.0],
    ['RA-RaMO:TI-EVG:DigBOMode-Sel', 0, 0.0],
    ['RA-RaMO:TI-EVG:OrbBOMode-Sel', 0, 0.0],

    ['RA-RaMO:TI-EVG:RmpBODelayType-Sel', 0, 0.0],
    ['RA-RaMO:TI-EVG:DigBODelayType-Sel', 0, 0.0],
    ['RA-RaMO:TI-EVG:OrbBODelayType-Sel', 0, 0.0],

    ['RA-RaMO:TI-EVG:RmpBODelay-SP', 0.0, 0.0],
    ['RA-RaMO:TI-EVG:DigBODelay-SP', 0.0, 0.0],
    ['RA-RaMO:TI-EVG:OrbBODelay-SP', 0.0, 0.0],

    ['BO-35D:TI-DCCT:State-Sel', 0, 0.0],
    ['BO-48D:TI-EjeKckr:State-Sel', 0, 0.0],
    ['BO-Glob:TI-Corrs:State-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-PsMtn:State-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-Rmp:State-Sel', 0, 0.0],
    ['BO-Glob:TI-Mags:State-Sel', 0, 0.0],
    ['BO-Glob:TI-TuneProc:State-Sel', 0, 0.0],
    ['AS-Glob:TI-BPM-SIBO:State-Sel', 0, 0.0],

    ['BO-35D:TI-DCCT:Polarity-Sel', 0, 0.0],
    ['BO-48D:TI-EjeKckr:Polarity-Sel', 0, 0.0],
    ['BO-Glob:TI-Corrs:Polarity-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-PsMtn:Polarity-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-Rmp:Polarity-Sel', 0, 0.0],
    ['BO-Glob:TI-Mags:Polarity-Sel', 0, 0.0],
    ['BO-Glob:TI-TuneProc:Polarity-Sel', 0, 0.0],
    ['AS-Glob:TI-BPM-SIBO:Polarity-Sel', 0, 0.0],

    ['BO-35D:TI-DCCT:Src-Sel', 0, 0.0],
    ['BO-48D:TI-EjeKckr:Src-Sel', 0, 0.0],
    ['BO-Glob:TI-Corrs:Src-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-PsMtn:Src-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-Rmp:Src-Sel', 0, 0.0],
    ['BO-Glob:TI-Mags:Src-Sel', 0, 0.0],
    ['BO-Glob:TI-TuneProc:Src-Sel', 0, 0.0],
    ['AS-Glob:TI-BPM-SIBO:Src-Sel', 0, 0.0],

    ['BO-35D:TI-DCCT:NrPulses-SP', 0, 0.0],
    ['BO-48D:TI-EjeKckr:NrPulses-SP', 0, 0.0],
    ['BO-Glob:TI-Corrs:NrPulses-SP', 0, 0.0],
    ['BO-Glob:TI-LLRF-PsMtn:NrPulses-SP', 0, 0.0],
    ['BO-Glob:TI-LLRF-Rmp:NrPulses-SP', 0, 0.0],
    ['BO-Glob:TI-Mags:NrPulses-SP', 0, 0.0],
    ['BO-Glob:TI-TuneProc:NrPulses-SP', 0, 0.0],
    ['AS-Glob:TI-BPM-SIBO:NrPulses-SP', 0, 0.0],

    ['BO-35D:TI-DCCT:Duration-SP', 0.0, 0.0],
    ['BO-48D:TI-EjeKckr:Duration-SP', 0.0, 0.0],
    ['BO-Glob:TI-Corrs:Duration-SP', 0.0, 0.0],
    ['BO-Glob:TI-LLRF-PsMtn:Duration-SP', 0.0, 0.0],
    ['BO-Glob:TI-LLRF-Rmp:Duration-SP', 0.0, 0.0],
    ['BO-Glob:TI-Mags:Duration-SP', 0.0, 0.0],
    ['BO-Glob:TI-TuneProc:Duration-SP', 0.0, 0.0],
    ['AS-Glob:TI-BPM-SIBO:Duration-SP', 0.0, 0.0],

    ['BO-35D:TI-DCCT:Delay-SP', 0.0, 0.0],
    ['BO-48D:TI-EjeKckr:Delay-SP', 0.0, 0.0],
    ['BO-Glob:TI-Corrs:Delay-SP', 0.0, 0.0],
    ['BO-Glob:TI-LLRF-PsMtn:Delay-SP', 0.0, 0.0],
    ['BO-Glob:TI-LLRF-Rmp:Delay-SP', 0.0, 0.0],
    ['BO-Glob:TI-Mags:Delay-SP', 0.0, 0.0],
    ['BO-Glob:TI-TuneProc:Delay-SP', 0.0, 0.0],
    ['AS-Glob:TI-BPM-SIBO:Delay-SP', 0.0, 0.0],

    ['BO-35D:TI-DCCT:ByPassIntlk-Sel', 0, 0.0],
    ['BO-48D:TI-EjeKckr:ByPassIntlk-Sel', 0, 0.0],
    # ['BO-Glob:TI-Corrs:ByPassIntlk-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-PsMtn:ByPassIntlk-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-Rmp:ByPassIntlk-Sel', 0, 0.0],
    ['BO-Glob:TI-Mags:ByPassIntlk-Sel', 0, 0.0],
    ['BO-Glob:TI-TuneProc:ByPassIntlk-Sel', 0, 0.0],
    # ['AS-Glob:TI-BPM-SIBO:ByPassIntlk-Sel', 0, 0.0],

    ['BO-35D:TI-DCCT:RFDelayType-Sel', 0, 0.0],
    ['BO-48D:TI-EjeKckr:RFDelayType-Sel', 0, 0.0],
    # ['BO-Glob:TI-Corrs:RFDelayType-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-PsMtn:RFDelayType-Sel', 0, 0.0],
    ['BO-Glob:TI-LLRF-Rmp:RFDelayType-Sel', 0, 0.0],
    # ['BO-Glob:TI-Mags:RFDelayType-Sel', 0, 0.0],
    ['BO-Glob:TI-TuneProc:RFDelayType-Sel', 0, 0.0],
    # ['AS-Glob:TI-BPM-SIBO:RFDelayType-Sel', 0, 0.0],
    ]

_template_dict = {
    'pvs':
        _pvs_li_llrf + _pvs_li_hl_timing + _pvs_li_pwrsupplies +
        _pvs_tb_ma + _pvs_tb_pu + _pvs_tb_hl_timing +
        _pvs_bo_ma + _pvs_bo_hl_timing
}
