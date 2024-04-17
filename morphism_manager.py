import pm4py
import itertools

from pm4py import Marking
from itertools import permutations
from transformator import Transformator


class PetriNetMorphismManager:
    """
    This class is responsible for managing isomorphism and alpha-morphism between PetriNets.
    """

    _transformator = None

    class TransformationCollection:
        """
        This class collects transformations that provides alpha-morphism from PetriNet.
        """

        def __init__(self):
            self.rule_a1_list = []
            self.rule_a2_list = []
            self.rule_a3_list = []
            self.rule_a4_list = []

        def __len__(self):
            return len(self.rule_a1_list + self.rule_a2_list + self.rule_a3_list + self.rule_a4_list)

    @classmethod
    def get_transformations(cls, net: pm4py.PetriNet) -> TransformationCollection:
        """
        find all transformations
        :return: TransformationCollection containing all transformations that function can find
        """

        # creating all lists of transformations
        transformations = cls.TransformationCollection()

        transformations.rule_a1_list = list(itertools.combinations(net.places, 2))

        transformations.rule_a2_list = list(itertools.combinations(net.transitions, 2))

        transformations.rule_a3_list = [transition for transition in net.transitions if
                                        len(transition.in_arcs) == 1 and len(transition.out_arcs) == 1]

        transformations.rule_a4_list = list(
            itertools.combinations([place for place in net.places if not place.out_arcs], 2))

        return transformations

    class TransformationData:
        def __init__(self):
            self.start_number_of_places = None
            self.start_number_of_transitions = None
            self.result_number_of_places = None
            self.result_number_of_transitions = None

    @classmethod
    def start_transformations(cls, net, initial_marking=None, final_marking=None, display=False) -> TransformationData:
        """
        applies all transformations
        :param display: if true print steps of transformations
        :param net: pm4py.PetriNet
        :param initial_marking: list with initial markings
        :param final_marking: list with final markings
        :return: None
        """
        tr_data = cls.TransformationData()
        tr_data.start_number_of_places = len(net.places)
        tr_data.start_number_of_transitions = len(net.transitions)

        cls._transformator = Transformator(net)

        # loop flag
        flag = True

        transformations = cls.get_transformations(net)

        a4_bad_elements = {}

        def view_net():
            pm4py.view_petri_net(net, Marking(), None, decorations={
                                                                       place: {"label": place.name} for place in
                                                                       net.places
                                                                   } | {transition: {"label": transition.name} for
                                                                        transition in
                                                                        net.transitions}) if display and flag else None

        def apply_a1():
            nonlocal flag
            # applies rule_a1
            for places in transformations.rule_a1_list:
                flag += cls._transformator.rule_a1(places[0], places[1], initial_marking)

        def apply_a2():
            nonlocal flag
            # applies rule_a2
            for transitions in transformations.rule_a2_list:
                arguments = transitions

                # if all transitions labeled
                if all(transition.label for transition in transitions):
                    continue

                # if first one is not labeled and second one is labeled
                elif transitions[1].label:
                    # transitions[0], transitions[1] = transitions[1], transitions[0]
                    arguments = (transitions[1], transitions[0])
                # applying rule
                flag += cls._transformator.rule_a2(*arguments)

        def apply_a3():
            nonlocal flag
            # applies rule_a3
            for transition in transformations.rule_a3_list:
                # if transition is not labeled
                if not transition.label:
                    flag += cls._transformator.rule_a3(transition, initial_marking)

        def apply_a4():
            nonlocal a4_bad_elements
            nonlocal flag
            # applies rule_a4
            for places in [i for i in transformations.rule_a4_list if
                           i[1] not in a4_bad_elements.get(i[0], set()) and i[0] not in a4_bad_elements.get(i[1],
                                                                                                            set())]:
                if places[0] not in a4_bad_elements:
                    a4_bad_elements[places[0]] = set()
                if places[1] not in a4_bad_elements:
                    a4_bad_elements[places[1]] = set()

                if a4_bad_elements[places[0]].intersection(
                        a4_bad_elements[places[1]]) or not cls._transformator.rule_a4(
                    places[0], places[1],
                    initial_marking):
                    a4_bad_elements[places[0]].add(places[1])
                    a4_bad_elements[places[1]].add(places[0])
                else:
                    flag += 1

        flag_a4_checked = False

        # while we can apply rules:
        # flag displays that we applied at least 1 rule
        while flag and len(transformations) != 0:

            while flag:
                flag = False
                apply_a1()
                apply_a2()
                apply_a3()
                transformations = cls.get_transformations(net)
                # display
                view_net() if display and flag else None

            if not flag:
                if flag_a4_checked:
                    break
                else:
                    apply_a4()
                flag_a4_checked = not flag

            # updates transformations
            transformations = cls.get_transformations(net)

            # display
            view_net() if display and flag else None

            flag = False

        tr_data.result_number_of_places = len(net.places)
        tr_data.result_number_of_transitions = len(net.transitions)
        return tr_data

    @classmethod
    def check_alphamorphism(cls, s_net, s_initial_markings, t_net, t_initial_markings):
        """
        Checks alphamorphism between the two nets
        :param s_net: PetriNet
        :param s_initial_markings: list of PetriNet.Places
        :param t_net:  PetriNet
        :param t_initial_markings: list of PetriNet.Places
        :return: Boolean
        """
        # applies rules
        cls.start_transformations(s_net, s_initial_markings)
        # try to find isomorphism
        return cls.check_isomorphism(s_net, s_initial_markings, t_net, t_initial_markings)

    @classmethod
    def check_isomorphism(cls, s_net, s_initial_markings, t_net, t_initial_markings):
        """
        Checks isomorphism between the two PetriNets
        :param s_net: PetriNet
        :param s_initial_markings: list of PetriNet.Places
        :param t_net: PetriNet
        :param t_initial_markings: list of PetriNet.Places
        :return: Boolean
        """
        # if sizes of initial markings are not equal
        if len(s_initial_markings) != len(t_initial_markings):
            return False

        # if sizes of places are not equal
        if len(s_net.places) != len(t_net.places):
            return False

        # if sizes of transitions are not equal
        if len(s_net.transitions) != len(t_net.transitions):
            return False

        def check_isomorphism_between_targets(source_node, target_node):
            """
            Tries to apply map between two places/transitions
            :param source_node: PetriNet.Place/PetriNet.Transition
            :param target_node: PetriNet.Place/PetriNet.Transition
            :return: Boolean
            """

            nonlocal mapping

            # if the map is incorrect
            if source_node in mapping.keys() and mapping[source_node] != target_node:
                return False
            if source_node not in mapping.keys() and target_node in mapping.values():
                return False

            # it can be a cycle
            if source_node in mapping.keys():
                if all(arc.target in mapping.keys() for arc in source_node.out_arcs):
                    return True

            # if numbers of coming out arcs are not equal
            if len(source_node.out_arcs) != len(target_node.out_arcs) or len(source_node.in_arcs) != len(
                    target_node.in_arcs):
                return False

            # if there are no arcs from s_node and t_node
            if len(source_node.out_arcs) == 0:
                mapping[source_node] = target_node
                return True

            reset_map = mapping.copy()

            # tries to find the map
            for target in permutations([arc_target.target for arc_target in target_node.out_arcs]):

                # new part of the mapping
                new_map = {key: value for key, value in
                           zip([arc_target.target for arc_target in source_node.out_arcs], target)}

                # adds new part
                mapping |= new_map

                if all(check_isomorphism_between_targets(*the_map) for the_map in new_map.copy().items()):
                    return True

                # if there is no bijection remove added map
                mapping = reset_map.copy()
            return False

        # mapping from s_net to t_net
        for try_map in permutations(t_initial_markings):
            # maps s_initial to t_initial
            initial_mapping = {key: value for key, value in zip(s_initial_markings, try_map)}

            # union of initial_map and labels_map
            mapping = initial_mapping  # | labeled_mapping

            if all(check_isomorphism_between_targets(*initial_place_mapping) for initial_place_mapping in
                   initial_mapping.copy().items()):
                return True

        # there is no such bijection that proved isomorphism
        return False

    @classmethod
    def deep_net_copy(cls, net: pm4py.PetriNet, marking: pm4py.Marking) -> (pm4py.PetriNet, pm4py.Marking):
        new_net = net.__deepcopy__()
        new_marking = Marking()
        for i in marking:
            places = [j for j in new_net.places if j.name == i.name]
            for place in places:
                new_marking[place] = 1
        return new_net, new_marking

    @classmethod
    def restore_to_default(cls):
        """
        Restores all transitions that were applied to the PetriNet
        :return:
        """
        while cls._transformator.restore_rule():
            continue
