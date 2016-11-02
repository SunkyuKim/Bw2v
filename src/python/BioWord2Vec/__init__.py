

# import pandas as pd
#
# df = pd.read_csv("../res/training_data_rel_added_revised.csv")
# with open("../res/training_data_rel_added_revised_tagged_sentences.csv", 'w') as fw:
#     for l in list(df['tagged_sentence']):
#         sentence = l
#         sentence = sentence.strip().replace("> ", ">").replace(">", "> ").replace(" <", "<").replace("<", " <")
#         fw.write(sentence + '\n')
def a():
    ls = (x for x in range(100000000))
    for l in ls:
        yield l

for k in a():
    print k