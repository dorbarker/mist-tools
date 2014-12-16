import mistutils
import os
import json
import argparse

def arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--fastas', help = "Path to gene fasta directory")
    parser.add_argument('-j', '--jsons', nargs='+', required=True, help='Path(s) to JSONs')
    parser.add_argument('-t','--test', help = "MIST test name")
    parser.add_argument('-o','--out', help = "Destination for out file")
    parser.add_argument('--trunc', action='store_true', help="Reverses the output; i.e. 1 is a truncation and 0 is non-truncated.")

    return parser.parse_args()

def get_gene_order(genepath):
    """Returns an alphabetically ordered list of genes."""

    ordered_genes = []
    
    for i in os.listdir(genepath):
        genes.append(utils.basename(i))

    ordered_genes.sort()
    
    return ordered_genes

def binarize(genes, gene_order, trunc):
    """ Returns a binarized list of presence/absence. 
        Maintains the correct order.

        If trunc == False (default), 1 indicates the gene is present,
        and 0 is missing. If trunc == True, then 1 is for missing genes
        and 0 otherwise.
    """
    binarized = []

    np = int(trunc)
    p = int(not trunc)

    for gene in gene_order:
        if genes[gene]["BlastResults"] == None or genes[gene]["IsContigTruncation"]:
            binarized.append(np)
        else:
            binarized.append(p)

    return binarized

def write_out(genomes_genes, gene_order, outpath):
    """Writes the binary data to a CSV."""

    genome_order = sorted(genomes_genes.keys())

    out_table = ""
    
    for i in gene_order:
        out_table += ","+i
    
    out_table += '\n'

    for key in genome_order:
        
        out_table += key
        
        for value in genomes_genes[key]:
            out_table+= "," + str(value)
        
        out_table += '\n'
    
    with open(outpath, 'w') as f:
        f.write(out_table)

def process(args):

    genomes_genes = {}
    gene_order = get_gene_order(args.fastas)
    jsons = mistutils.get_jsons(args.jsons)

    for j in jsons:
        try:
            data = mistutils.load_json(j)
            for name, genes in mistutils.loop_json_genomes(data, args.test):
                binarized = binarize(data, args.test, gene_order, args.trunc)
                genomes_genes[name] = binarized
        
        except KeyError:
            print("Something is amiss with ".format(j))

    write_out(genomes_genes, gene_order, args.out)

def main():

    args = arguments()
    process(args)

if __name__ == '__main__':
    main()