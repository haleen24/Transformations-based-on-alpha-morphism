import pm4py
import morphism_manager
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to

if __name__ == '__main__':
    s_net = pm4py.PetriNet('net1')
    t_net = pm4py.PetriNet('net2')

    s_places = [pm4py.objects.petri_net.utils.petri_utils.add_place(s_net) for i in range(4)]

    t_places = [pm4py.objects.petri_net.utils.petri_utils.add_place(t_net) for i in range(3)]

    s_transitions = [pm4py.objects.petri_net.utils.petri_utils.add_transition(s_net) for i in range(3)]
    # s_transitions.append(pm4py.objects.petri_net.utils.petri_utils.add_transition(s_net, label="t0"))

    t_transitions = [pm4py.objects.petri_net.utils.petri_utils.add_transition(t_net) for i in range(3)]

    add_arc_from_to(s_places[0], s_transitions[0], s_net)
    add_arc_from_to(s_places[0], s_transitions[1], s_net)
    add_arc_from_to(s_transitions[1], s_places[1], s_net)
    add_arc_from_to(s_places[1], s_transitions[2], s_net)
    add_arc_from_to(s_transitions[2], s_places[2], s_net)
    add_arc_from_to(s_transitions[0], s_places[3], s_net)

    # answer = morphism_manager.PetriNetMorphismManager.check_alphamorphism(s_net, [s_places[0]], t_net, [t_places[0]])

    # print(answer)

    s_transitions[0].label = "t0"
    s_transitions[1].label = "t1"
    s_transitions[2].label = "t2"
    s_im = pm4py.Marking()
    s_im[s_places[0]] = 1
    # morphism_manager.PetriNetMorphismManager.start_transformations(s_net, im, display=False)

    # pm4py.view_petri_net(s_net)

    add_arc_from_to(t_places[0], t_transitions[0], t_net)
    add_arc_from_to(t_places[0], t_transitions[1], t_net)
    add_arc_from_to(t_transitions[0], t_places[2], t_net)
    add_arc_from_to(t_transitions[1], t_places[1], t_net)
    add_arc_from_to(t_places[1], t_transitions[2], t_net)
    add_arc_from_to(t_transitions[2], t_places[2], t_net)

    pm4py.view_petri_net(t_net)

    t_im = pm4py.Marking()
    t_im[t_places[0]] = 1

    answer = morphism_manager.PetriNetMorphismManager.check_alphamorphism(s_net, s_im, t_net, t_im)
    print(answer)
