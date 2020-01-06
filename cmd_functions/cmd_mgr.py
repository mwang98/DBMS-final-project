import shortuuid
import copy
import os
from define_task import Task

class CmdMgr():
    def __init__( self ):
        self.tasks = []
        self.analysisMethod = {
            'ttest': {
                'alpha': "p-value threshold",
                'checker': self.ttestChecker
            }, 
            'fft':{
                'q': "frequency domain window",
                'z': "time domain window",
                'checker': self.fftChecker
            }}


    def defineTask( self, argv ):
        input_arg = copy.deepcopy(argv)
        input_arg ['id'] = shortuuid.uuid()

        self.tasks.append( Task( input_arg ) )
        task = self.tasks[-1]
        dbrp = task.getTick()
        task.define()

        return dbrp, input_arg ['id']
    
    
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

    def ttestChecker( self, params ):
        if params["alpha"] >= 0 and params["alpha"] <= 1:
            return True
        else:
            return False
    
    def fftChecker( self, params ):
        if type(params["q"]) is int and type(params["z"]) is int:
            return params["q"] > 0 and params["z"] > 0 
        return False

obj = {
        "method": "ttest",
        "taskName": "testTemp",
        "database": "dbdbdb",
        "measurement": "aaa",
        "field": "bbb",
        "size": 3600,
        "params":{
            "alpha": 0.0001
        }
    }
def main():
    idx = []
    mgr = CmdMgr()
    for i in range(10):
        _, id = mgr.defineTask(obj)
        idx.append(id)

    mgr.listTasks()

    mgr.execTask(idx[0])
    mgr.listTasks()

    mgr.stopTask(idx[0])
    mgr.listTasks()

    mgr.deleteTask(idx[0])
    mgr.listTasks()



if __name__ == "__main__":
    main()
