import argparse

argparser = argparse.ArgumentParser()
subparsers = argparser.add_subparsers(help='actions that you can take', dest='subparser_name')

parser_D = subparsers.add_parser("Define", help="define the task")
parser_E = subparsers.add_parser("Execute", help="execute the task")
parser_S = subparsers.add_parser("Stop", help="stop the task")
parser_L = subparsers.add_parser("List", help="show the list of tasks")

parser_D.add_argument("-t", "--taskname", help="name the task", required=True, )
parser_D.add_argument("-d", "--database", help="choose the database", required=True, )
parser_D.add_argument("-m", "--measurement", help="choose the measurement", required=True, )
parser_D.add_argument("-f", "--field", help="choose the field", required=True, )
parser_D.add_argument("-s", "--size", help="specify the size", default=3600, type=int)

parser_E.add_argument("-t", "--taskname", help="choose which task to execute", required=True, )

parser_S.add_argument("-t", "--taskname", help="choose which task to stop", required=True, )

args = argparser.parse_args()

if args.subparser_name == "Stop":
    print(args.subparser_name)
    print(args.taskname)
elif args.subparser_name == "Execute":
    print(args.subparser_name)
    print(args.taskname)
elif args.subparser_name == "Define":
    print(args.subparser_name)
    print(args.taskname)
    print(args.database)
    print(args.measurement)
    print(args.field)
    print(args.size)
elif args.subparser_name == "List":
    print(args.subparser_name)
else:
    print(args)
