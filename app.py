import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth#pip install dash-auth
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(
    app,
    {'resolve':'resolve2020'}
)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
users = pd.read_csv('../Users.csv')
events = pd.read_csv('../Events.csv')

users['Event_Name'] = users['Event_Name'].replace('install','Instalacion').replace('FIRST_ORDER_PLACED_CONFIRMED_BACK','Primera_orden')
users_dummie = pd.get_dummies(users,columns=['Event_Name'], drop_first = True)


users2 = users[['Hour','Event_Name','clientID']].groupby(['Hour','Event_Name']).count()
users2.reset_index(inplace=True)
users2.sort_values(['Event_Name'],inplace=True)

users['fecha'] = [x[:10] for x in users.Date]
users3 = users[['fecha','Event_Name','clientID']].groupby(['fecha','Event_Name']).count()
users3.reset_index(inplace=True)
users3.sort_values(['Event_Name'],inplace=True)

events['start_hour'] = [x[11:13] for x in events.start_date]
events2 = events.groupby(['start_hour','event_name']).count()
events2.reset_index(inplace=True)
events2.sort_values(['event_name'],inplace=True)

events['date'] = [x[:10] for x in events.start_date]
events3 = events.groupby(['date','event_name']).count()
events3.reset_index(inplace=True)
events3.sort_values(['event_name'],inplace=True)

merge = pd.merge(users_dummie,events,how='inner', left_on ='Date', right_on='start_date')
merge['only_date'] = [x[:10] for x in merge.start_date]
merge2 = merge[['only_date','event_name','Event_Name_Primera_orden','clientID']].groupby(['only_date','event_name','Event_Name_Primera_orden']).count()
merge2.reset_index(inplace=True)
merge2.sort_values(['event_name'],inplace=True)

merge21 = merge2[merge2['Event_Name_Primera_orden']==1]
merge22 = merge2[merge2['Event_Name_Primera_orden']==0]

merge3 = merge[['Hour','event_name','Event_Name_Primera_orden','clientID']].groupby(['Hour','event_name','Event_Name_Primera_orden']).count()
merge3.reset_index(inplace=True)
merge3.sort_values(['event_name'],inplace=True)

merge31 = merge3[merge3['Event_Name_Primera_orden']==1]
merge32 = merge3[merge3['Event_Name_Primera_orden']==0]

# ------------------------------------------------------------------------------
# Definir gráficos

def users_explore(evento, hover, color, color_line, title_var):
    fig = go.Figure([go.Bar(x= hover, y=evento.values.tolist(), text=evento.values.tolist())])
    fig.update_traces(marker_color=color, marker_line_color=color_line,
                    marker_line_width=1.5, opacity=0.6)
    fig.update_layout(title_text='Número de usuarios en categoría '+(str(title_var)))
    return fig

def cross_bars(df_users, var, head = 5):
    df_users = df_users.reset_index()
    df = df_users[['Event_Name',var,'Country_Code']].groupby(['Event_Name',var]).count().reset_index()
    i = df[df['Event_Name']=='Instalacion'].sort_values('Country_Code', ascending=False).head(head)
    p = df[df['Event_Name']=='Primera_orden'].sort_values('Country_Code', ascending=False).head(head)
    fig = go.Figure(data=[
        go.Bar(name='Instalación', x=i[var], y=i['Country_Code'],marker_color='lightsalmon'),
        go.Bar(name='Primera Orden', x=p[var], y=p['Country_Code'],marker_color='indianred')
    ])

    fig.update_layout(title_text='Número de usuarios por evento en categoría '+str(var),barmode='stack')
    return fig

def bubble_plot(df,var_x,var_y,var_z ,color, title,title_x, title_y, size_b):

    fig = go.Figure()
    sizeref = 2.*max(df[var_z])/(size_b**2)
    fig.add_trace(go.Scatter(
        x=df[var_x],
        y=df[var_y],
        marker_size= df[var_z],
        text=df[var_z],
        marker=dict(
            color=color,
            line_color = color,
        )
    ))
    fig.update_traces(mode='markers',marker=dict(sizemode='area',sizeref=sizeref, line_width=2))

    fig.update_layout(
        title=title,
        xaxis=dict(
            title=title_x,
            showgrid=False,
            showline=True,
            linecolor='rgb(102, 102, 102)',
            tickfont_color='rgb(102, 102, 102)',
            showticklabels=True,
            ticks='outside',
            tickcolor='rgb(102, 102, 102)',
        ),
        yaxis=dict(
            title=title_y,
            showline=True,
            linecolor='rgb(102, 102, 102)',
            tickfont_color='rgb(102, 102, 102)',
            showticklabels=True,
            #dtick=1,
            ticks='outside',
            tickcolor='rgb(102, 102, 102)',
            gridcolor='white',
            gridwidth=1,
        ),
        paper_bgcolor='white',
        #plot_bgcolor='rgb(243, 243, 243)',
    )

    return fig

