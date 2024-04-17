# Sequence-renamer

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10949335.svg)](https://doi.org/10.5281/zenodo.10949335)


Accesory script to homogenize sequence IDs in multifasta files 

Different fasta file sources come with headers (this is, the sequences ID or description line) with an wide variety of formats. Indeed, often times headers may contain unusual characters, or even whitespaces, that may result in a hellish experience with downstream applications. In this sense, is quite usual to find different issues: some applications may trim the headers upon a given character (such as hmmer does with withespaces), change characters (e.g., PhyML changes "." by "_") or even more complicated, trim the header to a given number of characters (this is a common issue with the strict phylip format, which allows only 10 characters). 
As such, we recommend to homogenize fasta files headers before to start the Seqrutinator pipeline, including MUFASA (and, why not, as a general rule whatsoever). To do so, we provide the `seq_renamer.py` script

The script renames each of the sequences in a fasta file with a fixed digit string (by default, of 10 characters long). The user can add a key to identify the sequences with argument `-id`, which should be a letter code for the sequences in the fasta file (for example, `-id eco` to indicate the sequences come from _Escherichia coli_). The 10 digits will be completed with increasing numbers. An output file (`file_map`) will be generated, showing the corresponding original header to each new name. 

### Requirements
Sequence renamer requires python package Biopython (https://biopython.org/). 
Install with:
`pip install biopython`

### Examples
We have the proteome of _E. coli_, with 4959 entries:
```
$ grep -c ">" Ecoli.fasta                                                                         1 ↵  
4959
```
Note the headers contain a rather complex setting, with neven lenghts, and presence of whitespaces.

```
$ head -n 6 Ecoli.fasta                                      
>WP_001300467.1 MULTISPECIES: leu operon leader peptide [Enterobacteriaceae]
MTHIVRFIGLLLLNASSLRGRRVSGIQH
>WP_000478195.1 MULTISPECIES: DUF3302 domain-containing protein [Enterobacteriaceae]
MFLDYFALGVLIFVFLVIFYGIIILHDIPYLIAKKRNHPHADAIHVAGWVSLFTLHVIWPFLWIWATLYRPERGWGMQSHDSSVMQLQQRIAGLEKQLADIKSSSAE
>WP_000543457.1 MULTISPECIES: 2,3-dihydroxyphenylpropionate/2,3-dihydroxicinnamic acid 1,2-dioxygenase [Bacteria]
MHAYLHCLSHSPLVGYVDPAQEVLDEVNGVIASARERIAAFSPELVVLFAPDHYNGFFYDVMPPFCLGVGATAIGDFGSAAGELPVPVELAEACAHAVMKSGIDLAVSYCMQVDHGFAQPLEFLLGGLDKVPVLPVFINGVATPLPGFQRTRMLGEAIGRFTSTLNKRVLFLGSGGLSHQPPVPELAKADAHMRDRLLGSGKDLPASERELRQQRVISAAEKFVEDQRTLHPLNPIWDNQFMTLLEQGRIQELDAVSNEELSAIAGKSTHEIKTWVAAFAAISAFGNWRSEGRYYRPIPEWIAGFGSLSARTEN
```

Running:

```bash
$ python3 seq_renamer.py -i Ecoli.fasta -id eco
Execution Successful: 0:00:00.032205

```

Yields an output file `Ecoli_renamed.fsa` which headers look now like:

```bash
$ head -n 6 Ecoli_renamed.fsa                                                                          
>eco0000001
MTHIVRFIGLLLLNASSLRGRRVSGIQH
>eco0000002
MFLDYFALGVLIFVFLVIFYGIIILHDIPYLIAKKRNHPHADAIHVAGWVSLFTLHVIWPFLWIWATLYRPERGWGMQSHDSSVMQLQQRIAGLEKQLADIKSSSAE
>eco0000003
MHAYLHCLSHSPLVGYVDPAQEVLDEVNGVIASARERIAAFSPELVVLFAPDHYNGFFYDVMPPFCLGVGATAIGDFGSAAGELPVPVELAEACAHAVMKSGIDLAVSYCMQVDHGFAQPLEFLLGGLDKVPVLPVFINGVATPLPGFQRTRMLGEAIGRFTSTLNKRVLFLGSGGLSHQPPVPELAKADAHMRDRLLGSGKDLPASERELRQQRVISAAEKFVEDQRTLHPLNPIWDNQFMTLLEQGRIQELDAVSNEELSAIAGKSTHEIKTWVAAFAAISAFGNWRSEGRYYRPIPEWIAGFGSLSARTEN

```
In addition, a file termed `Ecoli_file_map` is created, containing an index of new and original names:

```bash
$ head -n 6 Ecoli_file_map                                                                             
eco0000001 	 WP_001300467.1 MULTISPECIES: leu operon leader peptide [Enterobacteriaceae]
eco0000002 	 WP_000478195.1 MULTISPECIES: DUF3302 domain-containing protein [Enterobacteriaceae]
eco0000003 	 WP_000543457.1 MULTISPECIES: 2,3-dihydroxyphenylpropionate/2,3-dihydroxicinnamic acid 1,2-dioxygenase [Bacteria]
eco0000004 	 WP_000291549.1 MULTISPECIES: lactose permease [Bacteria]
eco0000005 	 WP_000995441.1 MULTISPECIES: host-nuclease inhibitor Gam family protein [Enterobacteriaceae]
eco0000006 	 WP_000018633.1 MULTISPECIES: DUF2526 family protein YdcY [Enterobacterales]

```

We recommend a header name of 10 characters, with an index code (`-id`) of 3-4 characters. However, the user can use `-l` argument to extend the lenght of the header if desired. 
For example running:
```bash
$ python3 seq_renamer.py -i Ecoli.fasta -id esch_coli -l 15
$ head -n 6 Ecoli_renamed.fsa                                                                          
>esch_coli000001
MTHIVRFIGLLLLNASSLRGRRVSGIQH
>esch_coli000002
MFLDYFALGVLIFVFLVIFYGIIILHDIPYLIAKKRNHPHADAIHVAGWVSLFTLHVIWPFLWIWATLYRPERGWGMQSHDSSVMQLQQRIAGLEKQLADIKSSSAE
>esch_coli000003
MHAYLHCLSHSPLVGYVDPAQEVLDEVNGVIASARERIAAFSPELVVLFAPDHYNGFFYDVMPPFCLGVGATAIGDFGSAAGELPVPVELAEACAHAVMKSGIDLAVSYCMQVDHGFAQPLEFLLGGLDKVPVLPVFINGVATPLPGFQRTRMLGEAIGRFTSTLNKRVLFLGSGGLSHQPPVPELAKADAHMRDRLLGSGKDLPASERELRQQRVISAAEKFVEDQRTLHPLNPIWDNQFMTLLEQGRIQELDAVSNEELSAIAGKSTHEIKTWVAAFAAISAFGNWRSEGRYYRPIPEWIAGFGSLSARTEN
```
Note that headers in the renamed file have 15 characters long, which allows to better accomodate the index "ecoli". 


 
