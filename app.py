# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import numpy as np
import json
from dash.dependencies import Input, Output,State

df = pd.read_csv('../skillscape/clean_job.csv')
del df['dummy']
df.sort_values('wage',inplace=True,ascending=False)

cols=['title','wage','employees','automation','cognitive','code']
# Hold off description

df=df[df['wage']>0]
# Do some filtering

#     dcc.RangeSlider(
#     min=0,
#     max=30,
#     value=[8, 10, 15, 17, 20],
#     pushable=2
# ),

######################
def generate_table(dataframe, max_rows=100):
    return dt.DataTable(
    rows=df.to_dict('records'), # initialise the rows
    #row_selectable=True,
    #filterable=True,
    sortable=True,
    selected_row_indices=[],
    id='table',
    max_rows_in_viewport=max_rows
)

    return html.Table(
        # Header
        [html.Tr([html.Th(col.capitalize()) for col in cols])] +

        [html.Tr(['{:d}'.format(dataframe.iloc[i]['wage']),dataframe.iloc[i]['wage']]) for i in range(min(len(dataframe), max_rows))]

        # [html.Tr([
        #     html.Td(dataframe.iloc[i][col]) for col in cols
        # ]) for i in range(min(len(dataframe), max_rows))]
        ,id='table'
    )

############################
app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div(children=[
    html.H1(children='Skillscape'),

    # html.Div(children='''
    #     Dash: A web application framework for Python.
    # '''),

    dcc.Graph(
        id='wage-hist',
        selectedData={},
        hoverData={},
        figure={
            'data': [
                {'x':  df['wage'], 'type': 'histogram'},
            ],
            'layout': {
                'title': 'Wage Distribution'
            }
        }
    ),


    generate_table(df)
    #dt.DataTable(id='table')
])
components = ['id', 'clickData', 'hoverData', 'clear_on_unhover', \
'selectedData', 'relayoutData', 'figure', 'style', 'className', 'animate', \
'animation_options', 'config']
########################
@app.callback(
    Output('table', 'rows'),
    [Input('wage-hist','relayoutData')])
def test(relayData):
    if relayData:
        print('*** New range')
        if relayData.get('xaxis.range[0]') and relayData.get('xaxis.range[0]'):
            print(relayData['xaxis.range[0]'])
            print(relayData['xaxis.range[1]'])

            wageMin = relayData['xaxis.range[0]']
            wageMax = relayData['xaxis.range[1]']

            dff = df[(df.wage>wageMin)&(df.wage<wageMax)]
            print('*** Passing',dff.shape)
            #return dff.to_dict('records')
            #return generate_table(dff)
            return dff.to_dict('records')
        else:
            #return generate_table(df)
            return df.to_dict('records')
    else:
        #return generate_table(df)
        return df.to_dict('records')
    #    return df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
