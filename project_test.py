from tokenize import String
from dash import Dash
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

def country_analysis(df, Title, graph=True):
    countries={}
    country = list(df['country'].fillna('Unknown'))
    for i in country:
        i=list(i.split(','))
        if len(i)==1:
            if i in list(countries.keys()):
                print(i)
                countries[i]+=1
            else:
                countries[i[0]]=1
        else:
            for j in i:
                if j in list(countries.keys()):
                    countries[j]+=1
                else:
                    countries[j]=1
    final_countries={}

    for country, no in countries.items():
        country=country.replace(' ', '')
        if country in list(final_countries.keys()):
            final_countries[country]+=no
        else:
            final_countries[country]=no

    final_countries={k:v for k, v in sorted(final_countries.items(), key=lambda item : item[1] , reverse=True)}
    dict_to_pandaframe = {'Country': list(final_countries.keys()), Title: list(final_countries.values())}
    countries_df = pd.DataFrame(dict_to_pandaframe)

    if graph==True:
        fig = px.bar(countries_df.head(), x='Country', y = Title, template = 'plotly_dark', title = Title, color = 'Country')
    
    return fig

def rating(df:pd.DataFrame, title:str):
    df = df.fillna("Unknown")
    df_ratings = df[df.rating.isin(df['rating'].value_counts().index[0:len(df['rating'].unique())].to_list()[:5])]
    fig = px.histogram(df_ratings, x = 'rating', category_orders = {'rating': df_ratings['rating'].value_counts().index[0:len(df_ratings['rating'].unique())].to_list()}, 
              template = 'plotly_dark', title = title, color = 'rating')
    return fig



#Starting the Application
def main() -> None:
    df = pd.read_csv("D:\\ITI\\Data Visualization\\labs\\netflix_titles.csv")
    app = Dash(external_stylesheets = [dbc.themes.CYBORG])

    
    app.layout = html.Div([ 

        dbc.Row([
            dbc.Col(html.H3("Netflix Statistics"), width = {'size': 8, 'offset': 6})
        ], justify="center", align="center"), 

        # dbc.Row([
        #     dbc.Col([
        #                 html.Div(
        #                     [
        #                         html.Div(
        #                             [
        #                                 html.P("No. of Wells"),
        #                                 html.H6(
        #                                     id="well_text",
        #                                     className="info_text"
        #                                 )
        #                             ],
        #                             id="wells",
        #                             className="pretty_container")
        #                     ], className = "mini_container")
        #             ])
        # ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id = "myGraph1", figure = {}), width = {'size': 8, 'offset': 2, 'order':0}, style={'color': 'red', 'fontSize': 40, 'textAlign': 'center'}),
            ], align = "center"),
            
        

        dbc.Row([
            dbc.Col(dcc.Graph(id = "myGraph2", figure = {}), width = {'size': 4, 'offset': 0, 'order':1}),
            dbc.Col(dcc.Dropdown(options = [{'label': str(release_year), 'value': release_year} for release_year in df['release_year'].sort_values(ascending = False).unique()], 
                        value = None, 
                        id = 'demoDropdown',
                        placeholder = 'Choose a year...',
                        multi = True), width = {'size': 4, 'offset':0, 'order':2}, align = "center"),
            dbc.Col(dcc.Graph(id = "myGraph3", figure = {}), width = {'size': 4, 'offset': 0, 'order':3})
        ]),

        dbc.Row([
            dbc.Col(dcc.Graph(id = "myGraph4", figure = {}), width = {'size': 6, 'offset': 0, 'order':1}),
            dbc.Col(dcc.Graph(id = "myGraph5", figure = {}), width = {'size': 6, 'offset': 0, 'order':2})
            ]),
        ])

    @app.callback(
        Output('myGraph1', 'figure'),
        Output('myGraph2', 'figure'),
        Output('myGraph3', 'figure'),
        Output('myGraph4', 'figure'),
        Output('myGraph5', 'figure'),
        Input('demoDropdown', 'value'),
    )
    def update_output(demoDropdown):

        if demoDropdown == None:
            filtered_df = df.copy()
        elif len(demoDropdown) == 0:
            filtered_df = df.copy()
        else:
            filtered_df = df[df.release_year.isin(demoDropdown)]
            

        netflix_shows = filtered_df[filtered_df['type'] == "TV Show"] 
        netflix_movie = filtered_df[filtered_df['type'] == "Movie"] 
        fig1 = px.histogram(filtered_df, 
                            x= "type", 
                            color = "type", 
                            template = 
                            'plotly_dark',
                            )

        fig2 = rating(netflix_movie, 'Movie Ratings')
        fig3 = rating(netflix_shows, "Show ratings")
        fig4 = country_analysis(netflix_movie, "Movies Produced")
        fig5 = country_analysis(netflix_shows, "Shows Produced")
        
        return fig1, fig2, fig3, fig4, fig5

    app.run_server()

if __name__ == '__main__':
    main()