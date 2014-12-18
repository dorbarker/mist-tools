from Bio import SeqIO
import mistutils
import os, sys, fileinput
import argparse

def arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--fastas', help = "Path to gene fasta directory")
    parser.add_argument('-j', '--jsons', nargs='+', required=True, help='Path(s) to JSONs')
    parser.add_argument('-t', '--test', required = True, help = "MIST test name")

    return parser.parse_args()

def init_sets(fastapath):
    """Gets the known alleles and stores them in a set.

    """
    st = set()
    with open (fastapath, 'r') as f:

        for rec in SeqIO.parse(f, 'fasta'):
            sq = str(rec.seq)
            st.add(sq)

    return st

def get_known_alleles(allele_dir):
    """Stores known alleles as a dict full of sets.
    """
    known_alleles = {}

    alleles = [f for f in os.listdir(allele_dir) if '.f' in f]

    for allele in alleles:
        
        name = mistutils.basename(allele)

        path = os.path.join(allele_dir, allele)

        known = init_sets(path)
        known_alleles[name] = known

    return known_alleles

def novel_alleles(genes, test):
    """Generator function that iterates over the JSONs and 
        yields potential novel alleles.

        Works for allelic or PCR-type assays.
    """

    for gene in genes:
        trunc = genes[gene]["IsContigTruncation"]

        if genes[gene]["BlastResults"] != None:
            
            match = genes[gene]["CorrectMarkerMatch"]
            subjaln = genes[gene]["BlastResults"]["SubjAln"]
            if not (trunc or match) and len(subjaln) > 0:
                yield gene, subjaln

        else:
            if genes[gene]["ForwardPrimerBlastResult"] != None:
                if genes[gene]["ReversePrimerBlastResult"] != None:
                    if (not trunc) and len(genes[gene]["Amplicon"]) > 0:
                        yield gene, genes[gene]["Amplicon"]

def get_novel_alleles(jsons, known_alleles, tests):
    """Loops over JSONs, finds novel alleles,
        and tracks them in a dictionary.
    """

    
    novel = {}

    for json in jsons:
        data = mistutils.load_json(json)
        
        for test in tests:

            for strain, genes in mistutils.loop_json_genomes(data, test):
            
                for gene, potential in novel_alleles(genes, test):

                    if potential not in known_alleles[gene]:
                        
                        try:
                            novel[gene].append(potential)
                        except KeyError:
                            novel[gene] = [potential]

                        known_alleles[gene].add(potential)

    return novel

def write_novel_alleles(alleles, novel):
    """Appends new alleles to multifasta file.
    """
    for gene in novel:

        filename = os.path.join(alleles, gene + '.fasta')

        with open(filename, 'a') as f:
            for allele in novel[gene]:
                f.write('>placeholder\n')
                f.write(allele + "\n")

        fix_headers(filename)
        
def fix_headers(filename):
    """Fixes the headers to be the basename and a incrementing allele number.
    e.g. >1

    """

    counter = 1

    for line in fileinput.input(filename, inplace = True):
        if '>' in line:
            line = line.replace(line, '>'+str(counter)+'\n')
            counter += 1
        sys.stdout.write(line)

def process(args):

    jsons = mistutils.get_jsons(args.jsons)

    known = get_known_alleles(args.fastas)

    novel = get_novel_alleles(jsons, known, args.tests)

    write_novel_alleles(args.fastas, novel)

def main():
    
    args = arguments()
    process(args)

if __name__ == '__main__':
    main()