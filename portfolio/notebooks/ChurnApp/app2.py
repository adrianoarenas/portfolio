import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import State, Output, Input
from dash.exceptions import PreventUpdate
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import numpy as np
import pandas as pd
import pickle

###########################################################
##########READ IN DATA AND LOAD MODEL FROM PICKLE##########
###########################################################

dfA = pd.read_csv('Company A - Data.csv')

#PICKLE LOADING
#IF A NEW MODEL IS TRAINED, JUST CHANGE THIS PICKLE FILE
########################################################
model = pickle.load(open('daip5_V2.pkl', 'rb'))
########################################################

cols = dfA.drop(['customerID','Unnamed: 0','Churn','TotalCharges'], axis=1)



def fit_models_and_clean(x):
    x.drop(['Unnamed: 0', 'customerID','TotalCharges'], axis=1, inplace=True)
    x = x.replace(r'^\s*$', 0, regex=True)
#    x['TotalCharges'] = pd.to_numeric(x['TotalCharges'])
    return (x)

xA = fit_models_and_clean(dfA)

xA.gender.replace(('Male', 'Female'), (1, 0), inplace=True)
xA.Partner.replace(('Yes', 'No'), (1, 0), inplace=True)
xA.Dependents.replace(('Yes', 'No'), (1, 0), inplace=True)
xA.PhoneService.replace(('Yes', 'No'), (1, 0), inplace=True)
xA.PaperlessBilling.replace(('Yes', 'No'), (1, 0), inplace=True)
xA.dropna(axis=0, inplace=True)

ohe = OneHotEncoder(categories='auto', drop='first')
feature_arr = ohe.fit_transform(xA[['InternetService', 'OnlineSecurity', 'OnlineBackup',
                                   'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                                   'Contract', 'PaymentMethod', 'MultipleLines']]).toarray()
features = pd.DataFrame(feature_arr)
total_x = pd.concat([xA, features], axis=1)
total_x.drop(['InternetService', 'OnlineSecurity', 'OnlineBackup',
              'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
              'Contract', 'PaymentMethod', 'MultipleLines'], axis=1, inplace=True)

X = total_x.drop(['Churn'], axis=1)
y = total_x['Churn']
X_train, X_test, y, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)
scaler = StandardScaler()
scaled = scaler.fit_transform(X_train)




###################################
#############DASHBOARD#############
###################################

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Churn Prediction'),
    html.Div(children='''Please enter the variables you would like to predict: '''),
    html.Div(children='''------------------------------------------------------------'''),

    html.Div(children=[
    html.Label('Select Gender'),
    dcc.Dropdown(
        id='gender',
        options=[{'label': 'male', 'value': 1},
                 {'label': 'female', 'value': 0}
        ],
        style={"width": "50%"},
        value=1
    ),

    html.Label('Select seniority'),
    dcc.Dropdown(
        id='senior',
        options=[{'label': 'senior', 'value': 1},
                 {'label': 'not senior', 'value': 0}
        ],
        style={"width": "50%"},
        value=1
    ),

    html.Label('Select partner'),
    dcc.Dropdown(
        id='partner',
        options=[{'label': 'has partner', 'value': 1},
                 {'label': 'no partner', 'value': 0}
        ],
        style={"width": "50%"},
        value=1
    ),

    html.Label('Select dependents'),
    dcc.Dropdown(
        id='dependents',
        options=[{'label': 'has dependents', 'value': 1},
                 {'label': 'no dependents', 'value': 0}
        ],
        style={"width": "50%"},
        value=1
    ),

    html.Label('Tenure'),
    dcc.Input(id='tenure', type="number", value=0
    ),

    html.Label('Select phone service'),
    dcc.Dropdown(
        id='phoneservice',
        options=[{'label': 'has phone service', 'value': 1},
                 {'label': 'no phone service', 'value': 0}
        ],
        style={"width": "50%"},
        value=1
    ),

    html.Label('Select multiple lines'),
    dcc.Dropdown(
        id='multiplelines',
        options=[{'label': 'multiple lines', 'value': 'Yes'},
                {'label': 'no multiple lines', 'value': 'No'},
                {'label': 'no phone service', 'value': 'No phone service'}
        ],
        style={"width": "50%"},
        value='Yes'
    ),

    html.Label('Select internet service'),
    dcc.Dropdown(
        id='internetservice',
        options=[{'label': 'fiber optic', 'value': 'Fiber optic'},
                {'label': 'no internet service', 'value': 'No'},
                {'label': 'DSL', 'value': 'DSL'}
        ],
        style={"width": "50%"},
        value='Fiber optic'
    ),

    html.Label('Select online security'),
    dcc.Dropdown(
        id='onlinesecurity',
        options=[{'label': 'online security', 'value': 'Yes'},
                {'label': 'no online security', 'value': 'No'},
                {'label': 'no internet service', 'value': 'No internet service'}
        ],
        style={"width": "50%"},
        value='Yes'
    ),

    html.Label('Select online backup'),
    dcc.Dropdown(
        id='onlinebackup',
        options=[{'label': 'online backup', 'value': 'Yes'},
                {'label': 'no online backup', 'value': 'No'},
                {'label': 'no internet service', 'value': 'No internet service'}
        ],
        style={"width": "50%"},
        value='Yes'
    ),

    html.Label('Select device protection'),
    dcc.Dropdown(
        id='deviceprotection',
        options=[{'label': 'device protection', 'value': 'Yes'},
                {'label': 'no device protection', 'value': 'No'},
                {'label': 'no internet service', 'value': 'No internet service'}
        ],
        style={"width": "50%"},
        value='Yes'
    ),

    html.Label('Select tech support'),
    dcc.Dropdown(
        id='techsupport',
        options=[{'label': 'tech support', 'value': 'Yes'},
                {'label': 'no tech support', 'value': 'No'},
                {'label': 'no internet service', 'value': 'No internet service'}
        ],
        style={"width": "50%"},
        value='Yes'
    ),

    html.Label('Select streaming tv'),
    dcc.Dropdown(
        id='streamingtv',
        options=[{'label': 'streaming tv', 'value': 'Yes'},
                {'label': 'no streaming tv', 'value': 'No'},
                {'label': 'no internet service', 'value': 'No internet service'}
        ],
        style={"width": "50%"},
        value='Yes'
    ),

    html.Label('Select streaming movies'),
    dcc.Dropdown(
        id='stremingmovies',
        options=[{'label': 'streaming movies', 'value': 'Yes'},
                {'label': 'no streaming movies', 'value': 'No'},
                {'label': 'no internet service', 'value': 'No internet service'}
        ],
        style={"width": "50%"},
        value='Yes'
    ),

    html.Label('Select contract'),
    dcc.Dropdown(
        id='contract',
        options=[{'label': 'two year', 'value': 'Two year'},
                {'label': 'month-to-month', 'value': 'Month-to-month'},
                {'label': 'one year', 'value': 'One year'}
        ],
        style={"width": "50%"},
        value='Month-to-month'
    ),

    html.Label('Select paperless billing'),
    dcc.Dropdown(
        id='paperlessbilling',
        options=[{'label': 'yes', 'value': 1},
                 {'label': 'no', 'value': 0}
        ],
        style={"width": "50%"},
        value=1
    ),

    html.Label('Select payment method'),
    dcc.Dropdown(
        id='paymentmethod',
        options=[{'label': 'Credit card (automatic)', 'value': 'Credit card (automatic)'},
                {'label': 'Bank transfer (automatic)', 'value': 'Bank transfer (automatic)'},
                {'label': 'Electronic check', 'value': 'Electronic check'},
                {'label': 'Mailed check', 'value': 'Mailed check'}
        ],
        style={"width": "50%"},
        value='Credit card (automatic)'
    ),

    html.Label('Monthly Charges'),
    dcc.Input(id='monthlycharges', type="number", value=0
    ),

    html.Div(children='''------------------------------------------------------------'''),

    html.Button('Predict', id='predict_button'),
    html.Div(id='container-button-basic',
            children='Press to predict Churn'),

    html.Div(children='''------------------------------------------------------------'''),
    html.Div(children='''Churn probability:'''),
    html.H6(id='pred_output'),

    ])
])


