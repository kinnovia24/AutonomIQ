import streamlit as st
import subprocess
import sys
import openai
import pandas as pd
from io import BytesIO

# Set your OpenAI API key here
openai.api_key = "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"
def generate_srs(software_description):
    """
    Generates a DOORS-style SRS document using OpenAI GPT-4.
    """
    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant that generates "},
                            {"role": "user", "content":  "detailed software requirements with verification method, ASIL level, Rationale and status in a detailed Doors template for " + software_description}
                        ],
                        max_tokens=1000,  # Adjust based on the expected length of the code
                        temperature=0.7,  # Controls creativity (0.0 = deterministic, 1.0 = creative)
                    )
    return response.choices[0].message.content.strip() 

def export_srs_to_excel(srs_document):
    """
    Converts the SRS document into an Excel file.
    """
    # Convert SRS to a DataFrame
    srs_lines = srs_document.split("\n")
    srs_data = {"Requirement ID": [], "Requirement Description": [], "ASIL Level": [], "Traceability": [], "Verification Method": []}
    #"Status": [], "Owner": [],
    
    requirement_id = 1
    for line in srs_lines:
        if line.strip():  # Skip empty lines
            srs_data["Requirement ID"].append(f"REQ-{requirement_id}")
            srs_data["Requirement Description"].append(line.strip())
            srs_data["ASIL Level"].append(line.strip())
            srs_data["Traceability"].append(line.strip())
            srs_data["Verification Method"].append(line.strip())
            
            requirement_id += 1
    
    srs_df = pd.DataFrame(srs_data)

    # Create an Excel file
    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
        srs_df.to_excel(writer, index=False, sheet_name="SRS")
    excel_file.seek(0)

    return excel_file


def run_app():
    """
    Runs the Streamlit app for Software Requirements Generation.
    """
    #st.title("Software Requirements Generation")

    # User input for software description
    st.write("### Requirements Generation - Describe the System or Software")
    st.write("This is the Requirements Analysis page. You can document and analyze software requirements here.")

    software_description = st.text_area("Enter a detailed description of the software:")

    # Button to generate SRS
    if st.button("Generate SRS"):
        if software_description:
            # Generate SRS
            srs_document = generate_srs(software_description)

            # Display the generated SRS
            st.write("### Generated Software Requirements Specification (SRS)")
            st.code(srs_document, language="text")

            # Export SRS to Excel
            excel_file = export_srs_to_excel(srs_document)

            # Download button for the Excel file
            st.download_button(
                label="Download SRS as Excel",
                data=excel_file,
                file_name="Software_Requirements_Specification.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Please enter a software description to generate the SRS.")
