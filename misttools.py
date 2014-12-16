import argparse

import adhoc_st
import allelic_dist
import binarizer
import json2csv
import marker_maker
import update_alleles

def arguments():

    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers()

    # Shared arguments    
    json_opts = ('-j','--jsons')
    json_kw = {'nargs':'+', 'help':'Path(s) to JSONs'}

    fasta_opts = ('-f', '--fastas')
    fasta_kw = {'help': "Path to gene fasta directory"} 

    outpath_opts = ('-o', '--out')
    outpath_kw = {'help': 'Complete outpath'}
    
    testname_opts = ('-t', '--tests')
    testname_kw = {'nargs':'+','help':"MIST test name(s)"}
    
    ttype_opts = ('--testtype',)
    ttype_kw = {'choices' : ["allelic", "pcr"], 'help':"MIST test type"}

    truncs_opts = ('--trunc',)
    truncs_kw = {'action':'store_true', 'default' : 'store_false', 'help' : "Return truncations as True instead of false"}

    quiet_opts = ('-q', '--quiet')
    quiet_kw = {'action':'store_true', 'help': "Suppresses error output."}


    # Ad hoc Sequence Type Generation
    parser_st = commands.add_parser('st', help = "Generate qad hoc sequence types for your MLST-like scheme")
    parser_st.add_argument(*json_opts, **json_kw)
    parser_st.add_argument(*testname_opts, **testname_kw)
    parser_st.add_argument(*outpath_opts, **outpath_kw)
    parser_st.add_argument(*quiet_opts, **quiet_kw)
    parser_st.set_defaults(func=adhoc_st.process)


    # Distance Matrix Generator
    parser_dm = commands.add_parser('distmat', help = "Generate a Hamming Distance matrix between all strains \
                                            for MLST-like typing data")
    parser_dm.add_argument(*json_opts, **json_kw)
    parser_dm.add_argument(*testname_opts, **testname_kw)
    parser_dm.add_argument(*outpath_opts, **outpath_kw)
    parser_dm.set_defaults(func=allelic_dist.process)

    # Binarizer
    parser_bin = commands.add_parser('binarize', help = "Create a binary presence/absence table for genes in strains")
    parser_bin.add_argument(*json_opts, **json_kw)
    parser_bin.add_argument(*testname_opts, **testname_kw)
    parser_bin.add_argument(*outpath_opts, **outpath_kw)
    parser_bin.add_argument(*fasta_opts, **fasta_kw)
    parser_bin.add_argument(*truncs_opts, **truncs_kw)
    parser_bin.set_defaults(func=binarizer.process)

    # Marker Maker
    parser_mk = commands.add_parser('markers', help = "Auto-creates a .markers file for allelic MIST tests")
    parser_mk.add_argument(*fasta_opts, **fasta_kw)
    parser_mk.add_argument(*outpath_opts, **outpath_kw)
    parser_mk.add_argument(*testname_opts, **testname_kw)
    parser_mk.add_argument(*ttype_opts, **ttype_kw)
    parser_mk.set_defaults(func=marker_maker.process)

    # Allele File Updater
    parser_up = commands.add_parser('update', help = "Updates multifastas with newly discovered alleles")
    parser_up.set_defaults(func=update_alleles.process)
    parser_up.add_argument(*json_opts, **json_kw)
    parser_up.add_argument(*testname_opts, **testname_kw)
    parser_up.add_argument(*fasta_opts, **fasta_kw)

    # JSON to CSV converter
    parser_j2c = commands.add_parser('json2csv', help = "Converts JSONs to a single CSV")
    parser_j2c.set_defaults(func=json2csv.process)
    parser_j2c.add_argument(*json_opts, **json_kw)
    parser_j2c.add_argument(*testname_opts, **testname_kw)
    parser_j2c.add_argument(*outpath_opts, **outpath_kw)
    parser_j2c.add_argument(*quiet_opts, **quiet_kw)
   
    return parser.parse_args()

def main():

    args = arguments()

    args.func(args)

if __name__ == '__main__':
    main()