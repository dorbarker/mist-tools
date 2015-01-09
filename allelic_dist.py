import argparse
import csv
import mistutils

def arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-j', '--jsons', nargs='+', required=True, help='Path(s) to JSONs')
    parser.add_argument('-t', '--tests', required=True, help="MIST test name")
    parser.add_argument('-o', '--out', required=True, help='Matrix outpath')

    return parser.parse_args()

def hamming_distance(strain1, strain2):
    """ Finds the Hamming Distance
        between two strains based on allele differences.
    """
    h_dist = 0
    order = strain1.keys()

    for item in order:
        if strain1[item] != strain2[item]:
            h_dist += 1

    return h_dist

def prepare_dist_matrix_csv(mat):
    """Perpares distance matrix dict as a 2D array."""

    order = mat.keys()
    prepped_mat = []
    row = ['genomes']
    row.extend(order)
    
    prepped_mat.append(row)

    for strain1 in order:
        
        row = [strain1]
        
        for strain2 in order:
            row.append(mat[strain1][strain2])

        prepped_mat.append(row)

    return prepped_mat

def write_dist_matrix_csv(outpath, mat):
    """Writes distance matrix to CSV."""

    prepped_mat = prepare_dist_matrix_csv(mat)

    with open(outpath, 'w') as f:
        out = csv.writer(f)
        for row in prepped_mat:
            out.writerow(row)

def build_matrix(strains_calls):
    """Constructs Hamming Distance matrix."""

    dist_mat = {}

    for strain1 in strains_calls:
        dist_mat[strain1] = {}
        
        for strain2 in strains_calls:
            
            h_dist = hamming_distance(strains_calls[strain1], strains_calls[strain2])
            dist_mat[strain1][strain2] = h_dist

    return dist_mat

def parse_json(genes, test):
    """Returns dict of allele matches."""
    
    d  = {}
   
    for gene in genes:
        
        if genes[gene]["BlastResults"] is None or genes[gene]["IsContigTruncation"]:
            
            d[gene] = "NA"
            print("Beware! {} is missing {}. This is treated as a valid 'allele' in the matrix.".format(genes[gene]["StrainName"], gene))
        
        else:
            d[gene] = genes[gene]["AlleleMatch"]

    return d

def process(args):

    strains_calls = {}
    jsons = mistutils.get_jsons(args.jsons)    

    for j in jsons:
        
        data = mistutils.load_json(j)
        for test in args.tests:
            
            for strain, genes in mistutils.loop_json_genomes(data, test):
                strains_calls[strain] = parse_json(genes, test)

    mat = build_matrix(strains_calls)

    write_dist_matrix_csv(args.out, mat)

def main():

    args = arguments()
    process(args)

if __name__ == '__main__':
    main()