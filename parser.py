import argparse
import os
import sys
sys.path.append('./cmdFunctions')

from cmdFunctions import cmdMgr

class Parser():
    def __init__( self ):
        self.argparser = argparse.ArgumentParser()
        subparsers = self.argparser.add_subparsers( metavar="==ACTIONS==", help="type \"exit\" to exit", dest='subparser_name')

        parser_Def = subparsers.add_parser( "Define",     help = "define the task")
        parser_E   = subparsers.add_parser( "Execute",    help = "execute the task")
        parser_S   = subparsers.add_parser( "Stop",       help = "stop the task")
        parser_Del = subparsers.add_parser( "Delete",     help = "delete the task")
        parser_M   = subparsers.add_parser( "Modify",     help = "modify the task")
        parser_L   = subparsers.add_parser( "List",       help = "show the list of [ tasks | tests ]")

        parser_Def.add_argument( "-task",   "--taskname", nargs="+",    help="name the task",                required=True,)
        parser_Def.add_argument( "-test",   "--testname", nargs="+",    help="choose a test",                required=True,)
        parser_Def.add_argument( "-d",      "--database", nargs="+",    help="choose the database" ,         required=True,)
        parser_Def.add_argument( "-m",      "--measurement", nargs="+", help="choose the measurement" ,      required=True,)
        parser_Def.add_argument( "-f",      "--field", nargs="+",       help="choose the field" ,            required=True,)
        parser_Def.add_argument( "-s",      "--size", nargs="+",        help="specify the size" ,            default=3600 ,  type=int)

        parser_E.add_argument  ( "-task",   "--taskname", nargs="+",    help="choose which task to execute", required=True,)

        parser_S.add_argument  ( "-task",   "--taskname", nargs="+",    help="choose which task to stop",    required=True,)

        parser_Del.add_argument( "-task",   "--taskname", nargs="+",    help="choose which task to stop",    required=True,)

        parser_M.add_argument  ( "-task",   "--taskname", nargs="+",    help="choose which task to modify",  required=True,)
        parser_M.add_argument  ( "-test",   "--testname", nargs="+",    help="choose a test",                              )
        parser_M.add_argument  ( "-d",      "--database", nargs="+",    help="choose the database",                        )
        parser_M.add_argument  ( "-m",      "--measurement", nargs="+", help="choose the measurement",                     )
        parser_M.add_argument  ( "-f",      "--field", nargs="+",       help="choose the field",                           )
        parser_M.add_argument  ( "-s",      "--size", nargs="+",        help="specify the size" ,                 type=int,)

        parser_L.add_argument  ( "listname", nargs="+",                 help="choose which list to show",     choices=["method", "task"], type=str.lower)

    def func( self, args ):
        mgr = cmdMgr.cmdMgr()
        if args.subparser_name == "Define":
            obj = {
                "taskName": args.taskname ,
                "database": args.database,
                "measurement": args.measurement,
                "field": args.field,
                "size": str(args.size)
            }
            mgr.defineTask('ttest', obj)
        elif args.subparser_name == "Execute":
            # print ( args.subparser_name )
            # print ( args.taskname )
            mgr.execTask( args.taskname )
        elif   args.subparser_name == "Stop":
            # print ( args.subparser_name )
            # print ( args.taskname )
            mgr.stopTask( args.taskname )
        elif args.subparser_name == "Delete":
            # print ( args.subparser_name )
            # print ( args.taskname )
            mgr.deleteTask( args.taskname )
        elif args.subparser_name == "Modify":
            # print ( args.subparser_name )
            # print ( args.taskname )
            # if args.database :   print ( args.database )
            # if args.measurement :print ( args.measurement )
            # if args.field :      print ( args.field )
            # if args.size :       print ( args.size )
            obj = {
                "database": args.database,
                "measurement": args.measurement,
                "field": args.field,
                "size": str(args.size)
            }
            mgr.modifyTask( args.taskname, obj)
        elif args.subparser_name == "List":
            if args.listname == ["method"]:
                # print( args.listname )
                mgr.listMethods()
            elif args.listname == ["task"]:
                # print( args.listname )
                mgr.listTasks()


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