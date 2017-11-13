import json
from pandas.io.json import json_normalize

data = json.load((open('world_bank_projects.json')))
# ns_tables_name = ['majorsector_percent', 'mjsector_namecode', 'mjtheme_namecode', 'projectdocs', 'sector', 'sector_namecode', 'theme_namecode']
ns_tables_name = ['majorsector_percent', 'mjsector_namecode', 'mjtheme_namecode', 'sector', 'sector_namecode']

# create df with all columns and drop the nested columns
wb = json_normalize(data)
wb = wb.drop(ns_tables_name, axis=1)

# create separate df's with the nested tables and include id columns from main table
ns_tables = {}
for i in ns_tables_name:
    ns_tables[i] = json_normalize(data, i, ['id'], errors='ignore')

##############################################################################
#############      Find the 10 countries with most projects      #############
##############################################################################

top10_cnty_pr = wb.groupby('countrycode')['id'].count().sort_values(ascending=False)
print('Top 10 countries with the most projects: ', top10_cnty_pr[0:10])

##############################################################################
### Find the top 10 major project themes (using column 'mjtheme_namecode') ###
##############################################################################

top10_mj_pr_theme = ns_tables['mjtheme_namecode'].groupby('code')['id'].count().sort_values(ascending=False)
print('Top 10 major project themes used: ', top10_mj_pr_theme[0:10])

##############################################################################################
# In 2. above you will notice that some entries have only the code and the name is missing. ##
# Create a dataframe with the missing names filled in.                                      ##
##############################################################################################

# Create a new dataframe where the data will be manipulated
tb = ns_tables['mjtheme_namecode']

# function that returns True is the value provided is in the dictionary
def check_indict_v(val, dicn):
    for k in dicn.values():
        for m in k:
            if m == val:
                return True
    return False


dict_code = {}
code_list = []
for i in tb.index:
    tmp_c = tb.code[i]
    tmp_n = tb.name[i]
    if tb.code[i] not in code_list:
        if tb.name[i] != '':
            dict_code[tb.code[i]] = [tb.name[i]]
            code_list.append(tb.code[i])
    else:
        if not check_indict_v(tb.name[i], dict_code):
            dict_code[tb.code[i]].append(tb.name[i])

# check the variation of values per key
dict_var = [len(i) for i in dict_code.values()]

# confirm that we have a one to one ratio of keys and values
print(len(dict_var) == len(code_list))

# update missing names for tb data frame
tb.name = [dict_code[i][0] for i in tb.code]
