import altair as alt
import pandas as pd
import itertools

character_all_data = './data/character_all_data.csv'
character_all_data = pd.read_csv(character_all_data)


# all data type
all_metadata = './data/character_female_means_trait_metadata.csv'
all_metadata = pd.read_csv(all_metadata)
metadata_description = all_metadata.set_index('character')['character_description'].to_dict()


def generate_interactive_selection_graph(x_variable, y_variable, data):
    selection = alt.selection_multi(fields=['species'])

    color = alt.condition(selection,
                          alt.Color('species:N', legend=None, ),
                          alt.value('lightgray'), scale=alt.Scale(scheme='dark2'), opacity=alt.value(0.1),
                          )

    scatter = alt.Chart(data).mark_point().encode(
        x=alt.X(x_variable, axis=alt.Axis(title=str(metadata_description[x_variable]))),
        y=alt.X(y_variable, axis=alt.Axis(title=str(metadata_description[y_variable]))),
        color=color,
        tooltip=data.columns.tolist()
    )

    legend = alt.Chart(data).mark_point().encode(
        y=alt.Y('species:N', axis=alt.Axis(orient='right')),
        color=color
    ).add_selection(
        selection
    )

    return scatter | legend


def get_concat_graphs(selected_attributes, data):
    permutations = itertools.combinations(selected_attributes, 2)
    graphs = []
    for p in permutations:
        single_graph = generate_interactive_selection_graph(p[0], p[1], data)
        graphs.append(single_graph)

    return graphs


# make a single row
def make_hcc(row_of_charts):
    hconcat = [chart for chart in row_of_charts]
    hcc = alt.HConcatChart(hconcat=hconcat)
    return hcc

# take an array of charts and produce a facet grid
def facet_wrap(charts, charts_per_row):
    rows_of_charts = [
        charts[i:i+charts_per_row]
        for i in range(0, len(charts), charts_per_row)]
    vconcat = [make_hcc(r) for r in rows_of_charts]
    vcc = alt.VConcatChart(vconcat=vconcat)\
      .configure_axisX(grid=True)\
      .configure_axisY(grid=True)
    return vcc


import webbrowser
import os

# integrate graphs
# multi_correlation_attributes = [x for x in character_all_data.columns if 'morph' in x and 'sex' not in x]
# list = ['morph_hind_leg_length','tail_length','trunk_length','trunk_width']
#
# graphs = get_concat_graphs(selected_attributes= list, data= character_all_data)
# compound_chart = facet_wrap(graphs, charts_per_row=2)
# compound_chart.properties(title='Facet correlation plots:').save('chart.html')
# webbrowser.open('file://' + os.path.realpath('chart.html'))


