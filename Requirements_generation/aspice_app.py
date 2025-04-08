import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from streamlit_image_coordinates import streamlit_image_coordinates

# Set page title and layout
st.set_page_config(page_title="ASPICE Level 2 Interactive Image", layout="wide")

# Define ASPICE System Engineering and Software Engineering Process Groups and their tasks for Level 2
aspice_processes = {
    "System Engineering": {
        "SYS.1 - Requirements Elicitation and Analysis": [
            "Elicit and document system requirements.",
            "Analyze requirements for consistency and completeness.",
            "Validate requirements with stakeholders.",
            "Establish traceability to stakeholder needs.",
            "Manage changes to requirements.",
        ],
        "SYS.2 - System Requirements Analysis": [
            "Refine system requirements.",
            "Analyze requirements for feasibility and testability.",
            "Establish traceability to stakeholder requirements.",
            "Verify system requirements.",
            "Manage changes to system requirements.",
        ],
        "SYS.3 - System Architectural Design": [
            "Define system architecture.",
            "Document architectural design decisions.",
            "Ensure consistency with system requirements.",
            "Establish traceability to system requirements.",
            "Verify architectural design.",
            "Manage changes to the architecture.",
        ],
        "SYS.4 - System Integration and Integration Testing": [
            "Integrate system components.",
            "Develop integration test cases.",
            "Execute integration tests.",
            "Document integration test results.",
            "Verify integration test coverage.",
            "Manage changes to integration tests.",
        ],
        "SYS.5 - System Qualification Testing": [
            "Develop qualification test cases.",
            "Execute qualification tests.",
            "Document qualification test results.",
            "Verify qualification test coverage.",
            "Manage changes to qualification tests.",
        ],
    },
    "Software Engineering": {
        "SWE.1 - Software Requirements Analysis": [
            "Elicit and document software requirements.",
            "Analyze requirements for consistency and completeness.",
            "Establish traceability to system requirements.",
            "Validate requirements with stakeholders.",
            "Verify requirements for testability.",
            "Manage changes to requirements.",
        ],
        "SWE.2 - Software Architectural Design": [
            "Define software architecture.",
            "Document architectural design decisions.",
            "Ensure consistency with system architecture.",
            "Establish traceability to software requirements.",
            "Verify architectural design.",
            "Manage changes to the architecture.",
        ],
        "SWE.3 - Software Detailed Design and Unit Construction": [
            "Develop detailed design for software components.",
            "Implement software units according to design.",
            "Establish traceability to architectural design.",
            "Verify detailed design and units.",
            "Manage changes to the design and units.",
        ],
        "SWE.4 - Software Unit Verification": [
            "Develop unit test cases.",
            "Execute unit tests.",
            "Document unit test results.",
            "Verify unit test coverage.",
            "Manage changes to unit tests.",
        ],
        "SWE.5 - Software Integration and Integration Testing": [
            "Integrate software components.",
            "Develop integration test cases.",
            "Execute integration tests.",
            "Document integration test results.",
            "Verify integration test coverage.",
            "Manage changes to integration tests.",
        ],
        "SWE.6 - Software Qualification Testing": [
            "Develop qualification test cases.",
            "Execute qualification tests.",
            "Document qualification test results.",
            "Verify qualification test coverage.",
            "Manage changes to qualification tests.",
        ],
    },
}

def aspice_acessor():    
    
    # Initialize session state for visibility
    if "visibility" not in st.session_state:
        st.session_state.visibility = {
        category: {process: False for process in processes.keys()}
        for category, processes in aspice_processes.items()
        }

    st.write("Select a process group to see the tasks required to achieve ASPICE Level 2.")
    # Display buttons for each process group
    for category, processes in aspice_processes.items():
        st.write(f"### {category} Process Groups")
        for process in processes.keys():
            # Show/Hide button
            if st.button(f"{process}"):
                st.session_state.visibility[category][process] = not st.session_state.visibility[category][process]

            # Display tasks if the process is visible
            if st.session_state.visibility[category][process]:
                st.write(f"#### Tasks for {process}")
                tasks = processes[process]
                task_status = {task: False for task in tasks}

                # Create checkboxes for each task
                for task in tasks:
                    task_status[task] = st.checkbox(task, value=task_status[task])

                # Check if all tasks are completed
                if all(task_status.values()):
                    st.success("Congratulations! You have achieved ASPICE Level 2 for this process.")
                else:
                    st.warning("Complete all tasks to achieve ASPICE Level 2.")



