import pm4py
from os.path import join

import morphism_manager
from tests.test import check, view_net

test_path = "data"
answer_path = "results"
source = "1-1.pnml"

if __name__ == "__main__":
    net, marking, _ = pm4py.read_pnml(join(test_path, source))
    net_result, marking_result, _ = pm4py.read_pnml(join(answer_path, "result_" + source))
    view_net(net)
    view_net(net_result)
    print(
        "test_name/isomorphism/alphamorphism----------------",
        check(net, marking, net_result, marking_result, morphism_manager.PetriNetMorphismManager.check_isomorphism),
        check(net, marking, net_result, marking_result,
              morphism_manager.PetriNetMorphismManager.check_alphamorphism),
        "----------------"
    )
