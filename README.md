# mist-tools

A suite of tools for parsing and manipulating JSON files output by [Microbial In Silico Typer](https://bitbucket.org/peterk87/mist/wiki/Home).

Currently, mist-tools depends upon Biopython for certain tasks. To get Biopython, follow the instructions below.

For all platforms:

```
pip install biopython
```

or

[Download](http://www.biopython.org) and compile from source

For Debian-like Linux:

```
sudo apt-get install python-biopython
```



## Components

***Ad hoc* Sequence Type Generator**

Creates MLST-like Sequence Types for your dataset. These currently make no reference to existing public definitions, and are defined based on the data given to it only. 

Each unique combination of alleles is an ST.

**Allelic Distance Matrix**

Calculates the [[Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance) between strains in a pair-wise. The resulting matrix is written to a CSV.

**Binarizer**

Generates binary (presence/absence) data for each gene in each genome and writes it to a CSV.

**JSON to CSV**

A tool for easy conversion of allelic JSON data to CSV format. Multiple assays can be run together, and the gene columns are grouped by test and ordered alphanumerically. 

**Marker Maker** 

Creates .markers files for MIST automatically. Currently only set up to work for allelic assays, but support for the other assay types is on the way!

**Update Allele Definitions**

Reads through JSONs created by MIST and finds novel alleles for allelic assays. These novel alleles are assigned a number and appended to the original input allele fastas.

Coming soon: In-place editing of the JSONs so there's no need to rerun MIST to get the new allele names in the JSONs.