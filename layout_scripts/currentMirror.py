from gdsfactory import Component
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized
from glayout.flow.placement.two_transistor_interdigitized import two_pfet_interdigitized
from glayout.flow.pdk.util.comp_utils import prec_ref_center, movey, evaluate_bbox
from glayout.flow.routing.smart_route import smart_route
from glayout.flow.routing.c_route import c_route

from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk

def CurrentMirror(pdk: MappedPDK, width, length, type):
    CurrentMirror = Component(name="CurrentMirror")
    if type == "pfet":
        currm = two_pfet_interdigitized(pdk, numcols=2, dummy=True, with_substrate_tap=False, with_tie=True, width=width, length=length, rmult=1)
    elif type == "nfet":
        currm = two_nfet_interdigitized(pdk, numcols=2, dummy=True, with_substrate_tap=False, with_tie=True, width=width, length=length, rmult=1)
    currm_ref = prec_ref_center(currm)
    CurrentMirror.add(currm_ref)
    CurrentMirror.add_ports(currm_ref.get_ports_list(), prefix="currm_")
    CurrentMirror << smart_route(pdk,CurrentMirror.ports["currm_A_gate_E"], CurrentMirror.ports["currm_B_gate_E"],currm_ref,CurrentMirror)
    CurrentMirror << smart_route(pdk,CurrentMirror.ports["currm_A_drain_E"], CurrentMirror.ports["currm_A_gate_E"],currm_ref,CurrentMirror)
    CurrentMirror << smart_route(pdk,CurrentMirror.ports["currm_A_source_E"], CurrentMirror.ports["currm_B_source_E"],currm_ref,CurrentMirror)
    return CurrentMirror

CurrentMirror(sky130_mapped_pdk, 2, 2, "pfet").show()