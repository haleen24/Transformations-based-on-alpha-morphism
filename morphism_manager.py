import pm4py
import itertools

from pm4py.objects.petri_net.utils import initial_marking

from transformator import Transformator


class PetriNetMorphismManager:
    """
    This class is responsible for managing isomorphism and alphamorphism between PetriNets.
    """

    _transformator = None

    class TransformationCollection:
        """
        This class collects transformations that provides alphamorphism from PetriNet.
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

    @classmethod
    def start_transformations(cls, net, initial_marking, final_marking=None, display=False):
        """
        applies all transformations
        :param net: Pm4py.PetriNet
        :param initial_marking: list with initial markings
        :param final_marking: list with final markings
        :return: None
        """
        cls._transformator = Transformator(net)

        # loop flag
        flag = True

        transformations = cls.get_transformations(net)

        # while we can apply rules:
        while len(transformations) != 0 and flag:

            # flag displays that we applied at least 1 rule
            flag = False

            # applies rule_a1
            for places in transformations.rule_a1_list:
                flag += cls._transformator.rule_a1(places[0], places[1])

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

            # applies rule_a3
            for transition in transformations.rule_a3_list:
                # if transition is not labeled
                if not transition.label:
                    flag += cls._transformator.rule_a3(transition)

            # applies rule_a4
            for places in transformations.rule_a4_list:
                flag += cls._transformator.rule_a4(places[0], places[1], initial_marking, final_marking)

            # updates transformations
            transformations = cls.get_transformations(net)

            # display
            pm4py.view_petri_net(net, None, None) if display else None

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

            # it can be a cycle
            if source_node in mapping.keys():
                if all(arc.target in mapping.keys() for arc in source_node.out_arcs):
                    return True

            # if numbers of coming out arcs are not equal
            if len(source_node.out_arcs) != len(target_node.out_arcs):
                return False

            # if there are no arcs from s_node and t_node
            if len(source_node.out_arcs) == 0:
                mapping[source_node] = target_node
                return True

            # tries to find the map
            for target in permutations([arc_target.target for arc_target in target_node.out_arcs]):

                # new part of the mapping
                new_map = {key: value for key, value in
                           zip([arc_target.target for arc_target in source_node.out_arcs], target)}

                # adds new part
                mapping |= new_map

                if all(check_isomorphism_between_targets(*the_map) for the_map in new_map.items()):
                    return True

                # if there is no bijection remove added map
                mapping -= new_map
            return False

        # finds all transitions with same labels in two nets
        labeled_mapping = {key: value for key in s_net.transitions for value in t_net.transitions if
                           key.label == value.label and key.label is not None}

        from itertools import permutations

        # mapping from s_net to t_net
        for try_map in permutations(t_initial_markings):
            # maps s_initial to t_initial
            initial_mapping = {key: value for key, value in zip(s_initial_markings, try_map)}

            # union of initial_map and labels_map
            mapping = initial_mapping | labeled_mapping

            # if the map was correct
            if all(check_isomorphism_between_targets(*initial_place_mapping) for initial_place_mapping in
                   mapping.copy().items()):
                return True

        # there is no such bijection that proved isomorphism
        return False

    @classmethod
    def restore_to_default(cls):
        """
        Restores all transitions that were applied to the PetriNet
        :return:
        """
        while cls._transformator.restore_rule():
            continue
