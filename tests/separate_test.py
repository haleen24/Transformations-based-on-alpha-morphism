import pm4py
from os.path import join

import morphism_manager
from tests.test import check, view_net

test_path = "data"
answer_path = "results"
source = "2-3.pnml"

if __name__ == "__main__":
    net, marking, _ = pm4py.read_pnml(join(test_path, source))
    net_result, marking_result, _ = pm4py.read_pnml(join(answer_path, "result_" + source))
    view_net(net)
    view_net(net_result)
    print(
        "isomorphism: ",
        morphism_manager.PetriNetMorphismManager.check_isomorphism(net, marking, net_result, marking_result),
        "\nalphamorphism: ",
        morphism_manager.PetriNetMorphismManager.check_alphamorphism(net, marking, net_result, marking_result),
        end=''
    )
    view_net(net)
