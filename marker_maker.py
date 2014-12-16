import os
import argparse

def arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f','--fastas')
    parser.add_argument('-o','--out')
    parser.add_argument('-t', '--test')
    parser.add_argument('--testtype', choices = ["allelic", "pcr"])
    return parser.parse_args()

def prep_header():
    """Prepares the header for .markers file."""

    x = ["Marker Name", "Test Name", "Test Type", "Forward Primer",
         "Reverse Primer", "Amplicon Size (bp)",
         "Amplicon Range Factor (e.g. 0.1)",
         "Allelic Database Filename", "Repeat Size\n"]

    return '\t'.join(x)

def allelic_markers(fastas, test, outpath):
    """Generates a MIST .markers file for allelic assays."""

    out = prep_header()

    for fasta in (f for f in os.listdir(fastas) if '.f' in f):
        name = fasta[:fasta.index('.')]
        out += "{0}\t{1}\t1\t\t\t-1\t0\t{2}\t0\n".format(name, test, fasta)

    with open(outpath, 'w') as z:z.write(out)

def process(args):

    header = prep_header()

    if args.type == 'allelic':

        allelic_markers(args.fastas, args.testtype, args.out)

    if args.type == 'pcr':
        print("This is not yet functional!")

def main():
    
    args = ArgumentParsernts()
    process(args)

if __name__ == '__main__':
    main()