def bubble_merge(merge1,merge2,var,color1, color2,title,title_y):
    fig = go.Figure()
    sizeref = 2.*max(merge1['clientID'])/(20**2)
    fig.add_trace(go.Scatter(
        x=merge1['event_name'],
        y=merge1[var],
        marker_size= merge1['clientID'],
        text = merge1['clientID'],
        name ='Instalación',
        marker=dict(
            color=color1,
            line_color = color1,
        )
    ))

    fig.add_trace(go.Scatter(
        x=merge2['event_name'],
        y=merge2[var],
        marker_size= merge2['clientID'],
        opacity=0.8,
        text = merge2['clientID'],
        name ='Primer evento ',
        marker=dict(
            color=color2,
            line_color = color2,
        )
    ))

    fig.update_traces(mode='markers',marker=dict(sizemode='area',sizeref=sizeref, line_width=2))
    fig.update_layout(
        title=title,
        showlegend=True,
        xaxis=dict(
            title='Evento B',
            showgrid=False,
            showline=True,
            linecolor='rgb(102, 102, 102)',
            tickfont_color='rgb(102, 102, 102)',
            showticklabels=True,
            ticks='outside',
            tickcolor='rgb(102, 102, 102)',
        ),
        yaxis=dict(
            title=title_y,
            showline=True,
            linecolor='rgb(102, 102, 102)',
            tickfont_color='rgb(102, 102, 102)',
            showticklabels=True,
            #dtick=1,
            ticks='outside',
            tickcolor='rgb(102, 102, 102)',
            gridcolor='white',
            gridwidth=1,
        ),
        paper_bgcolor='white',
        #plot_bgcolor='rgb(243, 243, 243)',
    )
    return fig
# Create global chart template
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNrOWJqb2F4djBnMjEzbG50amg0dnJieG4ifQ.Zme1-Uzoi75IaFbieBDl3A"

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
)
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("dash-logo.png"),
                            id="plotly-image",
                            style={
                                "height": "60px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "StudioSAS",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Prueba científico de datos", style={"margin-top": "0px"}
                                ),
                                html.H6(
                                    "Angie Navarrete", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Número de usuarios por variable:",
                            className="control_label",
                        ),
                        dcc.Dropdown(id="slct_var11",
                             options=[
                                 {"label": "Evento", "value": 'Event_Name'},
                                 {"label": "Hora", "value": 'Hour'},
                                 {"label": "WiFi", "value": 'WIFI'},
                                 {"label": "Dispositivo", "value": 'Device_Category'},
                                 {"label": "Medio (top 10)", "value": 'sourceMedium'},
                                 {"label": "Canal (top 10)", "value": 'Channel'},
                                 {"label": "Carrier (top 10)", "value": 'Carrier'},
                                 {"label": "Operador (top 10)", "value": 'Operator'}],
                             multi = False,
                             value='Event_Name',
                             className="dcc_control"
                        ),

                        html.Div(
                            [dcc.Graph(id='barplot_var', figure={})],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="six columns",
                ),

                                html.Div(
                                    [
                                        html.P(
                                            "Número de usuarios por variable y orden:",
                                            className="control_label",
                                        ),
                                        dcc.Dropdown(id="slct_var12",
                                             options=[{"label": "Hora", "value": 'Hour'},
                                                 {"label": "WiFi", "value": 'WIFI'},
                                                 {"label": "Dispositivo", "value": 'Device_Category'},
                                                 {"label": "Medio (top 5)", "value": 'sourceMedium'},
                                                 {"label": "Canal (top 5)", "value": 'Channel'},
                                                 {"label": "Carrier (top 5)", "value": 'Carrier'},
                                                 {"label": "Operador (top 5)", "value": 'Operator'}],
                                             multi = False,
                                             value='Hour',
                                             className="dcc_control"
                                        ),

                                        html.Div(
                                            [dcc.Graph(id='barplot_cross', figure={})],
                                            id="countGraphContainer3",
                                            className="pretty_container",
                                        ),
                                    ],
                                    id="right-column3",
                                    className="six columns",
                                ),
            ],
            className="row flex-display",

        ),
        #aqui

        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "NOTA: Hay dos clases de eventos que se denotarán como:",
                            className="control_label",
                        ),
                        html.P(
                            "EVENTO_A: Instalacion o Primera orden ",
                            className="control_label",
                        ),
                        html.P(
                            "EVENTO_B:  A, AA, B, ..., o Z",
                            className="control_label",
                        ),
                        html.P("Filtro cruce de ambos eventos:", className="control_label"),
                        dcc.Dropdown(id="slct_var2",
                                     options=[
                                         {"label": "Fecha", "value": 'fecha'},
                                         {"label": "Hora", "value": 'Hour'}],
                                     multi=False,
                                     value='Fecha',
                                     className="dcc_control"
                                     ),
                        html.P("Filtro EVENTO_A por fecha y hora:", className="control_label"),
                        dcc.Dropdown(id="slct_var21",
                                     options=[
                                         {"label": "Fecha", "value": 'fecha'},
                                         {"label": "Hora", "value": 'Hour'}],
                                     multi=False,
                                     value='Fecha',
                                     className="dcc_control"
                                     ),
                        html.P("Filtro EVENTO_B por fecha y hora:", className="control_label"),
                        dcc.Dropdown(id="slct_var22",
                                     options=[
                                         {"label": "Fecha", "value": 'fecha'},
                                         {"label": "Hora", "value": 'Hour'}],
                                     multi=False,
                                     value='Fecha',
                                     className="dcc_control"
                                     ),

                    ],
                    className="pretty_container three columns",
                    id="cross-filter-options1",
                ),
                html.Div(
                    [
                        html.Div(
                            [dcc.Graph(id='bubble_merge_var', figure={})],
                            id="countGraphContainer1",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column2",
                    className="nine columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id='bubble_user', figure={})],
                    className="pretty_container twelve columns", #six
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id='bubble_event', figure={})],
                    className="pretty_container twelve columns",
                ),
                #html.Div(
                #    [dcc.Graph(id="aggregate_graph")],
                #    className="pretty_container five columns",
                #),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='barplot_var', component_property='figure'),
    [Input(component_id='slct_var11', component_property='value')])

