import dash
import dash_core_components as dcc 
import dash_html_components as html 
import pandas as pd 
import seaborn as sns 
import plotly.graph_objs as go 

app = dash.Dash() # make python obj with Dash() method

app.title = 'Purwadhika Dash Plotly' # set web title
dfTips = sns.load_dataset('tips')
color_set = ['#ff3fd8','#4290ff']

# function to generate HTML Table
def generate_table(dataframe, max_rows=10) :
    return html.Table(
         # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(str(dataframe.iloc[i][col])) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

# the layout/content
app.layout = html.Div(children=[
    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='Tips Data Set', children=[
            html.Div([
                html.H1('Tips Data Set', className='h1FirstTab'),
                generate_table(dfTips)
            ])
        ]),
        dcc.Tab(label='Scatter Plot', children=[
            html.Div([
                html.H1('Scatter Plot Tips Data Set', className='h1FirstTab'),
                dcc.Graph(
                    id='scatterPlot',
                    figure={
                        'data': [
                            go.Scatter(
                                x=dfTips[dfTips['sex'] == col]['total_bill'], 
                                y=dfTips[dfTips['sex'] == col]['tip'], 
                                mode='markers', 
                                marker=dict(color=color_set[i], size=10, line={'width': 0.5, 'color': 'white'}), 
                                name=col
                            ) for col,i in zip(dfTips['sex'].unique(),range(2))
                        ],
                        'layout': go.Layout(
                            xaxis={'title': 'Total Bill'},
                            yaxis={'title': 'Tip'},
                            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                            hovermode='closest'
                        )
                    }
                )
            ])
        ]),
        dcc.Tab(label='Bar Plot', children=[
            html.Div([
                html.H1('Bar Plot Tips Data Set', className='h1FirstTab'),
                html.Div([
                    html.P('X Axis : '),
                    dcc.Dropdown(
                        id='ddl-x-bar-plot',
                        options=[{'label': 'Sex', 'value': 'sex'},
                                {'label': 'Smoker', 'value': 'smoker'},
                                {'label': 'Day', 'value': 'day'},
                                {'label': 'Time', 'value': 'time'}],
                        value='sex'
                    )
                ], style={'width':'30%'}),
                html.Div([
                    html.P('Stats : '),
                    dcc.Dropdown(
                        id='ddl-stats-bar-plot',
                        options=[{'label': 'Average', 'value': 'mean'},
                                {'label': 'Standard Deviation', 'value': 'std'},
                                {'label': 'Minimum', 'value': 'min'},
                                {'label': '25th percentile', 'value': '25%'},
                                {'label': 'Median', 'value': '50%'},
                                {'label': '75th percentile', 'value': '75%'},
                                {'label': 'Maximum', 'value': 'max'}],
                        value='mean'
                    )
                ], style={'width':'30%', 'paddingBottom': '40px'}),
                dcc.Graph(
                    id='barPlot',
                    figure={
                        'data': [
                            go.Bar(
                                x=dfTips.groupby('sex')['tip'].mean().index,
                                y=dfTips.groupby('sex')['tip'].mean(),
                                opacity=0.7,
                                name='Tips'
                            ),
                            go.Bar(
                                x=dfTips.groupby('sex')['total_bill'].mean().index,
                                y=dfTips.groupby('sex')['total_bill'].mean(),
                                opacity=0.7,
                                name='Total Bill'
                            )
                        ],
                        'layout': go.Layout(
                            xaxis={'title': 'Sex'}, yaxis={'title': 'US$'},
                            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                            legend={'x': 0, 'y': 1}, hovermode='closest',
                            # plot_bgcolor= 'black', paper_bgcolor= 'black',
                        )
                    }
                )
            ])
        ])
    ],style={
        'fontFamily': 'system-ui'
    }, content_style={
        'fontFamily': 'Arial',
        'borderBottom': '1px solid #d6d6d6',
        'borderLeft': '1px solid #d6d6d6',
        'borderRight': '1px solid #d6d6d6',
        'padding': '44px'
    })
], style={
    'maxWidth': '1000px',
    'margin': '0 auto'
})

@app.callback(
    dash.dependencies.Output('barPlot', 'figure'),
    [dash.dependencies.Input('ddl-x-bar-plot', 'value'),
    dash.dependencies.Input('ddl-stats-bar-plot', 'value')])
def update_bar_graph(ddlXBarPlot, stats):
    return {
            'data': [
                go.Bar(
                    x=dfTips.groupby(ddlXBarPlot)['tip'].describe()[stats].index,
                    y=dfTips.groupby(ddlXBarPlot)['tip'].describe()[stats],
                    opacity=0.7,
                    name='Tip'
                ),
                go.Bar(
                    x=dfTips.groupby(ddlXBarPlot)['total_bill'].describe()[stats].index,
                    y=dfTips.groupby(ddlXBarPlot)['total_bill'].describe()[stats],
                    opacity=0.7,
                    name='Total Bill'
                )
            ],
            'layout': go.Layout(
                xaxis={'title': ddlXBarPlot.capitalize()},
                yaxis={'title': 'US$'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
    }

if __name__ == '__main__' :
    # run server on port 1997
    # debug=True for auto restart if code edited
    app.run_server(debug=True,port=1997)