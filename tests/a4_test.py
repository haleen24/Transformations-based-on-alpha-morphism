import pm4py
from pm4py import Marking
import transformator
from pm4py.objects.petri_net.utils import petri_utils
from pm4py.objects.petri_net.utils import reachability_graph

from pm4py.objects.petri_net.utils.petri_utils import add_arc_from_to
from pm4py.objects.petri_net.utils.petri_utils import add_place
from pm4py.objects.petri_net.utils.petri_utils import add_transition
from pm4py.visualization.transition_system import visualizer as ts_visualizer

if __name__ == "__main__":
    net = pm4py.PetriNet("tmp")

    places = [add_place(net, f'p{i}') for i in range(6)]

    transitions = [add_transition(net, f't{i}', f't{i}') for i in range(7)]

    add_arc_from_to(places[0], transitions[0], net)
    add_arc_from_to(places[0], transitions[1], net)
    add_arc_from_to(transitions[0], places[1], net)
    add_arc_from_to(transitions[1], places[2], net)

    initial_marking = Marking()
    initial_marking[places[0]] = 1

    pm4py.objects.petri_net.utils.petri_utils.remove_unconnected_components(net)

    # pm4py.view_petri_net(net, initial_marking)

    trans = transformator.Transformator(net)

    trans.rule_a4(places[1], places[2], initial_marking, [])

    pm4py.view_petri_net(net, initial_marking)

    while trans.restore_rule():
        continue

    pm4py.view_petri_net(net, initial_marking)
    # ts = reachability_graph.construct_reachability_graph(net, initial_marking)
    # gviz = ts_visualizer.apply(ts, parameters={ts_visualizer.Variants.VIEW_BASED.value.Parameters.FORMAT: "svg"})
    # ts_visualizer.view(gviz)
