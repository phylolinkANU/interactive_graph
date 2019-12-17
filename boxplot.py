import altair as alt
import pandas as pd


# all data type
all_metadata = './data/character_female_means_trait_metadata.csv'
all_metadata = pd.read_csv(all_metadata)
metadata_description = all_metadata.set_index('character')['character_description'].to_dict()



def generate_boxplot(attribute, data):
    '''Boxplot'''
    boxplot = alt.Chart(data).mark_boxplot().encode(
        x='species:O',
        y=attribute + ':Q'
    ).properties(title='Boxplot: {}'.format(str(metadata_description[attribute])),
            height =700,
            width = 700
                 )

    return boxplot


#################################
#         Individual Test       #
#################################

# attribute = 'morph_SVL'
# generate_boxplot(attribute, character_all_data)




