import pm4py
import morphism_manager
from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to as add_arc

if __name__ == '__main__':
    net = pm4py.PetriNet('net')
    places = [pm4py.objects.petri_net.utils.petri_utils.add_place(net) for i in range(8)]
    transitions = [pm4py.objects.petri_net.utils.petri_utils.add_transition(net) for i in range(6)]

    add_arc(places[0], transitions[0], net)
    add_arc(places[0], transitions[1], net)

    add_arc(places[1], transitions[2], net)
    add_arc(places[1], transitions[3], net)

    add_arc(transitions[0], places[2], net)
    add_arc(transitions[1], places[3], net)
    add_arc(transitions[2], places[4], net)
    add_arc(transitions[3], places[5], net)

    add_arc(places[2], transitions[4], net)
    add_arc(places[3], transitions[5], net)
    add_arc(places[4], transitions[4], net)
    add_arc(places[5], transitions[5], net)

    add_arc(transitions[4], places[6], net)
    add_arc(transitions[5], places[7], net)

    initial_marking = pm4py.Marking()
    initial_marking[places[0]] = 1
    initial_marking[places[1]] = 1

    pm4py.write_pnml(net, initial_marking, [], 'nets/test3.pnml')
    pm4py.view_petri_net(net, initial_marking)

    manager = morphism_manager.PetriNetMorphismManager()

    manager.start_transformations(net, initial_marking)


