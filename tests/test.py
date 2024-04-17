from os import listdir
from os.path import isfile
from os.path import join
import pm4py
from pm4py import Marking
import morphism_manager


def view_net(net):
    pm4py.view_petri_net(net, Marking(), None, decorations={
                                                               place: {"label": place.name} for place in
                                                               net.places
                                                           } | {transition: {"label": transition.name}
                                                                for
                                                                transition in
                                                                net.transitions})


def remove_empty_labels(net):
    for i in net.transitions:
        if i.label is not None and i.label.find('\n') != -1:
            i.label = None


def check(net, marking, net_result, marking_result, check_morphism):
    remove_empty_labels(net)
    remove_empty_labels(net_result)
    return check_morphism(net, marking, net_result, marking_result)


def init():
    tests = sorted([filename for filename in listdir(join(test_path)) if
                    isfile(join(test_path, filename)) and filename.find(".pnml") != -1])
    for test in tests:
        net, marking, _ = pm4py.read_pnml(join(test_path, test))
        check(net, marking, net, marking, morphism_manager.PetriNetMorphismManager.check_alphamorphism)
        pm4py.write_pnml(net, marking, Marking(), join(answer_path, "result_" + test))


test_path = "data"
answer_path = "results"

if __name__ == "__main__":
    if not listdir(answer_path):
        init()

    tests = sorted([filename for filename in listdir(join(test_path)) if
                    isfile(join(test_path, filename)) and filename.find(".pnml") != -1])
    answers = sorted([filename for filename in listdir(join(answer_path)) if
                      isfile(join(answer_path, filename)) and filename.find(".pnml") != -1])

    with open("tmp.txt", "a") as file:
        for test in zip(tests, answers):
            net, marking, _ = pm4py.read_pnml(join(test_path, test[0]))
            net_result, marking_result, _ = pm4py.read_pnml(join(answer_path, test[1]))
            print(
                "test_name/isomorphism/alphamorphism----------------",
                test[0],
                check(net, marking, net_result, marking_result, morphism_manager.PetriNetMorphismManager.check_isomorphism),
                check(net, marking, net_result, marking_result,
                      morphism_manager.PetriNetMorphismManager.check_alphamorphism),
                "----------------"
            )
            data = morphism_manager.PetriNetMorphismManager.start_transformations(net, marking)
            pnml = ".pnml"
            empty = ""
            file.write(
                f"|{test[0].replace(pnml, empty)}|{data.start_number_of_places}|{data.result_number_of_places}|{data.start_number_of_transitions}|{data.result_number_of_transitions}|\n")
