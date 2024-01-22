import os.path
import pickle

import pm4py.objects.petri_net.utils.petri_utils


class TransformationLogger:

    def __init__(self):
        self.logs = []
        self.paths = []

    def add_log(self, transformation_log):
        self.logs.append(transformation_log)
        self.__save()

    def __save(self):
        self.paths.append(os.path.join('logs', f'{self.logs[-1].saved_name}.pkl'))
        with open(self.paths[-1], 'wb') as file:
            pickle.dump(self.logs[-1], file)

    def restore_rule(self):
        if len(self.paths) == 0:
            return None

        with open(self.paths[-1], 'rb') as file:
            place = pickle.load(file)
        self.paths.pop()
        return place


class TransformationLog:

    def __init__(self, key_name, saved_name, transformation_type, data=None):
        if data is None:
            data = []
        self.key_name = key_name
        self.saved_name = saved_name
        self.type = transformation_type
        self.data = data
