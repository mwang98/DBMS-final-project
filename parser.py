import argparse
import os
import sys
sys.path.append('./cmdFunctions')

from cmdFunctions import cmdMgr

class Parser():
    def __init__( self ):
        self.argparser = argparse.ArgumentParser()
        self.mgr = cmdMgr.cmdMgr()
        subparsers = self.argparser.add_subparsers( metavar="==ACTIONS==", help="type \"exit\" to exit", dest='subparser_name')

        parser_Def = subparsers.add_parser( "Define",     help = "define the task")
        parser_E   = subparsers.add_parser( "Execute",    help = "execute the task")
        parser_S   = subparsers.add_parser( "Stop",       help = "stop the task")
        parser_Del = subparsers.add_parser( "Delete",     help = "delete the task")
        parser_M   = subparsers.add_parser( "Modify",     help = "modify the task")
        parser_L   = subparsers.add_parser( "List",       help = "show the list of [ tasks | tests ]")

        parser_Def.add_argument( "-task",   "--taskname",     help="name the task",                required=True,)
        parser_Def.add_argument( "-md",     "--method",       help="choose a method",              required=True,)
        parser_Def.add_argument( "-d",      "--database",     help="choose the database" ,         required=True,)
        parser_Def.add_argument( "-ms",     "--measurement",  help="choose the measurement" ,      required=True,)
        parser_Def.add_argument( "-f",      "--field",        help="choose the field" ,            required=True,)
        parser_Def.add_argument( "-s",      "--size",         help="specify the size" ,            default=3600 ,  type=int)

        parser_E.add_argument  ( "-task",   "--taskname",     help="choose which task to execute", required=True,)

        parser_S.add_argument  ( "-task",   "--taskname",     help="choose which task to stop",    required=True,)

        parser_Del.add_argument( "-task",   "--taskname",     help="choose which task to stop",    required=True,)

        parser_M.add_argument  ( "-task",   "--taskname",     help="choose which task to modify",  required=True,)
        parser_M.add_argument  ( "-md",     "--method",       help="choose a method",                            )
        parser_M.add_argument  ( "-d",      "--database",     help="choose the database",                        )
        parser_M.add_argument  ( "-ms",     "--measurement",  help="choose the measurement",                     )
        parser_M.add_argument  ( "-f",      "--field",        help="choose the field",                           )
        parser_M.add_argument  ( "-s",      "--size",         help="specify the size" ,                 type=int,)

        parser_L.add_argument  ( "listname",                  help="choose which list to show",     choices=["method", "task"], type=str.lower)

    def func( self, args ):
        if args.subparser_name == "Define":
            obj = {
                "taskName": args.taskname,
                "database": args.database,
                "measurement": args.measurement,
                "field": args.field,
                "size": str(args.size)
            }
            self.mgr.defineTask(args.method, obj)
        elif args.subparser_name == "Execute":
            # print ( args.subparser_name )
            # print ( args.taskname )
            self.mgr.execTask( args.taskname )
        elif   args.subparser_name == "Stop":
            # print ( args.subparser_name )
            # print ( args.taskname )
            self.mgr.stopTask( args.taskname )
        elif args.subparser_name == "Delete":
            # print ( args.subparser_name )
            # print ( args.taskname )
            self.mgr.deleteTask( args.taskname )
        elif args.subparser_name == "Modify":
            # print ( args.subparser_name )
            # print ( args.taskname )
            # if args.database :   print ( args.database )
            # if args.measurement :print ( args.measurement )
            # if args.field :      print ( args.field )
            # if args.size :       print ( args.size )
            obj = {
                "method":args.method,
                "database": args.database,
                "measurement": args.measurement,
                "field": args.field,
                "size": str(args.size)
            }
            self.mgr.modifyTask( args.taskname, obj)
        elif args.subparser_name == "List":
            if args.listname == "method":
                # print( args.listname )
                # print( self.mgr.listMethods() )
                print( "Method Name" )
                print( "================")
                print( *self.mgr.listMethods(), sep = "\n" )
            elif args.listname == "task":
                # print( args.listname )
                self.mgr.listTasks()

def main():
    parser = Parser()
    while True:
        cmd = input("parser>>>$ ")
        if cmd == "exit":
            break
        _cmd = cmd.split()
        try:
            args = parser.argparser.parse_args(_cmd)
            parser.func( args )
        except:
            print("")


if __name__ == '__main__':
    main()  