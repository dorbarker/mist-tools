import mistutils
import argparse
import csv

def arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-j', '--jsons', nargs='+', help='Path(s) to JSONs')
    parser.add_argument('-t', '--tests', nargs='+', help="Test name(s)")
    parser.add_argument('-o', '--out', help="Outpath for CSV")
    parser.add_argument('-q', '--quiet', action='store_true', help="Suppress error messages.")

    return parser.parse_args()

def allele_calls(genes):
    """Returns dictionary of allele calls
        with the gene name as the key.
    """

    d = {}

    for gene in genes:
        d[gene] = genes[gene]["AlleleMatch"]

    return d

def write_csv(genomes_test, test_genes, tests, outpath):
    """Writes JSON data to CSV format."""

    test_order = sorted(tests)

    with open(outpath, 'w') as f:
        out = csv.writer(f)

        header = ['genomes']
        for test in test_order:
            for gene in sorted(test_genes[test]):
                header.append(gene)
        out.writerow(header)

        for genome in genomes_test:
            
            row = [genome]
            
            for test in test_order:
                
                for gene in sorted(test_genes[test]):
                    row.append(genomes_test[genome][test][gene])

            out.writerow(row)

def process(args):

    jsons = mistutils.get_jsons(args.jsons)

    genomes_test = dict()
    test_genes = dict()

    for j in jsons:

        data = mistutils.load_json(j)
        
        for t in args.tests:
            try:
                
                if t not in test_genes:
                    test_genes[t] = set([])

                for strain, genes in mistutils.loop_json_genomes(data, t):
                    for gene in genes:
                        test_genes[t].add(gene)

                    if strain not in genomes_test:
                        genomes_test[strain] = {}

                    genomes_test[strain][t] = allele_calls(genes)
            
            except KeyError:

                if not args.quiet:
                    message = "Skipping {} in {} as it doesn't see to be present. This is probably normal.".format(t, j)
                    print(message)

    write_csv(genomes_test, test_genes, args.tests, args.out)

def main():

    args = arguments()
    process(args)

if __name__ == '__main__':
    main()