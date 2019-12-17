import altair as alt


# function to draw scatterplot and histograms (find the correlation between dependent and independent variables)

def get_histogram_with_scatterplot(data, x_variable, y_variable):
    base = alt.Chart(data)
    area_args = {'opacity': .3, 'interpolate': 'step'}
    points = base.mark_circle().encode(
        alt.X(x_variable),
        alt.Y(y_variable),
        color='species', size=y_variable)

    # top histogram
    top_hist = base.mark_area(**area_args).encode(
        alt.X(x_variable + ':Q',
              bin=alt.Bin(maxbins=20),
              stack=None,
              title=''
              ),
        alt.Y('count()', stack=None, title=''),
        alt.Color('species:N'),
    ).properties(height=200)

    # right histogram
    right_hist = base.mark_area(**area_args).encode(
        alt.Y(y_variable + ':Q',
              bin=alt.Bin(maxbins=20),
              stack=None,
              title='',
              ),
        alt.X('count()', stack=None, title=''),
        alt.Color('species:N'),
    ).properties(width=200)

    graph = top_hist & (points | right_hist)
    return graph


#################################
#         Individual Test       #
#################################

# function call
# x_variable = 'morph_SVL'
# y_variable = 'morph_head_width'
# get_histogram_with_scatterplot(character_all_data, x_variable, y_variable)


