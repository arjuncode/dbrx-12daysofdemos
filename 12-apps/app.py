import dash
from dash import dcc, html, Input, Output, State, callback, no_update, ctx
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd
import psycopg
from psycopg import sql
from psycopg_pool import ConnectionPool
import time
import os
from databricks import sdk

# --- DATABASE CONNECTION SETUP (Unchanged) ---
workspace_client = sdk.WorkspaceClient()
postgres_password = None
last_password_refresh = 0
connection_pool = None

def refresh_oauth_token():
    global postgres_password, last_password_refresh
    if postgres_password is None or time.time() - last_password_refresh > 900:
        try:
            postgres_password = workspace_client.config.oauth_token().access_token
            last_password_refresh = time.time()
        except Exception as e:
            print(f"❌ Failed to refresh OAuth token: {str(e)}")
            return False
    return True

def get_connection_pool():
    global connection_pool
    if connection_pool is None:
        if not refresh_oauth_token():
            raise Exception("Could not acquire OAuth token for DB connection")
        conn_string = (
            f"dbname={os.getenv('PGDATABASE')} "
            f"user={os.getenv('PGUSER')} "
            f"password={postgres_password} "
            f"host={os.getenv('PGHOST')} "
            f"port={os.getenv('PGPORT')} "
            f"sslmode={os.getenv('PGSSLMODE', 'require')} "
            f"application_name={os.getenv('PGAPPNAME', 'gift_app')}"
        )
        connection_pool = ConnectionPool(conn_string, min_size=2, max_size=10)
    return connection_pool

def get_connection():
    global connection_pool
    if postgres_password is None or time.time() - last_password_refresh > 900:
        if connection_pool:
            connection_pool.close()
            connection_pool = None
    return get_connection_pool().connection()

def fetch_data():
    empty_df = pd.DataFrame(columns=[
        'request_id', 'timestamp', 'child_id', 'latitude', 'longitude', 
        'country', 'primary_gift_category', 'gift_count',
        'delivery_preference', 'en_route', 'delivered', 'cookies'
    ])
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                query = "SELECT * FROM public.gift_requests_pg"
                cur.execute(query)
                rows = cur.fetchall()
                if cur.description:
                    colnames = [desc[0] for desc in cur.description]
                    return pd.DataFrame(rows, columns=colnames)
                return empty_df
    except Exception as e:
        print(f"Query Error: {e}")
        return empty_df

def update_record(request_id, column, value):
    if column in ['en_route', 'delivered']:
        value = bool(value)
    if column == 'cookies':
        value = int(value) if value is not None else 0
    query = sql.SQL("UPDATE public.gift_requests_pg SET {} = %s WHERE request_id = %s").format(sql.Identifier(column))
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, (value, request_id))
            conn.commit()
        return True
    except Exception as e:
        print(f"Update Error: {e}")
        return False

# --- LOAD DATA ---
df = fetch_data()

# --- APP CONFIG & CUSTOM CSS ---
# Using CYBORG for dark mode foundation + Google Fonts
external_stylesheets = [
    dbc.themes.CYBORG,
    "https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Custom CSS to force DM Sans, fix Dropdown colors in dark mode, and round corners
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>

            :root {{
                --background-color: #081B16;
                --card-bg: #0D3128;
                --selection-bg: #0D3128;
                --text-title: #CC1417;
                --text-primary: #eff1ed;
                --text-secondary: #6f7370;
            }}

            /* GLOBAL FONT */
            body, h1, h2, h3, h4, h5, h6, .card, .toast, .dash-table-container, .ag-theme-alpine-dark {
                font-family: 'DM Sans', sans-serif !important;
            }
            
            /* GLOBAL FOCUS REMOVAL */
            *:focus {
                outline: none !important;
                box-shadow: none !important;
            }

            /* DARK MODE DROPDOWNS OVERRIDES - NO BORDERS */
            .Select-control {
                background-color: #1a1a1a !important;
                border: none !important;
                border-radius: 8px !important;
                color: white !important;
                box-shadow: none !important;
            }
            .Select-value-label {
                color: white !important;
            }
            .Select-menu-outer {
                background-color: #1a1a1a !important;
                border: none !important;
                color: white !important;
            }
            .Select-option {
                background-color: #1a1a1a !important;
                color: white !important;
            }
            .Select-option:hover {
                background-color: #007bff !important;
            }
            .Select-placeholder {
                color: #aaa !important;
            }
            
            /* GENERAL UI TWEAKS - NO BORDERS */
            .card {
                background-color: #111 !important; /* Darker cards */
                border: none !important;
                border-radius: 12px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3); /* Soft shadow instead of border */
            }
            .toast {
                background-color: #222 !important;
                color: white !important;
                border: none !important;
            }
            /* Map container radius and cleanup */
            #map-graph .main-svg {
                border-radius: 12px;
                border: none !important;
            }
            
            /* AG GRID NO BORDERS */
            .ag-theme-alpine-dark {
                border: none !important;
            }
            .ag-root-wrapper {
                border: none !important;
            }

            body {
                margin: 50px 100px;
            }

        </style>
    </head>
    <body>
    
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# --- LAYOUT COMPONENTS ---

