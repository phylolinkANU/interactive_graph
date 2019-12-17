import altair as alt
import pandas as pd



# all data type
all_metadata = './data/character_female_means_trait_metadata.csv'
all_metadata = pd.read_csv(all_metadata)
metadata_description = all_metadata.set_index('character')['character_description'].to_dict()



def generate_ridgeline_plot(data, attribute):
    '''ridge line plot: multiple histograms overlaps'''

    step = 40
    overlap = 1

    graph = alt.Chart(data).transform_joinaggregate(
        mean_attribute="mean({})".format(str(attribute)), groupby=['species']
    ).transform_bin(
        ['bin_max', 'bin_min'], str(attribute)
    ).transform_aggregate(
        value='count()', groupby=['species', 'mean_attribute', 'bin_min', 'bin_max']
    ).transform_impute(
        impute='value', groupby=['species', 'mean_attribute'], key='bin_min', value=0
    ).mark_area(
        interpolate='monotone',
        fillOpacity=0.4,
        stroke='lightgray',
        strokeWidth=0.3
    ).encode(
        alt.X('bin_min:Q', bin='binned', title=str(attribute)),
        alt.Y(
            'value:Q',
            scale=alt.Scale(range=[step, -step * overlap]),
            axis=None
        ),
        alt.Fill(
            'mean_attribute:Q',
            legend=None,
            scale=alt.Scale(domain=[30, 5], scheme='redyellowblue')
        ),
        alt.Row(
            'species:O',
            title='Species',
            header=alt.Header(labelAngle=0, labelAlign='right')
        )
    ).properties(
        bounds='flush', title='Comparison: {}'.format(str(metadata_description[attribute])), height=100,
        width=700,
    ).configure_facet(
        spacing=0,
    ).configure_view(
        stroke=None,
    ).configure_title(
        anchor='end'
    )

    return graph



#################################
#         Individual Test       #
#################################

# attribute = 'morph_hind_leg_length'
# attribute = 'morph_SVL'
# generate_ridgeline_plot(character_all_data, attribute)



