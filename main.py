import argparse
from scatterplot import *
from scatterplot_correlation import *
from ridgeline  import *
from boxplot import *


parser = argparse.ArgumentParser()


# 0. add data in the front
parser.add_argument("data", help="input data")

# 1. histogram
parser.add_argument("-his", "--histogram", help="generate interactive histograms based on input data",action="store_true")

parser.add_argument("-x", "--x",  help="x variable of the input data")

parser.add_argument("-y", "--y", help="y variable of the input data")


# 2. Correlation scatter plots

parser.add_argument("-correlations", "--correlation_plots", help="correlation plot in pairs (interactive with selection enabled)",
                    action="store_true")

parser.add_argument("-attributes", "--attributes",  nargs='*',help="selected attributes to plot")


# 3. ridgeline plot

parser.add_argument("-ridge", "--ridgeline", help="ridgeline plot based on selected attribute",
                    action="store_true")


# 4. box plot
parser.add_argument("-box", "--boxplot", help="interactive box plot",
                    action="store_true")



args = parser.parse_args()



## data selection area

# all data type
all_metadata = './data/character_female_means_trait_metadata.csv'
all_metadata = pd.read_csv(all_metadata)
metadata_description = all_metadata.set_index('character')['character_description'].to_dict()


character_all_data = './data/character_all_data.csv'
character_all_data = pd.read_csv(character_all_data)



############################
#       main program       #
############################

data_path = args.data
import webbrowser, os


# execution query
# python3 main.py  ./data/character_all_data.csv -his -x morph_SVL -y morph_head_width
if args.histogram:
    if args.x and args.y:
        data = pd.read_csv(data_path)
        get_histogram_with_scatterplot(data, args.x, args.y).save('chart.html')
        webbrowser.open('file://' + os.path.realpath('chart.html'))


# execution query
# python3 main.py  ./data/character_all_data.csv -correlations -attributes morph_SVL, trunk_length, trunk_width
if args.correlation_plots:
    if args.attributes:
        data = pd.read_csv(data_path)
        list = [item[0:-1] if item[-1]==',' else item[::] for item in args.attributes]
        # assemble the facet grid
        graphs = get_concat_graphs(selected_attributes=list, data=character_all_data)
        compound_chart = facet_wrap(graphs, charts_per_row=2)
        compound_chart.properties(title='Facet correlation plots:').save('chart.html')
        webbrowser.open('file://' + os.path.realpath('chart.html'))


# execution query
# python3 main.py  ./data/character_all_data.csv -ridge -x morph_SVL
if args.ridgeline:
    if args.x:
        print(args.x)
        data = pd.read_csv(data_path)
        generate_ridgeline_plot(data, args.x).save('chart.html')
        webbrowser.open('file://' + os.path.realpath('chart.html'))


# execution query
# python3 main.py  ./data/character_all_data.csv -box -x morph_SVL
if args.boxplot:
    if args.x:
        data = pd.read_csv(data_path)
        generate_boxplot(args.x, data).save('chart.html')
        webbrowser.open('file://' + os.path.realpath('chart.html'))


