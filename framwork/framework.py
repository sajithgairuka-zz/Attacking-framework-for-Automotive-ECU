import argparse
import os
import sys
import lib.interface
import lib.time
import importlib
import errno
import traceback

MODULES_DIR = "modules"
VERSION = "0.1"

def show_script_header():
    """Show script header"""
    print(r"""
-------------------
CYBER1337s v{0}
-------------------
""".format(VERSION))

def fancy_header():
    return r"""------------------------------------------------------------------------------


 ██████╗██╗   ██╗██████╗ ███████╗██████╗  ██╗██████╗ ██████╗ ███████╗███████╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗███║╚════██╗╚════██╗╚════██║██╔════╝
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝╚██║ █████╔╝ █████╔╝    ██╔╝███████╗
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗ ██║ ╚═══██╗ ╚═══██╗   ██╔╝ ╚════██║
╚██████╗   ██║   ██████╔╝███████╗██║  ██║ ██║██████╔╝██████╔╝   ██║  ███████║
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ╚═╝╚═════╝ ╚═════╝    ╚═╝  ╚══════╝


------------------------------------------------------------------------------
""".format(VERSION)

def available_modules():
    blacklisted_files = ["__init__.py"]
    modules = [m[:-3] for m in os.listdir(MODULES_DIR) if m.endswith(".py") and m not in blacklisted_files]
    modules.sort()
    mod_str = "available modules:\n  "
    mod_str += ", ".join(modules)
    return mod_str

def parse_arguments():
    parser = argparse.ArgumentParser(description="{0}Attacking framework for Automotive ECU".format(fancy_header()),formatter_class=argparse.RawDescriptionHelpFormatter,epilog=available_modules())
    parser.add_argument("module",help="Name of the module to run")
    parser.add_argument("module_args", metavar="...", nargs=argparse.REMAINDER,help="Arguments to module")
    parser.add_argument("-i", dest="can_interface", default=None,help="force interface, e.g. 'can1' or 'vcan0'")
    parser.add_argument("-t", dest="can_fuzz_time",default=60,help= "this is only for fuzz.py" ,type=int)
    #sub= parser.add_subparsers(help='commands')
    #can_parsers=sub.add_parser("can_list", help='List of CAN Packet Attack')
    args = parser.parse_args()

    return args

def load_module(module_name):
    clean_mod_name = os.path.basename(module_name)
    package = "{0}.{1}".format(MODULES_DIR, clean_mod_name)
    try:
        py_mod = importlib.import_module(package)
        #print("Loaded module '{0}'\n".format(clean_mod_name))
        return py_mod
    except ImportError as e:
        #print("Load module failed: {0}".format(e))
        return None

def main():
    show_script_header()
    args = parse_arguments()
    if args.can_interface:
        lib.interface.DEFAULT_INTERFACE = args.can_interface
    if args.can_fuzz_time:
        lib.time.DEFAULT_TIME = args.can_fuzz_time

    mod = load_module(args.module)
    #if mod is not None:
    #    func_name = "module_main"
    #    func_exists = func_name in dir(mod) and callable(getattr(mod, func_name))
    #    if func_exists:
    #        mod.module_main(args.module_args)
    #    else:
    #        print("ERROR: Module '{0}' does not contain a '{1}' function.".format(args.module, func_name))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n attack stoped!")

    finally:
        print("")
