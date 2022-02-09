#https://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/Xanthomonas_oryzae/representative/GCF_001021915.1_ASM102191v1/
# next step - option to download only for specific bacteria
from ftplib import FTP
import os, sys, os.path

SERVER_PATH = r"ftp.ncbi.nlm.nih.gov"
SERVER_BACTERIA_LOCATION = r"/genomes/refseq/bacteria/"
SAVE_FOLDER = r"C:\Users\97252\Documents\year_4\bio_project_data\download_files_from_ncbi"

ALL_ASSEMBLY_PREFIX = r"latest_assembly_versions/"
NUMBER_OF_TRIES = 500
MAX_NUM_ERRORS_IN_TRY = 50


def get_genomes(num_try: int):
    print(f'starting num_try {num_try}')

    ftp = FTP(SERVER_PATH)

    # print('finished connection')

    ftp.login()
    print('logged in')

    ftp.cwd(SERVER_BACTERIA_LOCATION)
    print(f'changed dir to {SERVER_BACTERIA_LOCATION}')

    bacteria_folders = ftp.nlst(SERVER_BACTERIA_LOCATION)  # get folders within the directory
    num_errors_in_try = 0
    num_already_downloaded = 0
    # print(bacteria_folders)

    for i, bacteria in enumerate(bacteria_folders):
        # print(bacteria)
        local_folder = os.path.join(os.path.normpath(SAVE_FOLDER), os.path.basename(os.path.normpath(bacteria)))
        # print(local_folder)

        os.makedirs(local_folder, exist_ok=True) #I think makedir is enough (doens't need to be makedirs)


        file = None
        try:
            all_assembly_folder = bacteria + "/" + ALL_ASSEMBLY_PREFIX
            # each folder may contain many assemblies of same bacteria
            assemblies = ftp.nlst(all_assembly_folder)
            if len([name for name in os.listdir(local_folder) if os.path.isfile(os.path.join(local_folder, name)) and (name.endswith("_genomic.fna.gz") or name.endswith("_assembly_stats.txt"))])/2 < len(assemblies):
                for j in range(len(assemblies)):
                    files = ftp.nlst(assemblies[j])
                    try: #Maybe: to save time - I can check if the file exists before downloading
                        file2download = f'{assemblies[j]}/{os.path.split(assemblies[j])[-1]}_genomic.fna.gz'
                        local_filename = os.path.join(local_folder, os.path.basename(os.path.normpath(file2download)))
                        file = open(local_filename, 'wb')
                        ftp.retrbinary('RETR ' + file2download, file.write)
                        print(f'finished downloading file {local_filename}')
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
                        print(f'finished downloading file {local_filename}')
                        num_errors_in_try = 0
                    except:
                        print(f'error downloading stats file for {assemblies[j]} of bacteria {bacteria}')
                    if file != None:
                        file.close()
        except:
            num_errors_in_try += 1
            print(f'error downloading bacteria {bacteria}')
            if num_errors_in_try >= MAX_NUM_ERRORS_IN_TRY:
                break



    print(f'num_try {num_try}, already_downloaded {num_already_downloaded} | len {len(bacteria_folders)}')
    ftp.quit()  # This is the “polite” way to close a connection


for i in range(NUMBER_OF_TRIES):
    try:
        get_genomes(i)
    except Exception as e:
        print(e)
        print(f'finished try number: {i} out of {NUMBER_OF_TRIES}')

