#!/usr/bin/env python3

#################################################################
#   2nd release version                                         #
#################################################################

import argparse
from Bio import SeqIO
from datetime import datetime
import re
import glob
import pandas as pd
import os

startTime = datetime.now()

### Command Line Arguments ####################################################
parser = argparse.ArgumentParser()
parser.add_argument('-i', default='', help='Fasta file')
parser.add_argument('-t', default='', help='To activate processing of multiple fasta files. Indicate the name of tsv file with columns "file" and "code".')
parser.add_argument('-ext', default='*.fa', help='Extension of files if multiple fasta files are to be processed. Requires tsv file with columns "file", "code", "taxid"')
parser.add_argument('-id', default='', help='ID Key sequence name')
parser.add_argument('-taxid', default='', help='Tax ID (species level)')
parser.add_argument('-l', default=10, help='Seq name string lenght.')
parser.add_argument('--new_filename', default='', help='Enter a string or tsv column name to name output files.')

args = vars(parser.parse_args())

fasta_file = str(args['i'])
tsv_file = str(args['t'])
ext = str(args['ext'])
key = str(args['id'])
taxid = str(args['taxid'])
str_len = int(args['l'])
output_filename = str(args['new_filename'])
orig_str_len = int(args['l'])  # Store the original argument value
###############################################################################


numbers = re.compile(r'(\d+)')

def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

def input_files(ftype):
    list_of_files = sorted((glob.glob(ftype)), key=numericalSort)
    return list_of_files

def seqs_extractor(file_fasta):
    names = []
    seqs = []
    seq_num = []
    for seq_record in SeqIO.parse(file_fasta, "fasta"):
        names.append(seq_record.description)
        seqs.append(seq_record.seq)
    return names, seqs

#If no tsv file is provided, operate over a single fasta file indicated by -i
if tsv_file == '':
    real_fasta = str('.'.join(fasta_file.split('.')[:-1]))
    if fasta_file == '':
        print(f'If you want to run the script over a single file, you must indicate the input with -i')
        exit()
    names, seqs = seqs_extractor(fasta_file)

    max_seq = len(names)
    if str_len == 0:
        # Auto-adjust str_len
        str_len = len(key) + len(str(max_seq))
        print(f"Auto-adjusted -l to {str_len} to fit {max_seq} sequences with key '{key}'.")

    nk = str_len - len(key)
    if max_seq > 10**nk - 1:
        print(f"Error: -l value ({str_len}) is too small for {max_seq} sequences with key '{key}'. Increase -l.")
        exit(1)

    new_names = []

    for name, l in zip(names, list(range(1, len(names) + 1))):
        nk = str_len - len(key)
        nn = str(key) + str(l).zfill(nk)
        new_names.append(nn)

    if output_filename:
        # If a new filename is provided, use it for the output files
        out_file = output_filename
    else:
        # Otherwise, use the original fasta file name
        out_file = real_fasta
    
    with open(str(out_file) + "_rnmd.fsa", "w") as f1:
        for i, j in zip(new_names, seqs):
            f1.write(">" + str(i) + "\n")
            f1.write(str(j) + "\n")

    with open(str(out_file) + "_file_map", "w") as f2:
        for i, j in zip(new_names, names):
            print(i, '\t', j, '\t', taxid, file=f2)

    print(("Execution Successful: " + str((datetime.now() - startTime))))
else:
    if fasta_file != '':
        print(f'It seems you want to process several files with extension {ext}. In that case, -i argument must be empty.')
        exit()
    if key != '':
        print(f'It seems you want to process several files with extension {ext}. In that case, -id argument must be empty.')
        exit()

    # Load the fasta_code.tsv into a DataFrame
    fasta_code_df = pd.read_csv(tsv_file, sep='\t')

    # Check if required columns are present
    required_columns = {'file', 'code', 'taxid'}
    if not required_columns.issubset(fasta_code_df.columns):
        print(f"Error: The file {tsv_file} must contain the columns: {', '.join(required_columns)}")
        exit(1)

    list_of_fastas = input_files(ext)
    if not list_of_fastas:
        print("No files found with the extension provided. Check argument -ext")
        exit()

    for fasta_file_path in list_of_fastas:
        real_fasta = str('.'.join(fasta_file_path.split('.')[:-1])) 

        for index, row in fasta_code_df.iterrows():
            fasta = row['file']
            key = row['code']
            taxid = row['taxid']

            # Determine output file name
            if output_filename:
                if output_filename not in fasta_code_df.columns:
                    print(f"Error: The column '{output_filename}' does not exist in the TSV file. Please provide a valid column name with --new_filename.")
                    exit(1)
                out_file = str(row[output_filename])
                if not out_file or pd.isna(out_file):
                    print(f"Error: The column '{output_filename}' is empty for file '{fasta_file_path}'. Please provide a value in the TSV.")
                    exit(1)
            else:
                out_file = real_fasta

            if fasta == fasta_file_path:
                names, seqs = seqs_extractor(fasta_file_path)

                max_seq = len(names)
                # Use a local str_len for each file
                if orig_str_len == 0:
                    str_len = len(key) + len(str(max_seq))
                    print(f"Auto-adjusted -l to {str_len} to fit {max_seq} sequences with key '{key}' in file '{fasta_file_path}'.")
                else:
                    str_len = orig_str_len

                nk = str_len - len(key)
                if max_seq > 10**nk - 1:
                    print(f"Error: -l value ({str_len}) is too small for {max_seq} sequences with key '{key}' in file '{fasta_file_path}'. Increase -l.")
                    exit(1)

                new_names = []

                for name, l in zip(names, list(range(1, len(names) + 1))):
                    nk = str_len - len(key)
                    nn = str(key) + str(l).zfill(nk)
                    new_names.append(nn)

                with open(f"{out_file}_rnmd.fsa", "w") as f1:
                    for i, j in zip(new_names, seqs):
                        f1.write(">" + str(i) + "\n")
                        f1.write(str(j) + "\n")

                with open(f"{out_file}_file_map", "w") as f2:
                    for i, j in zip(new_names, names):
                        f2.write(f"{i}\t{j}\t{taxid}\n")

                print(f"Execution Successful for file {fasta_file_path}: {datetime.now() - startTime}")
                break  # Exit the inner loop once the matching file is processed

    print(f"Execution Successful: {datetime.now() - startTime}")