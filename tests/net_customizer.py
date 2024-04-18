from os import listdir
from os.path import isfile
from os.path import join
import pm4py
from pm4py import Marking
import morphism_manager
import transformator
from tests.test import view_net

directory = "data"
file = "1-1.pnml"

if __name__ == "__main__":
    net, marking, _ = pm4py.read_pnml(join(directory, file))
    while True:
        print(
            "-1 - exit \n"
            "0 - change label of transition by name\n"
            "1 - save result\n2 - do transformation\n"
            "3 - transformation step by step\n"
            "4 - show net\n"
            "5 - remove transition\n"
            "6 - remove place\n"
            "7 - add arc\n"
            "8 - remove all labels\n"
            "9 - remove arc\n"
            "10 - update initial marking")
        print("input command number")
        command = int(input())
        if command == -1:
            break
        if command == 0:
            print("input name of element")
            name = list(input().split(' '))
            obj = [i for i in net.transitions if i.name in name]
            if not obj:
                continue
            print("input new label")
            name = input()
            for i in obj:
                i.label = name if name != "" else None
        if command == 1:
            pm4py.write_pnml(net, marking, Marking(), join(directory, file))
        if command == 2 or command == 3:
            net_tmp, marking_tmp = morphism_manager.PetriNetMorphismManager.deep_net_copy(net, marking)
            morphism_manager.PetriNetMorphismManager.start_transformations(net_tmp, marking_tmp, display=command == 3)
            view_net(net_tmp)
            print(marking, marking_tmp)
        if command == 4:
            view_net(net)
            print(marking)
        if command in [5, 6]:
            print("input name")
            name = input()
            obj = [i for i in net.transitions if i.name == name] if command == 5 else [i for i in net.places if
                                                                                       i.name == name]
            if not obj:
                continue
            obj = obj[0]
            if command == 5:
                pm4py.objects.petri_net.utils.petri_utils.remove_transition(net, obj)
            else:
                pm4py.objects.petri_net.utils.petri_utils.remove_place(net, obj)
        if command in [7, 9]:
            name1 = input()
            name2 = input()
            obj1 = [i for i in net.places if i.name == name1] + [i for i in net.transitions if i.name == name1]
            obj2 = [i for i in net.places if i.name == name2] + [i for i in net.transitions if i.name == name2]
            if not obj1 or not obj2:
                continue
            obj1 = obj1[0]
            obj2 = obj2[0]
            if command == 7:
                pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(obj1, obj2, net)
            else:
                arc = [i for i in net.arcs if i.source == obj1 and i.target == obj2]
                if not arc:
                    continue
                arc = arc[0]
                pm4py.objects.petri_net.utils.petri_utils.remove_arc(net, arc)
        if command == 8:
            for i in net.transitions:
                i.label = None
        if command == 10:
            marking = Marking()
            for i in [j for j in net.places if len(j.in_arcs) == 0]:
                marking[i] = 1
        if command == 11:
            trans: transformator.Transformator = transformator.Transformator(net)
            s_components = trans.get_s_components(marking)
            print(len(net.places), len(net.transitions), len(s_components))
            j = min(s_components, key=lambda x: len(x))
            print(j)
            print("-----------")
            net_tmp, marking_tmp = morphism_manager.PetriNetMorphismManager.deep_net_copy(net, marking)
            morphism_manager.PetriNetMorphismManager.start_transformations(net_tmp, marking_tmp, display=command == 3)
            trans = transformator.Transformator(net_tmp)
            s_components = trans.get_s_components(marking_tmp)
            print(len(net_tmp.places), len(net_tmp.transitions), len(s_components),s_components)
