import streamlit as st
import subprocess
import sys
import openai
from groq import Groq
import pandas as pd
from io import BytesIO

from Requirements_generation.srs_app import run_app
from Requirements_generation.aspice_app import aspice
from Requirements_generation.misra_checker import check_misra
from Requirements_generation.system_design import system_arch
from Project_Intelligence.ai_project import project_ai

# Set your OpenAI API key here
client = Groq(api_key = "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")
# client = Groq(api_key = "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")

VALID_USERNAME = "admin"
VALID_PASSWORD = "admin"    

# Define the V-cycle steps
v_cycle_steps = [
        "SAFe Agile PM",
        "Requirements Generation",
        "System Design",
        "Coding",
        "MISRA-C Unit Testing",
        "Integration Testing",
        "System Testing",
        "Acceptance Testing",
        "ASPICE Assesor",
        "Specification Extractor",
        "Specification Intelligence"
    ]

# Initialize session state for login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Function to check login credentials
def check_login(username, password):
    # Replace with your actual authentication logic
    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return True
    return False

# Login function
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if check_login(username, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()  # Refresh the app to hide the login form
        else:
            st.error("Invalid username or password")

# Main application function
def main_app():
    logout_button = st.button("Logout")
    #st.title("Welcome to your AI Assistant!")
    #st.write("---")
    
    # Sidebar navigation for V-cycle steps
    st.sidebar.title("Development activities")
    selected_step = st.sidebar.radio("Go to", v_cycle_steps)
    main_application(selected_step)

    if logout_button:
        st.session_state.logged_in = False
        st.rerun()  # Refresh the app to show the login form again



def main_application(selected_step):

    # Main content based on the selected step
    #st.title(f"Software Engineering Copilot - {selected_step}")

    if selected_step == "SAFe Agile PM":
        project_ai()
        
    elif selected_step == "Requirements Generation":
        #st.write("### Requirements Analysis")
        run_app()

    elif selected_step == "System Design":
        st.write("### System Design")
        # st.write("This is the System Design page. You can create system architecture and design diagrams here.")
        system_arch()

    elif selected_step == "Coding":
        st.write("### Coding")
        st.write("This is the Coding page. You can generate code based on requirements and test it here.")

        # Input for requirements
        requirements = st.text_area("Enter your software requirements:")

        if st.button("Generate Code"):
            if requirements:
                # Call OpenAI GPT-4 to generate code
                with st.spinner("Generating Code..."):
                    try:
                        response = client.chat.completions.create(
                            model="deepseek-r1-distill-llama-70b",
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant that generates code in any programming language."},
                                {"role": "user", "content": requirements}
                            ],
                            max_tokens=128000,  # Adjust based on the expected length of the code
                            temperature=0.7,  # Controls creativity (0.0 = deterministic, 1.0 = creative)
                        )
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            
                generated_code = response.choices[0].message.content.strip() 
                st.code(generated_code, language="python")
                # Save generated code for unit testing
                st.session_state.generated_code = generated_code
            else:
                st.warning("Please enter requirements to generate code.")

        if "generated_code" in st.session_state:
            st.write("### Unit Testing")
            if st.button("Generate Unit Test Case"):
                # Generate unit test case using GPT-4
                with st.spinner("Generating Test Code..."):
                    try:
                        response = client.chat.completions.create(
                            model="deepseek-r1-distill-llama-70b",
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant that generates Test code in any programming language."},
                                {"role": "user", "content": st.session_state.generated_code}
                            ],
                            max_tokens=1000,  # Adjust based on the expected length of the code
                            temperature=0.7,  # Controls creativity (0.0 = deterministic, 1.0 = creative)
                        )
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
            
                unit_test_case = response.choices[0].message.content.strip() 
                st.code(unit_test_case, language="python")

                # Save unit test case for execution
                st.session_state.unit_test_case = unit_test_case

            if "unit_test_case" in st.session_state:
                st.write("### Run Unit Test Case")
                # Input for test parameters
                test_parameters = st.text_input("Enter parameters to pass to the unit test case (comma-separated):")
                expected_output = st.text_input("Enter the expected output:")

                if st.button("Run Test"):
                    if test_parameters and expected_output:
                        # Prepare the test script
                        test_script = f"""
    {st.session_state.generated_code}

    {st.session_state.unit_test_case}

    if __name__ == "__main__":
        import sys
        params = [{test_parameters}]
        result = test_function(*params)  # Assuming the test function is named 'test_function'
        print(result)
                        """
                        # Save the test script to a temporary file
                        with open("temp_test_script.py", "w") as f:
                            f.write(test_script)

                        # Execute the test script
                        try:
                            result = subprocess.run(
                                [sys.executable, "temp_test_script.py"],
                                capture_output=True, text=True
                            )
                            actual_output = result.stdout.strip()
                            st.write(f"Actual Output: {actual_output}")
                            st.write(f"Expected Output: {expected_output}")

                            # Compare actual and expected output
                            if actual_output == expected_output:
                                st.success("TEST PASSED! ✅")
                            else:
                                st.error("TEST FAILED! ❌")
                        except Exception as e:
                            st.error(f"Error running the test: {e}")
                    else:
                        st.warning("Please provide both test parameters and expected output.")

    elif selected_step == "MISRA-C Unit Testing":
        st.title("MISRA-C Unit testing")
        st.write("Upload or paste your C code to check it against MISRA-C rules")
        check_misra()

    elif selected_step == "Integration Testing":
        st.write("### Integration Testing")
        st.write("This is the Integration Testing page. You can test the integration of different modules here.")

    elif selected_step == "System Testing":
        st.write("### System Testing")
        st.write("This is the System Testing page. You can test the entire system here.")

    elif selected_step == "Acceptance Testing":
        st.write("### Acceptance Testing")
        st.write("This is the Acceptance Testing page. You can validate the system against user requirements here.")
    
    elif selected_step == "ASPICE Assesor":
        aspice()

    elif selected_step == "Specification Extractor":
        from Requirements_generation import contentpage
        contentpage.show_pdf_parser()

    elif selected_step == "Specification Intelligence":
        from Requirements_generation import RAG_Chat  
        RAG_Chat.show_rag_chat() 


def main():
    
    if not st.session_state.logged_in:
        login()  # Show login form if not logged in
    else:
        main_app()  # Show main app content if logged in
    #Kinnovia Logo
    st.logo(
        image="Horizontal_black_orange.png",
        link="https://www.kinnovia.com",
        icon_image=None,
        )
    
    #######
    # Footer
    st.sidebar.write("---")
    st.sidebar.write("Kinnovia.com All Rights Reserved.")
    
    
if __name__ == "__main__":
    main()
