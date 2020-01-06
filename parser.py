import argparse
import os
import sys
sys.path.append('./cmd_functions')

from cmd_functions import cmd_mgr
class StoreDictKeyPair(argparse.Action):
     def __call__(self, parser, namespace, values, option_string=None):
         my_dict = {}
         for kv in values.split(","):
             k,v = kv.split("=")
             x = 0
             try:
                 x = int(v)
             except:
                 x = float(v)
             my_dict[k] = x
         setattr(namespace, self.dest, my_dict)

class Parser():
    def __init__( self ):
        self.argparser = argparse.ArgumentParser()
        self.mgr = cmd_mgr.CmdMgr()

        self.methods = self.mgr.listMethods()
        subparsers = self.argparser.add_subparsers( metavar="==ACTIONS==", help="type \"exit\" to exit", dest='subparser_name')

        parser_Def = subparsers.add_parser( "Define",     help = "define the task")
        parser_E   = subparsers.add_parser( "Execute",    help = "execute the task")
        parser_S   = subparsers.add_parser( "Stop",       help = "stop the task")
        parser_Del = subparsers.add_parser( "Delete",     help = "delete the task")
        parser_M   = subparsers.add_parser( "Modify",     help = "modify the task")
        parser_L   = subparsers.add_parser( "List",       help = "show the list of [ tasks | methods ]")

        parser_Def.add_argument( "-task",   "--taskName",     help="name the task",                required=True,)
        parser_Def.add_argument( "-md",     "--method",       help="choose a method ",             required=True, choices=self.methods )
        parser_Def.add_argument( "-d",      "--database",     help="choose the database" ,         required=True,)
        parser_Def.add_argument( "-ms",     "--measurement",  help="choose the measurement" ,      required=True,)
        parser_Def.add_argument( "-f",      "--field",        help="choose the field" ,            required=True,)
        parser_Def.add_argument( "-s",      "--size",         help="specify the size" ,            default=3600 ,  type=int)
        parser_Def.add_argument( "-p",      "--params",       help="determine the parameters",     action=StoreDictKeyPair, metavar="param1=VAL1,param2=VAL2...")

        parser_E.add_argument  ( "-tid",    "--taskID"  ,     help="choose which task to execute", required=True,)

        parser_S.add_argument  ( "-tid",    "--taskID"  ,     help="choose which task to stop",    required=True,)

        parser_Del.add_argument( "-tid",    "--taskID"  ,     help="choose which task to stop",    required=True,)

        parser_M.add_argument  ( "-tid",    "--taskID"  ,     help="choose which task to modify",  required=True,)
        parser_M.add_argument  ( "-md",     "--method",       help="choose a method",                            )
        parser_M.add_argument  ( "-d",      "--database",     help="choose the database",                        )
        parser_M.add_argument  ( "-ms",     "--measurement",  help="choose the measurement",                     )
        parser_M.add_argument  ( "-f",      "--field",        help="choose the field",                           )
        parser_M.add_argument  ( "-s",      "--size",         help="specify the size" ,                 type=int,)

        parser_L.add_argument  ( "listname",                  help="choose which list to show",     choices=["methods", "tasks"], type=str.lower)

    def func( self, args ):
        if args.subparser_name == "Define":
            obj = vars( args )
            st  = args.method
            if self.methods[st]['checker'](obj['params']):
                dbrp,_ = self.mgr.defineTask(obj)
                for key,value in dbrp.items():
                    print(key+"="+value)
            else:
                print("parameters not allowed!!")
        elif args.subparser_name == "Execute":
            self.mgr.execTask( args.taskID )
        elif   args.subparser_name == "Stop":
            self.mgr.stopTask( args.taskID )
        elif args.subparser_name == "Delete":
            self.mgr.deleteTask( args.taskID )
        elif args.subparser_name == "Modify":
            obj = vars( args )
            filtered = {k: v for k, v in obj.items() if v is not None}
            obj.clear()
            obj.update(filtered)

            self.mgr.modifyTask( args.taskID, obj )
        elif args.subparser_name == "List":
            if args.listname == "methods":
                print( "Method Name" )
                print( "================")
                print( *self.mgr.listMethods(), sep = "\n" )
            elif args.listname == "tasks":
                self.mgr.listTasks()

def main():
    parser = Parser()
    cmds = []
    if len(sys.argv) >= 2:
        f = open(sys.argv[1],'r')
        cmds = f.readlines()
    while True:
        cmd = ""
        if cmds:
            cmd = cmds.pop( 0 )
            print("parser>>>$ "+cmd)
        else:
            cmd = input("parser>>>$ ")
        _cmd = cmd.split()
        if _cmd == ["exit"]:
            break
        try:
            args = parser.argparser.parse_args(_cmd)
            parser.func( args )
        except :
            print( "" )


if __name__ == '__main__':
    main()  