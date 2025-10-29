import streamlit as st
from datetime import datetime

# Initialize
if 'balance' not in st.session_state:
    st.session_state.balance = {'IQD': 0.0, 'USD': 0.0}
if 'rate' not in st.session_state:
    st.session_state.rate = 1310.0
if 'logs' not in st.session_state:
    st.session_state.logs = []

def process(exp_iqd, exp_usd, act_iqd, act_usd, is_pay=False):
    total_exp = exp_iqd + exp_usd * st.session_state.rate
    total_act = act_iqd + act_usd * st.session_state.rate
    diff = total_act - total_exp
    if abs(diff) < 1:
        if is_pay:
            st.session_state.balance['IQD'] -= act_iqd
            st.session_state.balance['USD'] -= act_usd
        else:
            st.session_state.balance['IQD'] += act_iqd
            st.session_state.balance['USD'] += act_usd
        st.session_state.logs.append(f"{datetime.now().strftime('%H:%M')} | Success")
        return "Success!"
    else:
        st.session_state.logs.append(f"{datetime.now().strftime('%H:%M')} | Diff: {diff:,.0f} IQD")
        return f"Diff: {diff:,.0f} IQD"

st.title("Cash Register")

st.session_state.rate = st.number_input("Rate (IQD/USD)", value=st.session_state.rate)

tab1, tab2, tab3 = st.tabs(["Receive", "Pay", "Report"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        exp_iqd = st.number_input("Exp IQD", 0.0, key="r1")
        exp_usd = st.number_input("Exp USD", 0.0, key="r2")
    with col2:
        act_iqd = st.number_input("Act IQD", 0.0, key="r3")
        act_usd = st.number_input("Act USD", 0.0, key="r4")
    if st.button("Process Receive"):
        st.success(process(exp_iqd, exp_usd, act_iqd, act_usd))

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        exp_iqd = st.number_input("Pay IQD", 0.0, key="p1")
        exp_usd = st.number_input("Pay USD", 0.0, key="p2")
    with col2:
        act_iqd = st.number_input("Give IQD", 0.0, key="p3")
        act_usd = st.number_input("Give USD", 0.0, key="p4")
    if st.button("Process Pay"):
        if exp_iqd > st.session_state.balance['IQD'] or exp_usd > st.session_state.balance['USD']:
            st.error("Not enough balance!")
        else:
            st.success(process(exp_iqd, exp_usd, act_iqd, act_usd, is_pay=True))

with tab3:
    for log in st.session_state.logs[-10:]:
        st.write(log)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("IQD", f"{st.session_state.balance['IQD']:,.0f}")
    with col2:
        st.metric("USD", f"{st.session_state.balance['USD']:.2f}")
