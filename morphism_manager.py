import pm4py
import itertools

from transformator import Transformator


class PetriNetMorphismManager:
    transformator = None

    class TransformationCollection:

        def __init__(self):
            self.rule_a1_list = []
            self.rule_a2_list = []
            self.rule_a3_list = []
            self.rule_a4_list = []

        def __len__(self):
            return len(self.rule_a1_list + self.rule_a2_list + self.rule_a3_list + self.rule_a4_list)

    @classmethod
    def get_transformations(cls, net: pm4py.PetriNet) -> TransformationCollection:
        transformations = cls.TransformationCollection()
        transformations.rule_a1_list = list(itertools.combinations(net.places, 2))
        transformations.rule_a2_list = list(itertools.combinations(net.transitions, 2))
        transformations.rule_a3_list = [transition for transition in net.transitions if
                                        len(transition.in_arcs) == 1 and len(transition.out_arcs) == 1]
        transformations.rule_a4_list = list(
            itertools.combinations([place for place in net.places if not place.out_arcs], 2))

        return transformations

    @classmethod
    def start_transformations(cls, net, initial_marking=None, final_marking=None):
        cls.transformator = Transformator(net)
        flag = True
        transformations = cls.get_transformations(net)
        while len(transformations) != 0 and flag:
            flag = False
            for places in transformations.rule_a1_list:
                flag += cls.transformator.rule_a1(places[0], places[1])
            for transitions in transformations.rule_a2_list:
                if all(transition.label for transition in transitions):
                    continue
                elif transitions[1].label:
                    transitions[0], transitions[1] = transitions[1], transitions[0]
                flag += cls.transformator.rule_a2(transitions[0], transitions[1])
            for transition in transformations.rule_a3_list:
                flag += cls.transformator.rule_a3(transition)
            for places in transformations.rule_a4_list:
                flag += cls.transformator.rule_a4(places[0], places[1], initial_marking, final_marking)
            transformations = cls.get_transformations(net)
            pm4py.view_petri_net(net, [], [])

    @classmethod
    def check_alpha_morphism(cls, s_net, s_initial_markings, t_net, t_initial_markings):
        cls.start_transformations(s_net, s_initial_markings)
        return cls.check_isomorphic(s_net, s_initial_markings, t_net, t_initial_markings)

    @classmethod
    def check_isomorphic(cls, s_net, s_initial_markings, t_net, t_initial_markings):
        return None

    @classmethod
    def restore_to_default(cls):
        while cls.transformator.restore_rule():
            continue
