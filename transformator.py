import pm4py.objects.petri_net.utils.petri_utils
from pm4py import PetriNet
from transformation_logger import TransformationLogger
from transformation_logger import TransformationLog


class Transformator:
    def __init__(self, net):
        self.petri_net = net
        self.logger = TransformationLogger()
        self.__restore_functions = {
            'a1': self.restore_rule_a1,
            'a2': self.restore_rule_a2,
            'a3': self.restore_rule_a3,
            'a4': self.restore_rule_a4,
        }

    def rule_a1(self, p1: PetriNet.Place, p2: PetriNet.Place) -> None:
        """
        Place Simplification\n
        p1, p2: pm4py.PetriNet.Place\n
        p1 will be saved\n
        p2 will be destroyed\n
        """

        net = self.petri_net

        # if *p1 != *p2 or p1* != p2*
        if set(i.source for i in p1.in_arcs) != set(i.source for i in p2.in_arcs):
            return
        elif set(i.target for i in p1.out_arcs) != set(i.target for i in p2.out_arcs):
            return

        # logging for roll back
        self.logger.add_log(TransformationLog(p1.name, p2.name, 'a1'))

        # removing place
        pm4py.objects.petri_net.utils.petri_utils.remove_place(net, p2)

        return

    def rule_a2(self, t1: pm4py.PetriNet.Transition, t2: pm4py.PetriNet.Transition):
        """
        Transition Simplification\n
        t1, t2: pm4py.PetriNet.Transition\n
        t1 will be saved\n
        t2 will be destroyed\n
        """

        net = self.petri_net

        # if *p1 != *p2 or p1* != p2*
        if set(i.source for i in t1.in_arcs) != set(i.source for i in t2.in_arcs):
            return
        elif set(i.target for i in t1.out_arcs) != set(i.target for i in t2.out_arcs):
            return

        # logging for roll back
        self.logger.add_log(TransformationLog(t1.name, t2.name, 'a2'))

        # removing transition
        pm4py.objects.petri_net.utils.petri_utils.remove_transition(net, t2)

        return

    def rule_a3(self, t: pm4py.PetriNet.Transition):
        if not (len(t.in_arcs) == len(t.out_arcs) == 1):
            return
        p1: pm4py.PetriNet.Place = list(t.in_arcs)[0].source
        p2: pm4py.PetriNet.Place = list(t.out_arcs)[0].target

        if not (len(p1.out_arcs) == len(p2.in_arcs) == 1):
            return

        if p1.in_arcs is [] or p2.out_arcs is []:
            return

        if set(p1.in_arcs) & set(p2.out_arcs) != set():
            return

        self.logger.add_log(TransformationLog(p1.name, p2.name, 'a3', [t.name]))

        net = self.petri_net

        for i in p2.out_arcs:
            pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(p1, i.target, net)

        pm4py.objects.petri_net.utils.petri_utils.remove_transition(net, t)
        pm4py.objects.petri_net.utils.petri_utils.remove_place(net, p2)

        return

    def rule_a4(self, p1: PetriNet.Place, p2: PetriNet.Place, initial_marking):

        """
        Postset-Empty Place Simplification\n
        p1, p2: pm4py.PetriNet.Place\n
        p1 will be saved\n
        p2 will be destroyed\n
        """

        net = self.petri_net

        if p1.out_arcs != set() != p2.out_arcs:
            return

        if p1.in_arcs & p2.in_arcs != set():
            return

        for s_component in pm4py.objects.petri_net.utils.petri_utils.get_s_components_from_petri(net, initial_marking,
                                                                                                 pm4py.Marking()):
            if len(s_component) == 1:
                continue

            if not ((p1.name in s_component) == (p2.name in s_component)):
                return

        in_arcs = p2.in_arcs

        self.logger.add_log(TransformationLog(p1.name, p2.name, 'a4', in_arcs))

        for arc in in_arcs:
            pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(arc.source, p1, net)

        pm4py.objects.petri_net.utils.petri_utils.remove_place(net, p2)

        return

    def restore_rule(self):

        tl = self.logger.restore_rule()

        if tl is None:
            return False

        self.__restore_functions[tl.type](tl)

        return True

    def restore_rule_a1(self, tl):

        net = self.petri_net

        key_place = [i for i in net.places if i.name == tl.key_name][0]

        restored_place = pm4py.objects.petri_net.utils.petri_utils.add_place(net, tl.saved_name)

        for i in key_place.in_arcs:
            pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(i.source, restored_place, net)
        for i in key_place.out_arcs:
            pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(restored_place, i.target, net)

        return

    def restore_rule_a2(self, tl):

        net = self.petri_net

        key_transition = [i for i in net.transitions if i.name == tl.key_name][0]

        restored_transition = pm4py.objects.petri_net.utils.petri_utils.add_transition(net, tl.saved_name,
                                                                                       tl.saved_name)

        for i in key_transition.in_arcs:
            pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(i.source, restored_transition, net)
        for i in key_transition.out_arcs:
            pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(restored_transition, i.target, net)

        return

    def restore_rule_a3(self, tl):

        net = self.petri_net

        key_place = [i for i in net.places if i.name == tl.key_name][0]  # find p1

        # restore transition
        t = pm4py.objects.petri_net.utils.petri_utils.add_transition(net, tl.data[0], tl.data[0])

        # restore p2
        p2 = pm4py.objects.petri_net.utils.petri_utils.add_place(net, tl.saved_name)

        # restore arc between transition and p2
        pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(t, p2, net)

        # restore all arcs from p2
        for i in key_place.out_arcs:
            pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(p2, i.target, net)

        # removing arcs from p1
        out_arcs = key_place.out_arcs
        for arc in list(out_arcs):
            pm4py.objects.petri_net.utils.petri_utils.remove_arc(net, arc)

        # link p1 and transition
        pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(key_place, t, net)

        return

    def restore_rule_a4(self, tl):

        net = self.petri_net

        # restore place_2
        p2 = pm4py.objects.petri_net.utils.petri_utils.add_place(net, tl.saved_name)

        # find key place
        p1 = [place for place in net.places if place.name == tl.key_name][0]

        for arc in tl.data:
            # get transition
            transition = pm4py.objects.petri_net.utils.petri_utils.get_transition_by_name(net, arc.source.name)

            # add arc between transition and place
            pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(transition, p2, net)

            arc = [arc for arc in net.arcs if arc.source == transition and arc.target == p1][0]

            # delete arc
            pm4py.objects.petri_net.utils.petri_utils.remove_arc(net, arc)

        return
