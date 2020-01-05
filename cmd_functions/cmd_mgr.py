import shortuuid
import copy
import os
from define_task import Task

class CmdMgr():
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

        return dbrp
    
    
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
