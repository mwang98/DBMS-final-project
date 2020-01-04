import shortuuid
import copy
import os
from defineTask import Task

class cmdMgr():
    def __init__( self ):
        self.tasks = []
        self.analysisMethod = ['ttest', 'fft']


    def defineTask( self, analysisType, argv ):
        input_arg = copy.deepcopy(argv)
        input_arg ['id'] = shortuuid.uuid()

        self.tasks.append( Task( input_arg, analysisType ) )
        task = self.tasks[-1]
        dbrp = task.getTick()
        task.define()

        return input_arg ['id']
    
    
    def execTask( self, id ):
        tasks = list(filter( (lambda task: task.info['id'] == id), self.tasks ))
        task  = tasks[0]
        task.enable()

    def stopTask( self, id ):
        tasks = list(filter( (lambda task: task.info['id'] == id), self.tasks ))
        task  = tasks[0]
        task.disable()

    def deleteTask( self, id ):
        tasks = list(filter( (lambda task: task.info['id'] == id), self.tasks ))
        task  = tasks[0]
        self.tasks.remove( task )

    def modifyTask( self, id, argv ):
        tasks = list(filter( (lambda task: task.info['id'] == id), self.tasks ))
        task  = tasks[0]
        task.modify( argv )
        dbrp  = task.getTick()
        task.define()
        return dbrp

    def listTasks( self ):
        print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<25} {:<15}". \
                format("Task Name", "Method", "Database", "Measurement", "Field", "ID", "Status"))
        print("="*112)
        for task in self.tasks:
            print( task )
    
    def listMethods( self ):
        return self.analysisMethod


obj = {
    "taskName": "monitorTemp",
    "database": "Mike",
    "measurement": "temperature",
    "field": "hotend",
    "size": "3600"
}
modified_obj = {
    "taskName": "modified",
}
def main():
    mgr = cmdMgr()
    ids  = []
    for i in range(2):
        idx = mgr.defineTask('ttest', obj)
        ids.append(idx)
    print("----------------")
    mgr.listTasks()

    mgr.execTask(ids[0])
    mgr.listTasks()
    os.system("kapacitor list tasks")

    mgr.modifyTask(ids[0], modified_obj) 
    mgr.listTasks()
    os.system("kapacitor list tasks")

    mgr.stopTask(ids[0])
    mgr.listTasks()
    os.system("kapacitor list tasks")

    mgr.deleteTask(ids[0])
    mgr.listTasks()
    os.system("kapacitor list tasks")


if __name__ == '__main__':
    main()  