import shortuuid
import copy

from defineTask import Task


class cmdMgr:

    def __init__(self):
        self.tasks = []
        self.analysisMethod = ['ttest', 'fft']

    def defineTask(self, analysisType, argv):
        argv['id'] = shortuuid.uuid()
        task = Task(argv, analysisType)
        self.tasks.append(copy.deepcopy(task))
        dbrp = task.getTick()
        task.defineTask()
        return dbrp

    def execTask(self, id):
        tasks = list(filter((lambda task: task.info['id'] == id), self.tasks))
        task = tasks[0]
        task.enableTask()

    def stopTask(self, id):
        tasks = list(filter((lambda task: task.info['id'] == id), self.tasks))
        task = tasks[0]
        task.disableTask()

    def deleteTask(self, id):
        tasks = list(filter((lambda task: task.info['id'] == id), self.tasks))
        task = tasks[0]
        task.deleteTask()
        self.tasks.remove(task)

    def listTasks(self):
        print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<25} {:<15}".format(
            "Task Name", "Method", "Database", "Measurement", "Field", "ID", "Status"))
        print("=" * 112)
        for task in self.tasks:
            print(task)

    def listMethods(self):
        return self.analysisMethod


obj = {
    "taskName": "monitorTemp",
    "database": "Mike",
    "measurement": "temperature",
    "field": "hotend",
    "size": "3600"
}


def main():
    mgr = cmdMgr()
    ids = []
    for i in range(10):
        idx = mgr.defineTask('ttest', obj)
        ids.append(idx)
    print(" ")


if __name__ == '__main__':
    main()
