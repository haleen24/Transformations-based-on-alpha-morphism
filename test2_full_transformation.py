import pm4py
import morphism_manager
import transformator

if __name__ == '__main__':
    net, marking1, marking2 = pm4py.read.read_pnml('nets/test_net.pnml')
    pm4py.view_petri_net(net)
    marking2 = pm4py.Marking()
    for i in [i for i in net.places if i.out_arcs == set()]:
        marking2[i] = 1

    trans = transformator.Transformator(net)
    print(trans._get_s_component(net, dict(), dict()))
    # morphism_manager.PetriNetMorphismManager.start_transformations(net, marking1, marking2)
    # print(marking1, marking2)
