import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pickle

path_name = '/Users/adriano/Documents/Misc_Projects/Emissions/{}'
CO_path = path_name.format("CO_model.pkl")
NOx_path = path_name.format("NOx_model.pkl")

CO_model = "CO_model.pkl"
with open(CO_path, 'rb') as file:
    CO_model = pickle.load(file)

NOx_model = 'NOx_model.pkl'
with open(NOx_path, 'rb') as file:
    NOx_model = pickle.load(file)


#CO model variables:
#'Gas turbine exhaust press','Turbine inlet temp','Turbine after temp',
#'Turbine energy yield','Compressor discharge press'

#NOx model variables:
#'Ambient temp','Air filter diff press','Gas turbine exhaust press',
#'Turbine inlet temp','Turbine after temp','Turbine energy yield'

st.title('Gas turbine emissions prediction')
st.header('For the prediction of Carbon Monoxide and Nitric Oxides of a gas-powered turbine in Turkey')
st.header('')

st.sidebar.header('Please input the turbine variables:')

amb_temp = st.sidebar.number_input('Ambient Temperature [Celcius]')
ex_press = st.sidebar.number_input('Exhaust Pressure [mbar]')
in_temp = st.sidebar.number_input('Inlet Temperature [Celcius]')
aft_temp = st.sidebar.number_input('After Temperature [Celcius]')
energy_yield = st.sidebar.number_input('Energy Yield [MWh]')
disch_press = st.sidebar.number_input('Compressor Discharge Pressure [mbar]')
diff_press = st.sidebar.number_input('Air Filter Differential Pressure [mbar]')

CO_prediction = CO_model.predict(np.array([ex_press, in_temp, aft_temp, energy_yield, disch_press]).reshape(1,-1))
NOx_prediction = NOx_model.predict(np.array([amb_temp, diff_press, ex_press, in_temp, aft_temp, energy_yield]).reshape(1,-1))

CO_limit = 31 #mg/m^3
NOx_limit = 52 #mg/m^3

col1, col2 = st.beta_columns(2)
fig1, ax = plt.subplots(figsize=(3, 6))
ax.axhline(y=CO_limit, color='black')
ax.bar(1, CO_prediction, width = 1)
ax.set_ylabel('CO [mg/m^3]')
ax.set_xlim([0, 2])
ax.set_ylim([0, 75])
ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
col1.subheader('Carbon Monoxide')
col1.pyplot(fig1)

fig2, ax = plt.subplots(figsize=(3, 6))
ax.axhline(y=NOx_limit, color='black')
ax.bar(1, NOx_prediction, width = 1)
ax.set_ylabel('NOx [mg/m^3]')
ax.set_xlim([0, 2])
ax.set_ylim([0, 75])
ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
col2.subheader('Nitric Oxides')
col2.pyplot(fig2)

"""* Horizontal constants represent each gas emission limit"""