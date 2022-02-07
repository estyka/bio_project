from Bio import SeqIO
import os
import matplotlib.pyplot as plt
import seaborn as sns

DIR = "C:\\Users\\97252\\Documents\\year_4\\project\\ncbi-genomes-fasta-2022-02-02\\unzipped"

def find_lens(dir):
    lens = []
    for filename in os.listdir(dir):
        f = os.path.join(dir, filename)
        seq_len = 0
        for seq_record in SeqIO.parse(f, "fasta"):
            seq_len += len(seq_record)
        lens.append(seq_len)
    return lens

lens = find_lens(DIR)
plt.hist(lens, color = 'blue', edgecolor = 'black',
         bins = int(len(lens)/5))

plt.title('Xanthomonas - Histogram of Genome Lengths')
plt.xlabel('Length')
plt.ylabel('Number of Genomes')

sns.kdeplot(lens, bw="scott")
plt.title('Xanthomonas - Density Plot of Genome Lengths')
plt.xlabel('Length')
plt.ylabel('Number of Genomes')