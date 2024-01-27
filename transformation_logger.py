import os.path
import pickle
import pm4py.objects.petri_net.utils.petri_utils
import shutil


class TransformationLogger:
    """
    Logs transformations to permanent storage
    """

    def __init__(self, workdir='logs'):
        """
        :param workdir: directory to store logs
        """
        self.logs = []
        self.paths = []
        self.workdir = workdir
        if os.path.exists(workdir):
            shutil.rmtree(os.path.join(workdir), ignore_errors=False, onerror=None)
        os.mkdir(os.path.join(workdir))

    def add_log(self, transformation_log):
        self.logs.append(transformation_log)
        self._save()

    def _save(self):
        # stores the path of log in list
        self.paths.append(os.path.join(self.workdir, f'{self.logs[-1].saved_name}.pkl'))

        # stores loges to disk
        with open(self.paths[-1], 'wb') as file:
            pickle.dump(self.logs[-1], file)

    def restore_rule(self):
        """
        restores Rule
        :return: Rule if rule was restored or None
        """
        if len(self.paths) == 0:
            return None

        with open(self.paths[-1], 'rb') as file:
            log = pickle.load(file)
        self.paths.pop()
        return log


class TransformationLog:
    """
    Class for storing information about transformations
    """

    def __init__(self, key_name, saved_name, transformation_type, data=None):
        if data is None:
            data = []
        self.key_name = key_name
        self.saved_name = saved_name
        self.type = transformation_type
        self.data = data
