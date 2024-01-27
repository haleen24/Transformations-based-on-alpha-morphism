import os

import pm4py
from morphism_manager import PetriNetMorphismManager

if __name__ == '__main__':
    net, initial_marking, final_marking = pm4py.read_pnml(os.path.join("../nets/test_net.pnml"))
    pm4py.view_petri_net(net, initial_marking, final_marking)

    manager = PetriNetMorphismManager()
    manager.start_transformations(net)
    pm4py.view_petri_net(net, initial_marking, final_marking)

    stop = input()
    manager.restore_to_default()
    pm4py.view_petri_net(net,initial_marking,final_marking)