def update_graph(option_slctd):
    #container = "The year chosen by user was: {}".format(option_slctd)
    if option_slctd == 'Event_Name':
        fig = users_explore(pd.value_counts(users[option_slctd]), ['Intsalación','Primera orden'], 'orange', 'darkorange','Evento')
    elif option_slctd == 'Hour':
        fig = users_explore(pd.value_counts(users[option_slctd]).sort_index(), [str(s) + 'h' for s in list(range(25))], 'blue', 'darkblue','Hora')
    elif option_slctd == 'WIFI':
        fig = users_explore(pd.value_counts(users[option_slctd]), ['Con WiFi','Sin WiFi'], 'green', 'darkgreen','WiFi')
    elif option_slctd == 'Device_Category':
        fig = users_explore(pd.value_counts(users[option_slctd]), ['Celular','Tablet','Otro'], 'rgb(158,202,225)', 'rgb(8,48,107)','Dispositivo')
    elif option_slctd == 'sourceMedium':
        fig = users_explore(pd.value_counts(users[option_slctd]).head(10), pd.value_counts(users[option_slctd]).head(10).index, 'tomato', 'orangered','Medio')
    elif option_slctd == 'Channel':
        fig = users_explore(pd.value_counts(users[option_slctd]).head(10), pd.value_counts(users[option_slctd]).head(10).index, 'gray', 'dimgrey','Canal')
    elif option_slctd == 'Carrier':
        fig = users_explore(pd.value_counts(users[option_slctd]).head(10), pd.value_counts(users[option_slctd]).head(10).index, 'gold', 'goldenrod','Carrier')
    else:
        fig = users_explore(pd.value_counts(users[option_slctd]).head(10), pd.value_counts(users[option_slctd]).head(10).index, 'hotpink', 'purple','Operador')
    return fig

@app.callback(
    Output(component_id='barplot_cross', component_property='figure'),
    [Input(component_id='slct_var12', component_property='value')])

def update_graph1(option_slctd1):
    if option_slctd1 == 'Hour':
        fig =  cross_bars(users, option_slctd1, head=24)
    else:
        fig =  cross_bars(users, option_slctd1, head=5)
    return fig

@app.callback(Output(component_id='bubble_merge_var', component_property='figure'),
              [Input(component_id='slct_var2', component_property='value')])

def update_graph2(option_slctd2):
    #container = "The year chosen by user was: {}".format(option_slctd)
    if option_slctd2 == 'Hour':
        return bubble_merge(merge31,merge32,'Hour', 'green','orange','Ocurrencia por hora y tipos de ambos eventos.','Hora')
    else:
        return bubble_merge(merge21,merge22,'only_date', 'red','blue','Ocurrencia por fecha y tipos de ambos eventos.','Fecha')

@app.callback(Output(component_id='bubble_user', component_property='figure'),
              [Input(component_id='slct_var21', component_property='value')])

def update_graph2(option_slctd2):
    #container = "The year chosen by user was: {}".format(option_slctd)
    if option_slctd2 == 'Hour':
        return bubble_plot(users2,'Hour','Event_Name','clientID' ,'green', "Ocurrencia de cada eventoA por hora",'Hora','Evento',size_b=40)
    else:
        return bubble_plot(users3,'fecha','Event_Name','clientID' ,'purple', "Ocurrencia de cada eventoA por fecha",'Fecha','Evento',size_b=50)


@app.callback(Output(component_id='bubble_event', component_property='figure'),
              [Input(component_id='slct_var22', component_property='value')])

def update_graph3(option_slctd3):
    #container = "The year chosen by user was: {}".format(option_slctd)
    if option_slctd3 == 'Hour':
        return bubble_plot(events2,'event_name','start_hour','start_date' ,'red', "Ocurrencia de cada eventoB por hora",'Evento','Hora del día',size_b=15)
    else:
        return bubble_plot(events3,'event_name','date','start_date' ,'orange', "Ocurrencia de cada eventoB por fecha",'Evento','Fecha',size_b=18)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
