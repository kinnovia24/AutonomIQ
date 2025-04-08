import streamlit as st
import openai
import matplotlib.pyplot as plt
import graphviz

openai.api_key  = "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"

# Function to create a Graphviz diagram
def draw_graph(components):
     # Create a Graphviz Digraph object
    graph = graphviz.Digraph()
    # Split the components into edges
    edges = components.split(" -> ")
    # Add nodes and edges to the graph
    for i in range(len(edges) - 1):
        graph.edge(edges[i], edges[i + 1])
    return graph

def arch_components(system_description):
    prompt = f"""
    Describe the software architecture for a system with the following description:
    {system_description}

    Provide the architecture as a list of components and their relationships in the following format:
    - Component A -> Component B
    - Component B -> Component C
    """
    response = openai.chat.completions.create(
        model="gpt-4",  # Use GPT-4
        messages=[
            {"role": "system", "content": "You are a software architect. Describe the architecture of the system."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=1000,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

def parse_architecture_to_graph(architecture_text):
    graph = graphviz.Digraph()
    lines = architecture_text.split("\n")
    for line in lines:
        if "->" in line:
            source, target = line.split("->")
            source = source.strip().replace("-", "").strip()
            target = target.strip()
            graph.edge(source, target)
    return graph

# Function to generate system architecture using OpenAI
def generate_architecture(description, architecture_type):
    response = openai.chat.completions.create(
    model="gpt-4",  # Use GPT-4 or GPT-3.5
    messages=[
            {"role": "system", "content": f"You are a helpful assistant that designs {architecture_type} system architecture based on a description. Provide a list of components and their relationships in the format: 'Component1 -> Component2 -> Component3'. Also, list all components for the user to consider."},
            {"role": "user", "content": f"Design a {architecture_type} system architecture for the following system: {description}"},
        ],
        max_tokens=1000,  # Adjust based on the expected length of the code
        temperature=0.7,  # Controls creativity (0.0 = deterministic, 1.0 = creative)
    )
    return response.choices[0].message.content.strip()


def system_arch():
    
        # Title of the app
    st.title("System Architecture Designer")
    # Description
    st.write("Enter a description of your system, and the app will generate functional and physical architecture graphs along with a list of components.")
    # Input: System description
    system_description = st.text_area("Describe your system:", height=150)

    # Buttons to generate graphs
    col1, col2 = st.columns(2)
    with col1:
        functional_button = st.button("Generate Functional System Architecture")
    with col2:
        physical_button = st.button("Generate Physical System Architecture")
    
    # Generate Functional System Architecture
    if functional_button:
        if not system_description:
            st.warning("Please describe your system.")
        else:
            with st.spinner("Generating Functional System Architecture..."):
                try:
                    result = generate_architecture(system_description, "functional")
                    st.write("### Functional System Architecture:")
                    st.write(result)
                    
                    # Extract components and draw graph
                    # old draw_chart()
                    ######
                    architecture_text = arch_components(system_description)
                    # Parse architecture into a graph
                    graph = parse_architecture_to_graph(architecture_text)
                    # Display the graph
                    st.write("Visualized Architecture:")
                    st.graphviz_chart(graph)
                    #######
                    
                    # List components for the user
                    st.write("### Components to Consider:")
                    st.write(result.split("\n")[1:])  # Assume the rest of the lines list components
                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # Generate Physical System Architecture
    if physical_button:
        if not system_description:
            st.warning("Please describe your system.")
        else:
            with st.spinner("Generating Physical System Architecture..."):
                try:
                    result = generate_architecture(system_description, "physical")
                    st.write("### Physical System Architecture:")
                    st.write(result)
                    
                    # Extract components and draw graph
                    ######
                    architecture_text = arch_components(system_description)
                    # Parse architecture into a graph
                    graph = parse_architecture_to_graph(architecture_text)
                    # Display the graph
                    st.write("Visualized Architecture:")
                    st.graphviz_chart(graph)
                    ####### 
                    
                    # List components for the user
                    st.write("### Components to Consider:")
                    st.write(result.split("\n")[1:])  # Assume the rest of the lines list components
                except Exception as e:
                    st.error(f"An error occurred: {e}")