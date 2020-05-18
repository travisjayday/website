import pickle

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar
from footer import Footer

from risk_calculator.utils import convert_temp_units, predict_risk, valid_input, get_oxygen_ind
from risk_calculator.utils import cols_labs_mort, cols_no_labs_mort
from risk_calculator.visuals import get_labs_indicator,get_model_desc,get_feature_importance, get_inputed_vals
from risk_calculator.visuals import get_feature_cards, get_feature_cards, get_submit_button, get_results_card
from risk_calculator.visuals import get_lang,get_page_desc, get_personal_visual

nav = Navbar()
footer = Footer()

oxygen_in_mort = "SaO2" in cols_no_labs_mort or 'ABG: Oxygen Saturation (SaO2)' in cols_no_labs_mort
oxygen_in_mort_labs = "SaO2" in cols_labs_mort or 'ABG: Oxygen Saturation (SaO2)' in cols_labs_mort
oxygen_mort_ind = get_oxygen_ind(True)

body = dbc.Container(
        get_lang('language-calc-mortality') + \
        get_page_desc('page-desc-mortality') + \
        get_labs_indicator('lab_values_indicator') + \
        get_feature_cards('features-mortality') + \
        get_submit_button('submit-features-calc') + \
        get_results_card('score-calculator-card-body','calc-input-error') + \
        get_inputed_vals('imputed-text-mortality') + \
        get_personal_visual('visual-1-mortality') + \
        get_model_desc('mortality-model-desc') + \
        get_feature_importance('feature-importance-bar-graph'),
        className="page-body"
    )


def RiskCalc():
    layout = html.Div([nav, body, footer], className="site")
    return layout

def valid_input_mort(labs,feature_vals,language):
    if labs:
        with open('assets/risk_calculators/mortality/labs_imputer.pkl', 'rb') as file:
            imputer_pickle = pickle.load(file)
        with open('assets/risk_calculators/mortality/labs_json.pkl', 'rb') as file:
            features_pickle = pickle.load(file)
    else:
        with open('assets/risk_calculators/mortality/without_labs_imputer.pkl', 'rb') as file:
            imputer_pickle = pickle.load(file)
        with open('assets/risk_calculators/mortality/without_labs_json.pkl', 'rb') as file:
            features_pickle = pickle.load(file)
    features = features_pickle["json"]
    imputer = imputer_pickle["imputer"]
    length = len(features["numeric"])
    return valid_input(features["numeric"],feature_vals[0],length,language)

def predict_risk_mort(labs,feature_vals,temp_unit,card_text,language):
    if labs:
        with open('assets/risk_calculators/mortality/labs_imputer.pkl', 'rb') as file:
            imputer_pickle = pickle.load(file)
        with open('assets/risk_calculators/mortality/labs_json.pkl', 'rb') as file:
            features_pickle = pickle.load(file)
        with open('assets/risk_calculators/mortality/labs_model_explainer.pkl', 'rb') as file:
            model_pickle = pickle.load(file)
        cols = cols_labs_mort
    else:
        with open('assets/risk_calculators/mortality/without_labs_imputer.pkl', 'rb') as file:
            imputer_pickle = pickle.load(file)
        with open('assets/risk_calculators/mortality/without_labs_json.pkl', 'rb') as file:
            features_pickle = pickle.load(file)
        with open('assets/risk_calculators/mortality/without_labs_model_explainer.pkl', 'rb') as file:
            model_pickle = pickle.load(file)
        cols = cols_no_labs_mort
    model = model_pickle["model"]
    features = features_pickle["json"]
    imputer = imputer_pickle["imputer"]
    explainer = model_pickle["explainer"]

    score,imputed_text,plot = predict_risk(True,model,features,imputer,explainer,feature_vals,cols,temp_unit,labs,language)
    card_content = [
        html.H4(card_text,className="score-calculator-card-content"),
        html.H4(str(score)+"%",className="score-calculator-card-content"),
    ]
    return card_content,imputed_text,plot
