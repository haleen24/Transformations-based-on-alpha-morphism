import pm4py
import morphism_manager

if __name__ == '__main__':
    s_net = pm4py.PetriNet('net1')
    t_net = pm4py.PetriNet('net2')

    s_places = [pm4py.objects.petri_net.utils.petri_utils.add_place(s_net) for i in range(2)]

    t_places = [pm4py.objects.petri_net.utils.petri_utils.add_place(t_net) for i in range(2)]

    s_transitions = [pm4py.objects.petri_net.utils.petri_utils.add_transition(s_net) for i in range(1)]
    s_transitions.append(pm4py.objects.petri_net.utils.petri_utils.add_transition(s_net, label="t0"))

    t_transitions = [pm4py.objects.petri_net.utils.petri_utils.add_transition(t_net) for i in range(1)]

    pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(s_places[0], s_transitions[0], s_net)
    pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(s_transitions[0], s_places[1], s_net)
    pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(s_places[0], s_transitions[1], s_net)
    pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(s_transitions[1], s_places[1], s_net)

    pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(t_places[0], t_transitions[0], t_net)
    pm4py.objects.petri_net.utils.petri_utils.add_arc_from_to(t_transitions[0], t_places[1], t_net)

    pm4py.view_petri_net(t_net)

    answer = morphism_manager.PetriNetMorphismManager.check_alphamorphism(s_net, [s_places[0]], t_net, [t_places[0]])

    print(answer)
