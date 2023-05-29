from dash import dash, html, dcc,Input ,Output, dash_table
import pandas as pd

import csv
import numpy as np
from pandas import Series, DataFrame
import plotly.express as px
from datetime import datetime as dt
import dash_bootstrap_components as dbc
import matplotlib.pyplot as plt 

project = dash.Dash(__name__)
df = pd.read_csv("Sales_data.csv")
df.info()
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
mf = df.groupby(df["Order_Date"].dt.strftime("%B"))["Units_Sold"].sum()
df.insert(6,"Month",df["Order_Date"].dt.strftime("%B"))
print(df)
df.info()
print(df.iloc[:,[6]])
dff = df.groupby(["Item_Type", "Region", "Month"])["Units_Sold"].sum().reset_index()
print(dff)
lff = df.groupby(["Item_Type", "Region", "Month"])["Total profit"].sum().reset_index()
print(lff)
hf = df.groupby(df["Order_Date"].dt.strftime("%Y"))["Total profit"].sum()
print(hf)
print(mf)
ef =df.groupby(df["Region"])["Total profit"].sum()
lf = df.groupby(df["Region"])["Units_Sold"].sum()
print(ef)
print(lf)
fig = px.bar(x = ef.index, y = ef , color = ef.index, title= "Total Profit Region-wise")
fig.update_layout(
    xaxis_title = "Region",
    yaxis_title = "Profit"
)
fig1= px.pie(lf, values=lf, names=lf.index, title='Total Units Sold Region-wise')

fig2= px.line(mf, x=mf.index, y =mf,  title="Units sold monthly")
fig2.add_bar(x= mf.index , y = mf, )
fig2.update_layout(
    xaxis_title = "Month",
    yaxis_title = "Units Sold"
)
fig3 = px.line(hf, x= hf.index , y = hf, title="Yearly profit on sales")
fig3.update_layout(
    xaxis_title = "Year",
    yaxis_title = "Profit"
)

Offline = pd.Series([])    
for i in range(len(df)):
    if df["Sales_Channel"][i] == "Offline":
        Offline[i] = df["Total profit"][i].sum()
    else:
        Offline[i] = 0
df.insert(2,"Offline",Offline)


Online = pd.Series([])    
for i in range(len(df)):
    if df["Sales_Channel"][i] == "Online":
        Online[i] = df["Total profit"][i].sum()
    else:
        Online[i] = 0
df.insert(3,"Online",Online)
nf = df.loc[:,["Country", "Item_Type", "Offline","Online"]]

gf = nf.groupby(["Country","Item_Type"], as_index = False)[["Offline","Online"]].sum()
print(gf)


project.layout = html.Div([
            html.H1("Sales Dashboard", style={"font-size": "40px", "text-align": "center"}),
           html.Br(),
        html.Div([
        dcc.Graph(figure=fig ,  style={'float': 'left'} ),
        
        dcc.Graph(figure=fig1,  style={'float': 'left'}),
        
        dcc.Graph(figure= fig2,  style={'float': 'left'}),
        
        dcc.Graph(figure = fig3,  style={'float': 'left'} ),
        
        ]),
        html.Br(),
        html.Br(),
    
    
          html.Div([
            html.H1('Item Type',style={'font-size': '20px'} ),
        dcc.Dropdown(
            id="price_drop",
            style={'width': '200px', 'margin-left': 10},
                options=[{'label': x  , 'value': x  } for x in df["Item_Type"].unique()],
                value = "Beverages"),
            ], style = {"display": "inline-block", "margin-right": "20px"}),
        html.Div([
        html.H1('Month' ,style = {'font-size': '20px', "margin-left": 100}),
        dcc.Dropdown(
            id="Monthly_sale",
            style={'width': '200px', 'margin-left':60},
                options = [{'label': y , 'value': y } for y in df["Month"].unique()],
                value = "May"
                
      ),
            ], style = {"display": "inline-block", "margin-right": "20px"}),
        html.Div([
        html.H1('Region' , style = {'font-size':'20px', "margin-left": 200}),
        dcc.Dropdown(
            id="region",
            style = {'width': '200px', 'margin-left': 110},
                options=[{'label': z , 'value': z } for z in
                         df["Region"].unique()],
        value = "Europe"),
        ], style = {"display": "inline-block", "margin-right": "20px"}),
        html.Br(),
        html.Br(),
    
    
        html.Div([
        html.Div([
        dash_table.DataTable(data=gf.to_dict('records'),
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in gf.columns],
                filter_action='native',
                
                            
        style_cell_conditional=[
                                {
            'if': {'column_id': c},
            'textAlign': 'left'
            } for c in ['Country', 'Item_Type']
       
        ],
        style_data={
            'color': 'black',
            'backgroundColor': 'white'
            },
        style_data_conditional = [
            {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)'
            },
        ],
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',
            'fontWeight': 'bold'
                    },
        
                            ),  
        ], style ={"width": "50%" , "float": "left"} ),       
          
            
        
        
        html.Div([
        
    
            dcc.Graph(id = "map1"),
    
            dcc.Graph(id= "map2"),
    
            dcc.Graph(id = "map3"),
            
            dcc.Graph(id = "map4"),
            
            dcc.Graph(id = "map5"),
            
            dcc.Graph(id = "map6"),
        
        
        
        
        
         
        
        
        ],  style={'display': 'flex', 'justify-content': 'space-between', 'width': '50%', "flex-direction": "column" , "margin":"20px"}
    ),
            
        ]),
        
])
        

