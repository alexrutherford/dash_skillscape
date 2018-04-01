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

df['cognitive']=df['cognitive'].round(2)

dff=df.copy()

#     dcc.RangeSlider(
#     min=0,
#     max=30,
#     value=[8, 10, 15, 17, 20],
#     pushable=2
# ),

######################
def generate_table(dataframe, max_rows=9999999):
    print('Generating')

    return dt.DataTable(
    rows=df.to_dict('records'), # initialise the rows
    row_selectable=True,
    #filterable=True,
    sortable=True,
    #selected_row_indices=[],
    id='table',
    max_rows_in_viewport=max_rows,
    column_widths=10

)

#['id', 'editable', 'filterable', 'sortable', 'resizable', 'column_widths', 'columns', 'row_selectable', 'selected_row_indices',
# 'enable_drag_and_drop', 'header_row_height', 'min_height', 'min_width', 'max_rows_in_viewport', 'row_height', 'row_scroll_timeout',
# 'tab_index', 'filters', 'rows', 'row_update', 'sortColumn', 'sortDirection']

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
    html.Div([
    dcc.Graph(
        id='wage-hist',
        selectedData={},
        hoverData={},
        className="six columns",
        #gap=0.5,
        figure={
            'data': [
                {'x':  df['wage'], 'type': 'histogram'},
            ]
            #,
            #'layout': {
            #    'title': 'Wage Distribution'
            #}
        }
    ),
    dcc.Graph(
        id='employee-hist',
        selectedData={},
        hoverData={},
        className="six columns",
        figure={
            'data': [
                {'x':  df['employees'], 'type': 'histogram'},
            ],
            'layout': {
                'title': 'Employee Distribution'
            }
        }
    ),
    ],className='row'),
    html.Div([
    dcc.Graph(
        id='cognitive-hist',
        selectedData={},
        hoverData={},
        className="six columns",
        #gap=0.5,
        figure={
            'data': [
                {'x':  df['cognitive'], 'type': 'histogram'},
            ]
            #,
            #'layout': {
            #    'title': 'Wage Distribution'
            #}
        }
    ),
    dcc.Graph(
        id='auto-hist',
        selectedData={},
        hoverData={},
        className="six columns",
        figure={
            'data': [
                {'x':  df['automation'], 'type': 'histogram'},
            ],
            'layout': {
                'title': 'Automation Distribution'
            }
        }
    ),
    ],className='row'),

    generate_table(df)
    #dt.DataTable(id='table')
])
components = ['id', 'clickData', 'hoverData', 'clear_on_unhover', \
'selectedData', 'relayoutData', 'figure', 'style', 'className', 'animate', \
'animation_options', 'config']
########################
def makeLines(x,y):
    return {'type' : 'line', 'x0':x,'x1':x,'y0':0,'y1':100,
    'line':{'dash':'dot','width':2,'color':'rgb(128,128,128)'}}

########################
@app.callback(
    Output('wage-hist', 'figure'),
    [Input('table', 'rows'),
     Input('table', 'selected_row_indices')],
     [State('wage-hist', 'figure')])
def update_figure(rows, selected,state):
    print('Selection?')
    if selected:
        if len(selected)>0:
            dff = pd.DataFrame(rows)
            print('Updating')
            print(dff.iloc[selected])
            selectedWage=dff.iloc[selected]['wage'].values[0]
            #print(selectedWage.values[0])

            figure={
                'data': [
                    {'x':  df['wage'], 'type': 'histogram'},
                ],
                'layout' : {
                    'title': 'Wage Distribution',
                    'shapes' : []
                }
            }
            figure['layout']['shapes']=[makeLines(x,100) for x in dff.iloc[selected]['wage'].values]

            return figure
        else:
            figure={
                'data': [
                    {'x':  df['wage'], 'type': 'histogram'},
                ],
                'layout' : {
                    'title': 'Wage Distribution'
                }
            }
            return figure
    else:
        figure={
            'data': [
                {'x':  df['wage'], 'type': 'histogram'},
            ],
            'layout' : {
                'title': 'Wage Distribution'
            }
        }
        return figure
########################
@app.callback(
    Output('table', 'rows'),
    [Input('wage-hist','relayoutData')])
def test(relayData):
    print('Relay?')

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
