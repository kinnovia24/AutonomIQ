import streamlit as st
import openai
import matplotlib.pyplot as plt
import graphviz

openai.api_key = "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"

#def draw_graph(components):
#    G = nx.DiGraph()
#    edges = components.split(" -> ")
#    for i in range(len(edges) - 1):
#        G.add_edge(edges[i], edges[i + 1])
#    plt.figure(figsize=(8, 6))
#    pos = nx.spring_layout(G)
#    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold", arrows=True)
#    st.pyplot(plt)

# Function to create a Graphviz diagram
def draw_graph(components):
    edges = components.split(" -> ")
    graphviz_code = "digraph G {\n"
    for i in range(len(edges) - 1):
        graphviz_code += f'    "{edges[i]}" -> "{edges[i + 1]}";\n'
    graphviz_code += "}"
    return graphviz_code

# Function to generate system architecture using OpenAI
def generate_architecture(description, architecture_type):
    response = openai.ChatCompletion.create(
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
                    components = result.split("\n")[0]  # Assume the first line contains the component relationships
                    graphviz_code = draw_graph(components)
                    st.graphviz_chart(graphviz_code)
                    
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
                    components = result.split("\n")[0]  # Assume the first line contains the component relationships
                    graphviz_code = draw_graph(components)
                    st.graphviz_chart(graphviz_code)
                    
                    # List components for the user
                    st.write("### Components to Consider:")
                    st.write(result.split("\n")[1:])  # Assume the rest of the lines list components
                except Exception as e:
                    st.error(f"An error occurred: {e}")