def create_filter_card():
    def safe_unique(col):
        return sorted(df[col].unique()) if col in df and not df.empty else []

    # Common style for labels
    label_style = {"color": "#aaa", "fontSize": "0.85rem", "marginBottom": "5px"}

    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.Label("Country", style=label_style),
                    dcc.Dropdown(
                        id='filter-country',
                        options=safe_unique('country'),
                        multi=True,
                        placeholder="All Countries"
                    )
                ], width=3),
                dbc.Col([
                    html.Label("Gift Category", style=label_style),
                    dcc.Dropdown(
                        id='filter-category',
                        options=safe_unique('primary_gift_category'),
                        multi=True,
                        placeholder="All Categories"
                    )
                ], width=3),
                dbc.Col([
                    html.Label("Delivery Mode", style=label_style),
                    dcc.Dropdown(
                        id='filter-preference',
                        options=safe_unique('delivery_preference'),
                        multi=True,
                        placeholder="All Modes"
                    )
                ], width=2),
                dbc.Col([
                    html.Label("Status: En Route", style=label_style),
                    dcc.Dropdown(
                        id='filter-enroute',
                        options=[{'label': 'Yes', 'value': True}, {'label': 'No', 'value': False}],
                        multi=True,
                        placeholder="Any"
                    )
                ], width=2),
                dbc.Col([
                    html.Label("Status: Delivered", style=label_style),
                    dcc.Dropdown(
                        id='filter-delivered',
                        options=[{'label': 'Yes', 'value': True}, {'label': 'No', 'value': False}],
                        multi=True,
                        placeholder="Any"
                    )
                ], width=2),
            ], className="g-3") # g-3 gives more breathing room
        ]),
        className="mb-4 shadow-lg", # shadow-lg for depth
        style={"backgroundColor": "#1e1e1e"} 
    )

columnDefs = [
    {"field": "request_id", "hide": True},
    {"field": "child_id", "headerName": "Child ID", "width": 200, "pinned": "left"},
    {"field": "country", "headerName": "Country", "filter": True},
    {"field": "primary_gift_category", "headerName": "Category"},
    {
        "field": "en_route", 
        "headerName": "En Route", 
        "editable": True, 
        "cellDataType": "boolean",
        "width": 200,
        "cellStyle": {"textAlign": "center"}
    },
    {
        "field": "delivered", 
        "headerName": "Delivered", 
        "editable": True, 
        "cellDataType": "boolean",
        "width": 200,
        "cellStyle": {"textAlign": "center"}
    },
    {
        "field": "cookies", 
        "headerName": "Cookies", 
        "editable": True,
        # "type": "numericColumn",
        "cellEditor": "agNumberCellEditor",
        "cellEditorParams": {"min": 0, "step": 1},
        "width": 200,
        "cellStyle": {"fontWeight": "bold", "color": "#0dcaf0"}, # Cyan color for interactive feel
        "cellStyle": {"textAlign": "center"}
    },
    {"field": "letter_text", "headerName": "Letter Content", "flex": 1, "tooltipField": "letter_text"}
]