def aspice():
        # Title of the app
    st.title("ASPICE Level 2 Assesment report")
    # Description
    st.write("Click on the ASPICE Level 2 processes to learn more about requirement")

    # Load the ASPICE Level 2 image
    image_path = "aspice_3.png"  # Replace with the path to your ASPICE Level 2 image

    # Display the image and get click coordinates
    coordinates = streamlit_image_coordinates(image_path)

    # Define process areas and their descriptions
    process_areas = {
        "MAN.3": {"x_range": (718, 843), "y_range": (117, 153), "description": "Project Management", "Assesment": " "},
        "SUP.1": {"x_range": (157, 286), "y_range": (511, 550), "description": "Quality Assurance", "Assesment": ""},
        "SUP.8": {"x_range": (157, 283), "y_range": (556, 590), "description": "Configuration Management", "Assesment": ""},
        "SWE.1": {"x_range": (158, 286), "y_range": (248, 283), "description": "Software Requirements Analysis", "Assesment": ''' Process group: Software Engineering,  
                    The Software Requirements Analysis process in Automotive SPICE® (also known as SWE.1) helps your organization transform the software related aspects of the system requirements into a set of software requirements.
                    There are already system or customer requirements covering a project, but documenting software requirements is also essential. Projects must be delivered on time, within budget, and in the quality required by the customer.
                    Failure to document software requirements may lead to overlooked functionality or misinterpretation of customer expectations. Overlooking both essential software functionality and nonfunctional requirements (such as performance, reusability and maintenance) can lead to increased effort, added costs and delays along with false starts or even additional development cycles.
                    The SWE.1 process has links upstream to System Requirements Analysis (SYS.2) and System Architectural Design (SYS.3), and downstream to Software Architecture (SWE.2) and Software Qualification Test (SWE.6). Other processes with strong dependencies are Project Management (MAN.3) and Configuration Management (SUP.8), due to release management. Defect Management (SUP.9) and Change Request Management (SUP.10) also have dependencies because defects identified in tests must be addressed and bug fixes and change requests must be addressed, for example, in regression tests.
                    The following are the most important aspects of Software Requirements Analysis in Automotive SPICE®.'''},
        "SWE.2": {"x_range": (300, 400), "y_range": (200, 300), "description": "Software Architectural Design", "Assesment": ""},
        "SWE.3": {"x_range": (500, 600), "y_range": (200, 300), "description": "Software Detailed Design and Unit Construction", "Assesment": ""},
        "SWE.4": {"x_range": (100, 200), "y_range": (350, 450), "description": "Software Unit Testing", "Assesment": ""},
        "SWE.5": {"x_range": (300, 400), "y_range": (350, 450), "description": "Software Integration Testing", "Assesment": ""},
        "SWE.6": {"x_range": (500, 600), "y_range": (350, 450), "description": "Software Qualification Testing", "Assesment": ""},
    }

    # Check if the user clicked on a process area
    if coordinates:
        x, y = coordinates["x"], coordinates["y"]
        for process, area in process_areas.items():
            #st.write("X is: " ,x, "Y is: ", y)
            if area["x_range"][0] <= x <= area["x_range"][1] and area["y_range"][0] <= y <= area["y_range"][1]:
                st.success(f"You clicked on {process}: {area['description']} {area['Assesment']}")
                break
        else:
            st.warning("You clicked outside a process area.")
            
    aspice_acessor()