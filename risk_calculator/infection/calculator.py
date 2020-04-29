import pickle
import sklearn
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from footer import Footer

from risk_calculator.utils import convert_temp_units, predict_risk, valid_input
from risk_calculator.visuals import get_labs_indicator,get_model_desc,get_feature_importance, get_inputed_vals
from risk_calculator.visuals import get_feature_cards, get_feature_cards, get_submit_button, get_results_card

nav = Navbar()
footer = Footer()

with open('assets/risk_calculators/infection/model_with_lab.pkl', 'rb') as file:
    labs = pickle.load(file)

with open('assets/risk_calculators/infection/model_without_lab.pkl', 'rb') as file:
    no_labs = pickle.load(file)

labs_model_infec = labs["model"]
labs_imputer_infec = labs["imputer"]
labs_features_infec = labs["json"]

no_labs_model_infec = no_labs["model"]
no_labs_imputer_infec = no_labs["imputer"]
no_labs_features_infec = no_labs["json"]

body = dbc.Container(
    [
        dbc.Row(
        [
            dbc.Col(
            [
                dbc.Jumbotron(
                [
                    html.H2("Analytics can identify infected patients"),
                    dcc.Markdown(
                         """COVID-19 tests are time consuming, expensive and require patients to visit \
                         facilities in person, increasing exposure to the virus. To help identifying \
                         symptomatic patients, we developed a data-driven calculator to predict the \
                         probability of being infected.
                         """,
                    ),
                    html.Hr(),
                    dcc.Markdown(
                         """ **NOTE (This is a developmental version!)::** A model is only as good as the \
                         data it is trained on. We will release new versions of the calculator as the \
                         amount of data we receive from our partner institutions increases. If you are a \
                         medical institution and are willing to contribute to our effort, please reach out \
                         to us [here](https://www.covidanalytics.io/contact).
                         """,
                    )
                ]
                )
            ]
            ),
        ],
        )
    ] + \
    get_labs_indicator('lab_values_indicator_infection') + \
    get_feature_cards('features-infection') + \
    get_submit_button('submit-features-calc-infection') + \
    get_results_card('score-calculator-card-body-infection','calc-input-error-infection') + \
    get_inputed_vals('imputed-text-infection') + \
    get_model_desc('infection-model-desc') + \
    get_feature_importance('feature-importance-bar-graph-infection'),
    className="page-body"
)

def InfectionRiskCalc():
    layout = html.Div([nav, body, footer], className="site")
    return layout

def valid_input_infec(labs,feature_vals):
    if labs:
        features = labs_features_infec
        imputer = labs_imputer_infec
    else:
        features = no_labs_features_infec
        imputer = no_labs_imputer_infec
    length = len(features["numeric"])
    return valid_input(features["numeric"],feature_vals[0],length)

def predict_risk_infec(labs,feature_vals):
    if labs:
        cols = ['C-Reactive Protein (CRP)', 'Blood Calcium', 'CBC: Leukocytes', 'Aspartate Aminotransferase (AST)', \
        'ABG: PaO2', 'Age', 'Prothrombin Time (INR)', 'CBC: Hemoglobin', 'ABG: pH', 'Cholinesterase', 'Respiratory Frequency', \
        'Blood Urea Nitrogen (BUN)', 'ABG: MetHb', 'Temperature Celsius', 'Total Bilirubin', 'Systolic Blood Pressure', \
        'CBC: Mean Corpuscular Volume (MCV)', 'Glycemia', 'Cardiac Frequency', 'Sex']
    else:
        cols = ['Age', 'Cardiac Frequency', 'Respiratory Frequency', 'SaO2', 'Sex', 'Systolic Blood Pressure', 'Temperature Celsius']
    if labs:
        model = labs_model_infec
        features = labs_features_infec
        imputer = labs_imputer_infec
    else:
        model = no_labs_model_infec
        features = no_labs_features_infec
        imputer = no_labs_imputer_infec
    score,impute_text = predict_risk(False,model,features,imputer,feature_vals,cols)
    card_content = [
        html.H4("The infection risk score is:",className="score-calculator-card-content-infection"),
        html.H4(score,className="score-calculator-card-content-infection"),
    ]
    return card_content,impute_text



def get_model_desc_infection(labs):
    if labs:
        auc = html.Div(
             [
             "The calculator is based on [XGBoost classifier](https://xgboost.readthedocs.io/).",html.Br(),
             "The out of sample area under the curve (AUC) on 209 patients (out of whom 73% infected) is ",
             html.Span(' 0.91', style={'color': '#800020',"fontWeight":"bold"}), ".",html.Br(),\
             "When features are missing, the calculator will impute and report their values."
             ]
        )
    else:
        auc = html.Div(
            [
             "The calculator is based on [XGBoost classifier](https://xgboost.readthedocs.io/).",html.Br(),
             "The out of sample area under the curve (AUC) on 209 patients (out of whom 73% infected) is ",
             html.Span(' 0.85', style={'color': '#800020',"fontWeight":"bold"}), ".",html.Br(),\
             "When features are missing, the calculator will impute and report their values."
             ]
        )

    return [ \
        html.H2("Technical details"),
        dcc.Markdown(
             """
             Our model was trained on 1880 patients (out of whom 73% COVID-19 positive) \
             who visited the emergency room in the italian city of Cremona \
             ([Azienda Socio-Sanitaria Territoriale di Cremona](https://www.asst-cremona.it/en/home)). \
             Cremona is one of the most severely hit italian provinces in Lombardy with several thousand \
             positive cases to date.
             """,
        ),
        html.Hr(),
        auc,
        html.Br(),
        dcc.Markdown(
             """Overall, the importance of the features is as follows:""",
        )
    ]
