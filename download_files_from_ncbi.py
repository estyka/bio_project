#https://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/Xanthomonas_oryzae/representative/GCF_001021915.1_ASM102191v1/
# next step - option to download only for specific bacteria
from ftplib import FTP
import os, sys, os.path
import time

SERVER_PATH = r"ftp.ncbi.nlm.nih.gov"
SERVER_BACTERIA_LOCATION = r"/genomes/refseq/bacteria/"
SAVE_FOLDER = r"C:\Users\97252\Documents\year_4\bio_project_data\download_files_from_ncbi"

ALL_ASSEMBLY_PREFIX = r"latest_assembly_versions/"
NUMBER_OF_TRIES = 500
MAX_NUM_ERRORS_IN_TRY = 50

bacteria_input = r"Xanthomonas_oryzae" #later: check if runs on lowercase

def get_genomes(num_try: int):
    print(f'starting num_try {num_try}')

    ftp = FTP(SERVER_PATH)

    # print('finished connection')

    ftp.login()
    print('logged in')

    ftp.cwd(SERVER_BACTERIA_LOCATION)
    print(f'changed dir to {SERVER_BACTERIA_LOCATION}')

    bacteria_folders = ftp.nlst(SERVER_BACTERIA_LOCATION)  # get folders within the directory
    bacteria_folders_clean = [filename for filename in bacteria_folders if bacteria_input in os.path.basename(filename)] #get folders of searched bacteria

    num_errors_in_try = 0
    num_already_downloaded = 0

    local_folder = os.path.join(os.path.normpath(SAVE_FOLDER), os.path.basename(os.path.normpath(bacteria_input)))
    os.makedirs(local_folder, exist_ok=True)  # I think makedir is enough (doens't need to be makedirs)

    for i, bacteria in enumerate(bacteria_folders_clean):
        file = None
        try:
            all_assembly_folder = bacteria + "/" + ALL_ASSEMBLY_PREFIX # find out if there is a way of downloading this whole folder in one go (even better - of downloading only the files in this folder that end with _genomic.fna.gz)
            assemblies = ftp.nlst(all_assembly_folder)
            for j in range(len(assemblies)):
                #files = ftp.nlst(assemblies[j])
                try:
                    file2download = f'{assemblies[j]}/{os.path.split(assemblies[j])[-1]}_genomic.fna.gz'
                    local_filename = os.path.join(local_folder, os.path.basename(os.path.normpath(file2download)))
                    file = open(local_filename, 'wb')
                    ftp.retrbinary('RETR ' + file2download, file.write)
                    #print(f'finished downloading file {local_filename}')
                    num_errors_in_try = 0
                except:
                    print(f'error downloading fasta file for {assemblies[j]} of bacteria {bacteria}')
                if file != None:
                    file.close()
                try:
                    file2download = f'{assemblies[j]}/{os.path.split(assemblies[j])[-1]}_assembly_stats.txt'
                    local_filename = os.path.join(local_folder, os.path.basename(os.path.normpath(file2download)))
                    file = open(local_filename, 'wb')
                    ftp.retrbinary('RETR ' + file2download, file.write)
                    #print(f'finished downloading file {local_filename}')
                    num_errors_in_try = 0
                except:
                    print(f'error downloading stats file for {assemblies[j]} of bacteria {bacteria}')
                if file != None:
                    file.close()
                num_already_downloaded += 1
        except:
            num_errors_in_try += 1
            print(f'error downloading bacteria {bacteria}')
            if num_errors_in_try >= MAX_NUM_ERRORS_IN_TRY:
                break

    print(f'num_try {num_try}, already_downloaded {num_already_downloaded} | len {len(bacteria_folders_clean)}')
    ftp.quit()  # This is the “polite” way to close a connection


start = time.time()
print(f"Starting to download assmeblies of bacteria {bacteria_input}")
for i in range(NUMBER_OF_TRIES):
    try:
        get_genomes(i)
    except Exception as e:
        print(e)
        print(f'finished try number: {i} out of {NUMBER_OF_TRIES}')
end = time.time()
print(f"Runtime of the program is {end - start}")
