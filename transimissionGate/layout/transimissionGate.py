from gdsfactory import Component
from glayout.flow.pdk.mappedpdk import MappedPDK
from glayout.flow.placement.two_transistor_interdigitized import two_nfet_interdigitized
from glayout.flow.placement.two_transistor_interdigitized import two_pfet_interdigitized
from glayout.flow.pdk.util.comp_utils import prec_ref_center, movey, evaluate_bbox
from glayout.flow.routing.smart_route import smart_route
from glayout.flow.routing.c_route import c_route

from glayout.flow.placement.common_centroid_ab_ba import common_centroid_ab_ba
from glayout.flow.blocks.current_mirror import current_mirror
from glayout.flow.blocks.opamp import opamp

from glayout.flow.primitives.fet import nmos, pmos

from glayout.flow.pdk.sky130_mapped import sky130_mapped_pdk

def TransimissionGate(pdk: MappedPDK, width: float, length: float, fingers: int) -> Component:
    TransimissionGate = Component(name="TransimissionGate")

    tran_gate_nmos = nmos(sky130_mapped_pdk, width=width, length=length, fingers=fingers, with_dummy=True, with_tie=True)
    tran_gate_nmos_ref = prec_ref_center(tran_gate_nmos)
    TransimissionGate.add(tran_gate_nmos_ref)

    tran_gate_pmos = pmos(sky130_mapped_pdk, width=width, length=length, fingers=fingers, with_dummy=True, with_tie=True)
    tran_gate_pmos_ref = prec_ref_center(tran_gate_pmos)
    TransimissionGate.add(tran_gate_pmos_ref)

    offset = evaluate_bbox(tran_gate_nmos)[1] + pdk.util_max_metal_seperation()
    movey(tran_gate_pmos_ref, offset)

    TransimissionGate.add_ports(tran_gate_nmos_ref.get_ports_list(), prefix="nmos_")
    TransimissionGate.add_ports(tran_gate_pmos_ref.get_ports_list(), prefix="pmos_")

    print(tran_gate_nmos_ref.get_ports_dict())

    return TransimissionGate

#TransimissionGate(sky130_mapped_pdk, 4, 1, 2).show()