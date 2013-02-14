#! /usr/bin/python

import logging
from optparse import OptionParser
import sys

import dispatcher

def configure_logging():
    logging.basicConfig(format="", level=logging.DEBUG)

def validate_args(args, options):
    if len(args) < 2:
        logging.error("No input or output filename specified")
        return False
    elif not options.pack and not options.unpack:
        logging.error("You must specify either -p or -u.")
        return False
    return True

def main(args):
    configure_logging()
    oparser = OptionParser(usage="%prog [options] input_file output_file",
        version="1.0")

    oparser.add_option("-p", "--pack", action="store_true",
        dest="pack", default=False,
        help="Pack loose files into game resources.")
    oparser.add_option("-u", "--unpack", action="store_true",
        dest="unpack", default=False,
        help="Unpack game resources into loose files.")

    options, args = oparser.parse_args()

    if not validate_args(args, options):
        oparser.print_help()
        return 1

    try:
        fileDispatcher = dispatcher.FileDispatcher()
        fileDispatcher.dispatch_args(args, options)
    # TODO: add sepcific exception handling if required.
    except Exception, e:
        logging.exception("Unhandled exception: \n")
        return 2

    logging.info('Done!')
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))