@app.callback(
    Output('pred_output', 'children'),
    [Input('predict_button', 'n_clicks')],
    state = [State(component_id='gender', component_property='value'),
     State(component_id='senior', component_property='value'),
     State(component_id='partner', component_property='value'),
     State(component_id='dependents', component_property='value'),
     State(component_id='tenure', component_property='value'),
     State(component_id='phoneservice', component_property='value'),
     State(component_id='multiplelines', component_property='value'),
     State(component_id='internetservice', component_property='value'),
     State(component_id='onlinesecurity', component_property='value'),
     State(component_id='onlinebackup', component_property='value'),
     State(component_id='deviceprotection', component_property='value'),
     State(component_id='techsupport', component_property='value'),
     State(component_id='streamingtv', component_property='value'),
     State(component_id='stremingmovies', component_property='value'),
     State(component_id='contract', component_property='value'),
     State(component_id='paperlessbilling', component_property='value'),
     State(component_id='paymentmethod', component_property='value'),
     State(component_id='monthlycharges', component_property='value')]
)

def function(n_clicks,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r):
    if n_clicks:
        data_list = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r]

        in_data = pd.DataFrame([data_list], columns=cols.columns)

        in_data.replace(np.nan, 0, inplace=True)

        xAA = xA.append(in_data).drop(['Churn'], axis=1)
        ohe = OneHotEncoder(categories='auto', drop='first')
        pred_encode = ohe.fit_transform(xAA[['InternetService', 'OnlineSecurity', 'OnlineBackup',
                                             'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                                             'Contract', 'PaymentMethod', 'MultipleLines']].values).toarray()

        feats = pd.DataFrame(pred_encode)
        xAA.reset_index(inplace=True)

        in_data = pd.concat([xAA, feats], axis=1)
        in_data.drop(['InternetService', 'OnlineSecurity', 'OnlineBackup',
                      'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
                      'Contract', 'PaymentMethod', 'MultipleLines', 'index'], axis=1, inplace=True)


        data_ready = scaler.transform(in_data)
        pred_data = data_ready
        Churn_probability = model.predict_proba(pred_data)[:, -1][-1]

    else:
        raise PreventUpdate

    return(Churn_probability)

if __name__ == '__main__':
    app.run_server(debug=True)