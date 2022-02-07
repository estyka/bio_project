from Bio import SeqIO
import os
import pandas as pd
from datetime import datetime
from IPython.display import display
import matplotlib.pyplot as plt
import re


def get_org_dict(stats_dir):
    org_dict = {}
    for stats_filename in os.listdir(stats_dir):
        cur_dict = {}
        with open(os.path.join(stats_dir, stats_filename)) as stats_file:
            for line in stats_file:
                if line.startswith("# Organism name:"):
                    cur_dict["organism_name"] = line.split(":")[-1].lstrip().strip("\n")
                #                 if line.startswith("# Organism name:"):
                #                     if line.find("oryzae") != -1:
                #                         cur_dict["org_pv"] = "oryzae"
                #                     elif line.find("oryzicola") != -1:
                #                         cur_dict["org_pv"] = "oryzicola"
                elif line.startswith("# Infraspecific name:  strain="):
                    cur_dict["strain"] = line.split("strain=")[-1].strip("\n")
                elif line.startswith("# Date:"):
                    cur_dict["date"] = line.split()[-1].strip("\n")
                elif line.startswith("# GenBank assembly accession:"):
                    cur_dict["GenBank_accesion_id"] = line.split()[-1].strip("\n")
                    break
        if not cur_dict.get("organism_name") or not cur_dict.get("strain") or not cur_dict.get(
                "date") or not cur_dict.get("GenBank_accesion_id"):
            print("ERROR: file= %s has missing info" % stats_filename)
            break

        org_full_name = get_full_name(cur_dict)

        if not org_dict.get(org_full_name):
            org_dict[org_full_name] = []
        org_dict[org_full_name].append(
            {"date": cur_dict["date"], "GenBank_accesion_id": cur_dict["GenBank_accesion_id"]})

    return org_dict


def get_full_name(cur_dict):
    strain = cur_dict["strain"]
    org_name = re.sub(r"\([^()]*\)", "", cur_dict["organism_name"]).strip()  # remove whatever is in parenthesis
    if strain in org_name:
        org_full_name = org_name
    else:
        org_full_name = org_name + " " + strain
    return org_full_name


def get_latest_data_df(organism_dic):
    df_dict = {"organism name": [], "last assembly date": [], "number of assemblies": [],
               "last GenBank acession ID": []}
    for org, items in organism_dic.items():
        first_item = items[0]  # default value
        last_date = datetime.strptime(first_item["date"], "%Y-%m-%d")
        last_accession_id = first_item["GenBank_accesion_id"]
        if len(items) > 1:  # more than one assembly of the genome
            for item in items:
                date = datetime.strptime(item["date"], "%Y-%m-%d")
                if date > last_date:
                    last_date = date
                    last_accession_id = item["GenBank_accesion_id"]
        df_dict["organism name"].append(org)
        df_dict["last assembly date"].append(last_date)
        df_dict["number of assemblies"].append(len(items))
        df_dict["last GenBank acession ID"].append(last_accession_id)
    return pd.DataFrame(df_dict)


stats_dir = "C:\\Users\\97252\\Documents\\year_4\\project\\Xanthomonas Oryzae\\ncbi-genomes-stats-2022-02-02\\stats"

organism_dic = get_org_dict(stats_dir)
df = get_latest_data_df(organism_dic)
df.sort_values(by=["number of assemblies"], inplace=True, ascending=False)
display(df)

stats_dir = "C:\\Users\\97252\\Documents\\year_4\\project\\Xanthomonas\\ncbi-genomes-stats-refseq-2022-02-07"

organism_dic = get_org_dict(stats_dir)
df = get_latest_data_df(organism_dic)
df.sort_values(by=["number of assemblies"], inplace=True, ascending=False)
display(df)