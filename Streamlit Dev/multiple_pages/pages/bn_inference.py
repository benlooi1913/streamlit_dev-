import joblib
import streamlit as st
from pgmpy.inference import VariableElimination

# Load the Bayesian Network model using joblib
model = joblib.load('Bayesian_Network_Inference.joblib')

# Create the VariableElimination object for inference
infer_exact = VariableElimination(model)

st.title("Bayesian Network Inference")
st.write("Bayesian network inference is an analytically computation the conditional probability distribution over the variables of interest - it takes into account of model dependencies network which nodes and edges are computed in the algorithm ")
st.write("Example = P(status|evidence ={['FoamHeight':'low','inkfill_volume':'low']})")
st.write("Inference steps derived by probabilistic formula, while the target_variable = posterior given the evidence = variable':'states_condition")

st.image('Nodes&Edges.png')

# Define the variables for the query using Streamlit multiselect
variables = st.multiselect("Select Evidences", model.nodes)

# Define the evidence for the query using Streamlit multiselect
evidence = {}
for variable in variables:
    cpd = model.get_cpds(variable)
    states = cpd.state_names[variable]
    selected_states = st.multiselect(f"Select Evidence for {variable}", states)
    if selected_states:
        evidence[variable] = selected_states[0]  # Assuming only one state is selected

# Separate the target variable
target_variable = 'status'

# Perform the query
joint_distribution = infer_exact.query(variables=[target_variable], evidence=evidence)

# Display the joint distribution
st.write("Joint Distribution:")
st.write(joint_distribution)
