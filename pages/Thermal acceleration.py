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
st.write('Enter the activation energy, ambient temperature, and reference temperature below to calculate the Acceleration Factor:')

activation_energy = st.sidebar.slider('Activation Energy (eV)', 0.1, 1.0, 0.7, 0.1)
app_amb_T = st.sidebar.slider('Ambient Temperature (°C)', -40, 200, 25, 5)
stress_amb_T = st.sidebar.slider('Stress ambient Temperature (°C)', -40, 200, 25, 5)

arr_factor = arrhenius_acceleration_model(app_amb_T, stress_amb_T, activation_energy)
st.write("Acceleration Factor: " + str(arr_factor))


#df = pd.DataFrame({
#    'Temperature (°C)': np.arange(-40, 201, 5),
#    'Activation Energy(eV)'=[0.4,0.7],
#    'Acceleration Factor': arrhenius_acceleration_model(app_amb_T, np.arange(-40, 201, 5) ,[0.4,0.7])
#})


#app_temp = app_amb_T
stress_amb_T = [x for x in range(-40, 260, 10)]
activation_energy = [0.4, 0.7, 0.8, 1]
comb = np.array(np.meshgrid(stress_amb_T, activation_energy)).T.reshape(-1,2)

df = pd.DataFrame(data=comb, columns=["Stress ambient Temperature (°C)", "Activation energy(eV)"])
df['Application Ambient temp(°C)']= app_amb_T
df["Acceleration Factor"] = arrhenius_acceleration_model(df["Application Ambient temp(°C)"], df["Stress ambient Temperature (°C)"], df["Activation energy(eV)"], print_result=False)


#print(df)
#st.write(df)

chart = alt.Chart(df).mark_line().encode(
    x='Stress ambient Temperature (°C):Q',
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


st.title('Typical Activation energy')

st.markdown(
    """
Failure mechanism | Activation Energy (eV) | Test 
--|--|--
oxide defects | 0.3~0.5 | HTOL 
Silicon defects | 0.3~0.5 | HTOL 
Corrosion | 0.45 | HAST |
Assembly defects | 0.5~0.7 | TC |
Electronmigration Al line | 0.6 | HAST |
Electronmigration Contact/Via | 0.9 | HAST |
Mask defects, photoresist defect | 0.7 | HTOL |
Contamination | 1 | HTOL |
Charge injection | 1.3 | HTOL |	
""")