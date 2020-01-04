import argparse
import os
import sys
sys.path.append('./cmdFunctions')

from cmdFunctions import cmdMgr

argparser=argparse.ArgumentParser()
subparsers = argparser.add_subparsers( metavar="==ACTIONS==", help="type \"exit\" to exit", dest='subparser_name')

parser_Def = subparsers.add_parser( "Define",    help = "define the task")
parser_E   = subparsers.add_parser( "Execute",   help = "execute the task")
parser_S   = subparsers.add_parser( "Stop",      help = "stop the task")
parser_Del = subparsers.add_parser( "Delete",    help = "delete the task")
parser_M   = subparsers.add_parser( "Modify",    help = "modify the task")
parser_L   = subparsers.add_parser( "List",      help = "show the list of [ tasks | tests ]")

parser_Def.add_argument( "-task",   "--taskname",    help="name the task",                required=True,)
parser_Def.add_argument( "-test",   "--testname",    help="choose a test",                required=True,)
parser_Def.add_argument( "-d",      "--database",    help="choose the database" ,         required=True,)
parser_Def.add_argument( "-m",      "--measurement", help="choose the measurement" ,      required=True,)
parser_Def.add_argument( "-f",      "--field",       help="choose the field" ,            required=True,)
parser_Def.add_argument( "-s",      "--size",        help="specify the size" ,            default=3600 ,  type=int)

parser_E.add_argument  ( "-task",   "--taskname",    help="choose which task to execute", required=True,)

parser_S.add_argument  ( "-task",   "--taskname",    help="choose which task to stop",    required=True,)

parser_Del.add_argument( "-task",   "--taskname",    help="choose which task to stop",    required=True,)

parser_M.add_argument  ( "-task",   "--taskname",    help="choose which task to modify",  required=True,)
parser_M.add_argument  ( "-test",   "--testname",    help="choose a test",                              )
parser_M.add_argument  ( "-d",      "--database",    help="choose the database",                        )
parser_M.add_argument  ( "-m",      "--measurement", help="choose the measurement",                     )
parser_M.add_argument  ( "-f",      "--field",       help="choose the field",                           )
parser_M.add_argument  ( "-s",      "--size",        help="specify the size" ,                 type=int,)

parser_L.add_argument  ( "listname",                 help="choose which list to show",     choices=["test", "task"], type=str.lower)

while True:
    cmd = input("parser>>>$ ")
    _cmd = cmd.split()
    args = argparser.parse_args(_cmd)

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
        print ( args.subparser_name )
        print ( args.taskname )
    elif   args.subparser_name == "Stop":
        print ( args.subparser_name )
        print ( args.taskname )
    elif args.subparser_name == "Delete":
        print ( args.subparser_name )
        print ( args.taskname )
    elif args.subparser_name == "Modify":
        print ( args.subparser_name )
        print ( args.taskname )
        if args.database :   print ( args.database )
        if args.measurement :print ( args.measurement )
        if args.field :      print ( args.field )
        if args.size :       print ( args.size )
    elif args.subparser_name == "List":
        print ( args.subparser_name )
        print ( args.listname )
