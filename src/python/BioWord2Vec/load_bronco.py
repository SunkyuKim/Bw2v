
import pandas as pd

def bronco_full():
    df = pd.read_csv("../res/BRONCO_20151221/BRONCO_MAPPED_final_20150914.txt", delimiter='\t')

    # print df.columns
    # temp_df = df[['Gene', 'Mutation', 'Disease', 'Drug', 'Cell line']]
    temp_df = df[['Gene', 'Mutation', 'Disease', 'Drug']]
    full_list = []

    gene_set = set()
    drug_set = set()
    mut_set = set()
    disease_set = set()

    for tup in temp_df.itertuples():
        if '-' not in tup:
            disease = tup[3].replace(" ", "_").lower().split("|")[0].replace("(","").replace(")","")
            gene = tup[1]
            mut = tup[2].replace("|", "")
            drug = str(tup[4]).split("|")[0].replace("(","").replace(")","")

            # print gene, mut, disease, drug

            gene_set.add(gene)
            mut_set.add(mut)
            disease_set.add(disease)
            drug_set.add(drug)

            # full_list.append(tup[3].replace(" ", "_").lower())
            # color_list.append('blue')
            # full_list.append(tup[1])
            # color_list.append('green')
            # full_list.append(tup[2].replace("|", ""))
            # color_list.append('red')

    full_list = list(gene_set) + list(disease_set) + list(mut_set) + list(drug_set)
    color_list = ['red']*len(gene_set) + ['blue']*len(disease_set) + \
                 ['green']*len(mut_set) + ['yellow']*len(drug_set)

    return full_list, color_list

def bronco_abstract():

    pass

if __name__ == '__main__':
    bronco_full()