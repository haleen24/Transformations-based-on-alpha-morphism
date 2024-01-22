import pm4py
from pm4py import Marking

import transformator

from pm4py.objects.petri_net.utils import petri_utils

if __name__ == "__main__":
    net = pm4py.PetriNet("tmp")

    p0 = pm4py.objects.petri_net.utils.petri_utils.add_place(net, "p0")
    p1 = pm4py.objects.petri_net.utils.petri_utils.add_place(net, "p1")

    transitions = [pm4py.objects.petri_net.utils.petri_utils.add_transition(net, f't{i}', f't{i}') for i in range(7)]

    for i in range(3):
        pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(transitions[i], p0, net)

    for i in range(4, 7):
        pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(p1, transitions[i], net)

    pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(p0, transitions[3], net)
    pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(transitions[3], p1, net)

    initial_marking = Marking()
    # initial_marking[p0] = 1

    pm4py.write_pnml(net, initial_marking, None, "nets/net.pnml")

    pm4py.view_petri_net(net, initial_marking)

    # tran = transformator.Transformator(net)
    # tran.rule_a1(p1, p2)

    pm4py.view_petri_net(net)

    trans = transformator.Transformator(net)

    trans.rule_a3(transitions[3])

    # pm4py.view_petri_net(net)

    trans.restore_rule()

    # pm4py.view_petri_net(net)
