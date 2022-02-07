import gzip
import shutil
import os

dir = "C:\\Users\\97252\\Documents\\year_4\\project\\ncbi-genomes-fasta-2022-02-02"

for filename in os.listdir(dir):
    f = os.path.join(dir, filename)
    if f[-3:] == ".gz":
        with gzip.open(f, "rb") as f_in:
            with open(f[:-3], "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)