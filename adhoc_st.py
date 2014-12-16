import json
import os
import csv
import mistutils
import argparse

def arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-j', '--jsons', nargs='+', help='Path(s) to JSONs')
    parser.add_argument('-t', '--tests', nargs='+', help="Test name(s)")
    parser.add_argument('-o', '--out', help="Outpath for CSV")
    parser.add_argument('-q', '--quiet', action='store_true', help="Suppress error messages.")

    return parser.parse_args()

def make_st(dictionary):
    """Converts the dictionary of gene allele calls to a string.

        This allows it to be hashed for fast searching in a set.
    """
    order = sorted(dictionary.keys())
    l = []

    for i in order:
        l.append(dictionary[i])

    s = ' '.join(l)
    return s

def check_st(st, sts, test):
    """Checks to see if the ST is novel or not."""

    if test not in sts:
        sts[test] = {}

    if st not in sts[test]:
        try:
            sts[test][st] = max(sts[test].values()) + 1

        except ValueError:
            sts[test][st] = 1

    return sts[test][st]

def parse_json(genes): # Needs modification to allow for non-perfect data.

    """Returns allele matches for each gene.""" 
    d = {}

    for gene in genes:
        d[gene] = genes[gene]["AlleleMatch"]

    return d

def write_csv(genome_test, tests, outpath):
    """Writes the ST of each strain to a CSV.

    strain,st
    """
    headers = ['genome']
    for i in tests:headers.append(i)

    with open(outpath, 'w') as f:
        out = csv.writer(f)
        out.writerow(headers)
        for strain in genome_test:
            row = [strain]
            for test in tests:
                row.append(genome_test[strain][test])
            
            out.writerow(row)

def process(args):

    jsons = mistutils.get_jsons(args.jsons)
    sts = dict()

    genome_test = dict()

    for j in jsons:
        
        data = mistutils.load_json(j)
        
        for t in args.tests:

            try:
                for strain, genes in mistutils.loop_json_genomes(data, t):

                    if strain not in genome_test:
                        genome_test[strain] = {}

                    gene_calls = parse_json(genes)
                    calls = make_st(gene_calls)
                    st = check_st(calls, sts, t)

                    genome_test[strain][t] = st
            
            except KeyError:

                if not args.quiet:
                    message = "Skipping {} in {} as it doesn't see to be present. This is probably normal.".format(t, j)
                    print(message)

    write_csv(genome_test, args.tests, args.out)

def main():
    
    args = arguments()
    process(args)

if __name__ == '__main__':
    main()