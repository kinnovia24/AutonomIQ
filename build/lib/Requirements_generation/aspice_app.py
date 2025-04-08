import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from streamlit_image_coordinates import streamlit_image_coordinates

# Set page title and layout
st.set_page_config(page_title="ASPICE Level 2 Interactive Image", layout="wide")

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
        "SWE.1": {"x_range": (158, 286), "y_range": (248, 283), "description": "Software Requirements Analysis", "Assesment": ''' Process group: Software Engineering
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