# --- MAIN LAYOUT ---
app.layout = dbc.Container([
    # Title Section
    dbc.Row(
        dbc.Col(
            html.Div([
                html.H2("North Pole Delivery Command Center", className="fw-bold mb-0 text-white"),
                html.P("Real-time logistics and gift request tracking system", className="text-muted mt-1")
            ], className="py-4")
        )
    ),
    
    # Filter Card
    dbc.Row(dbc.Col(create_filter_card())),
    
    # Map Section
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        id='map-graph', 
                        config={'displayModeBar': False},
                        style={'height': '35vh', 'borderRadius': '8px', 'overflow': 'hidden'}
                    ),
                    className="p-1" # Thin padding
                ),
                className="mb-4 border-0 shadow-lg"
            ),
            width=12
        )
    ),
    
    # Grid Section
    dbc.Row(
        dbc.Col(
            html.Div([
                dag.AgGrid(
                    id="gift-grid",
                    rowData=df.to_dict("records"),
                    columnDefs=columnDefs,
                    defaultColDef={"resizable": True, "sortable": True, "filter": True},
                    dashGridOptions={"pagination": True, "paginationPageSize": 20, "rowHeight": 45},
                    getRowId="params.data.request_id",
                    style={"height": "40vh", "width": "100%"},
                    # DARK THEME FOR GRID
                    className="ag-theme-alpine-dark" 
                )
            ], className="shadow-lg rounded overflow-hidden"),
            width=12
        )
    ),
    
    # Notifications
    dbc.Toast(
        id="update-toast",
        header="Database Update",
        is_open=False,
        dismissable=True,
        icon="info",
        duration=4000,
        style={"position": "fixed", "top": 20, "right": 20, "width": 350, "zIndex": 9999},
    ),
], fluid=True, style={'minHeight': '100vh', 'backgroundColor': '#000000'})


# --- MASTER CALLBACK (Unchanged Logic, Updated Styles) ---
@callback(
    [Output('gift-grid', 'rowData'),
     Output('map-graph', 'figure'),
     Output('update-toast', 'is_open'),
     Output('update-toast', 'children')],
    [Input('filter-country', 'value'),
     Input('filter-category', 'value'),
     Input('filter-preference', 'value'),
     Input('filter-enroute', 'value'),
     Input('filter-delivered', 'value'),
     Input('gift-grid', 'cellValueChanged')]
)
def master_callback(countries, categories, prefs, en_route, delivered, cell_change):
    global df
    toast_open = False
    toast_msg = ""
    
    # 1. UPDATE
    if ctx.triggered_id == 'gift-grid' and cell_change:
        change = cell_change[0]
        row_id = change['data']['request_id']
        col_id = change['colId']
        new_val = change['value']
        
        success = update_record(row_id, col_id, new_val)
        if success:
            df.loc[df['request_id'] == row_id, col_id] = new_val
            toast_open = True
            toast_msg = f"Request {change['data'].get('child_id', 'Unknown')} updated."
        else:
            toast_open = True
            toast_msg = "Error: Database update failed."

    # 2. FILTER
    dff = df.copy()
    if countries: dff = dff[dff['country'].isin(countries)]
    if categories: dff = dff[dff['primary_gift_category'].isin(categories)]
    if prefs: dff = dff[dff['delivery_preference'].isin(prefs)]
    if en_route is not None and len(en_route) > 0: dff = dff[dff['en_route'].isin(en_route)]
    if delivered is not None and len(delivered) > 0: dff = dff[dff['delivered'].isin(delivered)]

    # 3. MAP (Dark Mode Style)
    if not dff.empty:
        fig = px.scatter_mapbox(
            dff, 
            lat="latitude", 
            lon="longitude", 
            color="primary_gift_category",
            # hover_name="child_id",
            # hover_data=["cookies", "gift_count"],
            zoom=1,
            mapbox_style="carto-darkmatter"
        )
        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor="rgba(0, 0, 0, 0)", # Match card background
            plot_bgcolor="rgba(0, 0, 0, 0)",
            font={"family": "DM Sans", "color": "white"},
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"),
            ),
            legend_title_text='<b>Primary Gift Category</b>'
        )
    else:
        fig = px.scatter_mapbox(lat=[], lon=[], mapbox_style="carto-darkmatter")
        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor="#111",
            plot_bgcolor="#111",
            font={"family": "DM Sans", "color": "white"}
        )

    return dff.to_dict("records"), fig, toast_open, toast_msg

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)