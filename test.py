import argparse
import sys
parser = argparse.ArgumentParser()

class StoreDictKeyPair(argparse.Action):
     def __call__(self, parser, namespace, values, option_string=None):
         my_dict = {}
         for kv in values.split(","):
             k,v = kv.split("=")
             my_dict[k] = v
         setattr(namespace, self.dest, my_dict)

parser.add_argument("-k", "--key_pairs", action=StoreDictKeyPair, metavar="KEY1=VAL1,KEY2=VAL2...")
parser.add_argument( "-p",      "--params",       help="determine the parameters",     action=StoreDictKeyPair, metavar="param1=VAL1,param2=VAL2...")

args = parser.parse_args(sys.argv[1:])
print ( sys.argv[1:] )
print ( vars(args) )
print ( args )