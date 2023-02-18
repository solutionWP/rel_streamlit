import streamlit as st
import numpy as np
import pandas as pd
import altair as alt


def arrhenius_acceleration_model(app_amb_T, stress_amb_T, activation_energy, print_result=False):
    boltzmann_const = 8.62e-5
    T_abs_0 = 273.16

    AF = np.exp((activation_energy / boltzmann_const)
                * (1 / (app_amb_T + T_abs_0) - 1 / (stress_amb_T + T_abs_0)))
    if (print_result):
        print("")
        print("k: Boltzmann Constant: " + str(boltzmann_const))
        print("Temp Abs 0(°K): " + str(T_abs_0))
        print("Acceleration Factor: " + str(round(AF, 3)))
    return AF

st.title('Arrhenius Law Application')
st.write('Enter the activation energy, ambient temperature, and reference temperature below to calculate the Arrhenius factor:')

activation_energy = st.slider('Activation Energy (eV)', 0.1, 1.0, 0.7, 0.1)
app_amb_T = st.slider('Ambient Temperature (°C)', -40, 200, 25, 5)
stress_amb_T = st.slider('Stress ambiant Temperature (°C)', -40, 200, 25, 5)

arr_factor = arrhenius_acceleration_model(app_amb_T, stress_amb_T, activation_energy)
st.write(arr_factor)


#df = pd.DataFrame({
#    'Temperature (°C)': np.arange(-40, 201, 5),
#    'Activation Energy(eV)'=[0.4,0.7],
#    'Acceleration Factor': arrhenius_acceleration_model(app_amb_T, np.arange(-40, 201, 5) ,[0.4,0.7])
#})


amp_ref_temp = 55
amb_T = [x for x in range(-40, 260, 10)]
activation_energy = [0.4, 0.7, 0.8, 1]
comb = np.array(np.meshgrid(amb_T, activation_energy)).T.reshape(-1,2)

df = pd.DataFrame(data=comb,columns=["Temperature(°C)", "Activation energy(eV)"])
df['ref Ambient temp(°C)']= 55
df["Acceleration Factor"] = arrhenius_acceleration_model(df["ref Ambient temp(°C)"], df["Temperature(°C)"], df["Activation energy(eV)"], print_result=False)


#print(df)
#st.write(df)

chart = alt.Chart(df).mark_line().encode(
    x='Temperature(°C):Q',
    y=alt.Y('Acceleration Factor:Q',scale=alt.Scale(domain=(0,1000),zero=True)),
    color='Activation energy(eV)'+':N'
).properties(
    width=600,
    height=400
).configure_axis(
    labelFontSize=14,
    titleFontSize=14
).configure_title(
    fontSize=18,
    anchor='middle'
).interactive()

st.altair_chart(chart, use_container_width=True)