@project.callback(
    Output("map1", "figure"),
    [Input("price_drop", "value"),
    Input("region", "value" )]
)

        
def upd(value1, value2):
    if value1 and value2:
    
        filtered_df = dff.loc[(dff["Item_Type"] == value1) & (dff["Region"] == value2)]
        fig = px.bar(filtered_df, x="Month", y="Units_Sold", color="Month")
        fig.update_layout(title=f"Total Units Sold in {value2} for {value1}")
    else:
        fig= {}
    return fig        
 
@project.callback(
    Output("map2", "figure"),
    [Input("price_drop", "value"),
    Input("Monthly_sale", "value" )]
)

def upd1(value1, value3):
    if value1 and value3:
    
        filtered_df = dff.loc[(dff["Item_Type"] == value1) & (dff["Month"] == value3)]
        fig = px.bar(filtered_df, x="Region", y="Units_Sold", color="Region")
        fig.update_layout(title=f"Total Units Sold in {value3} for {value1}")
    else:
        fig= {}
    return fig        
      
@project.callback(
    Output("map3", "figure"),
    [Input("region", "value"),
    Input("Monthly_sale", "value" )]
)

def upd2(value2, value3):
    if value2 and value3:
    
        filtered_df = dff.loc[(dff["Region"] == value2) & (dff["Month"] == value3)]
        fig = px.bar(filtered_df, x="Item_Type", y="Units_Sold", color="Item_Type")
        fig.update_layout(title=f"Total Units Sold in {value3} for {value2}")
    else:
        fig= {}
    return fig           

@project.callback(
    Output("map4", "figure"),
    [Input("price_drop", "value"),
     Input("region","value")]
)

def upd3(value1, value2):
    if value1 and value2:
        filtered_lf = lff.loc[(lff["Item_Type"] == value1) & (lff["Region"] == value2)]
        
        fig = px.bar(filtered_lf, x= "Month" , y = "Total profit", color = "Month")
        fig.update_layout(title = f"Total profit in {value2} of {value1}")
    else:
        fig = {}
    return fig


@project.callback(
    Output("map5", "figure"),
    [Input("price_drop", "value"),
     Input("Monthly_sale","value")]
)

def upd3(value1, value3):
    if value1 and value3:
        filtered_lf = lff.loc[(lff["Item_Type"] == value1) & (lff["Month"] == value3)]
        print(filtered_lf)
        fig = px.bar(filtered_lf, x= "Region" , y = "Total profit", color = "Region")
        fig.update_layout(title = f"Total profit in {value3} of {value1}")
    else:
        fig = {}
    return fig

@project.callback(
    Output("map6", "figure"),
    [Input("region", "value"),
     Input("Monthly_sale","value")]
)

def upd3(value2, value3):
    if value2 and value3:
        filtered_lf = lff.loc[(lff["Region"] == value2) & (lff["Month"] == value3)]
        print(filtered_lf)
        fig = px.bar(filtered_lf, x= "Item_Type" , y = "Total profit", color = "Item_Type")
        fig.update_layout(title = f"Total profit in {value3} of {value2}")
    else:
        fig = {}
    return fig



    

if __name__ == "__main__":
    project.run_server(debug=True, port= 8055)