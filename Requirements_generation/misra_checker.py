import streamlit as st
import openai

# OpenAI API Key Input
openai.api_key = "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"
# Function to check MISRA-C compliance using OpenAI
def check_misra_compliance(code):
    response = openai.chat.completions.create(
        model="gpt-4",  # Use GPT-4 or GPT-3.5
        messages=[
            {"role": "system", "content": "You are a helpful assistant that checks C code for compliance with MISRA-C rules. Analyze the code line by line and provide feedback on any violations."},
            {"role": "user", "content": f"Check the following C code for MISRA-C compliance:\n\n{code}\n\nProvide feedback for each line, indicating whether it complies with MISRA-C rules or violates any rules."},
        ],
        max_tokens=1000,  # Adjust based on the expected length of the code
        temperature=0.7,  # Controls creativity (0.0 = deterministic, 1.0 = creative)
    )
    return response.choices[0].message.content.strip() 

def check_misra():
    
    # Input: Upload or paste C code
    code_input = st.text_area("Paste your C code here:", height=300)

    # Check button
    if st.button("Check MISRA-C Compliance"):
        if not code_input:
            st.warning("Please paste or upload some C code to check.")
        else:
            with st.spinner("Checking MISRA-C compliance..."):
                try:
                    result = check_misra_compliance(code_input)
                    st.write("### MISRA-C Compliance Results:")
                    st.write(result)
                except Exception as e:
                    st.error(f"An error occurred: {e}")