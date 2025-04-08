import streamlit as st
from PIL import Image
import json

st.set_page_config(page_title="ASPICE Level 2 Interactive Image", layout="wide")


def aspice():# Set page title and layout

    # Title of the app
    st.title("ASPICE Level 2 Interactive Image")

    # Load the ASPICE Level 2 image
    image_path = "aspice_level_2.png"  # Replace with your image path
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        st.error(f"Image not found at path: {image_path}")
        st.stop()

    # Display the image with zoom functionality
    st.write("Use the mouse wheel or pinch gesture to zoom in and out.")
    st.image(image, use_container_width=True)

    # Define ASPICE regions (example bounding boxes: [x1, y1, x2, y2])
    aspice_regions = {
        "SYS.2": {"coords": [100, 150, 200, 250], "description": "System Requirements Analysis"},
        "SWE.1": {"coords": [300, 150, 400, 250], "description": "Software Requirements Analysis"},
        # Add more regions as needed
    }

    # JavaScript to detect mouse clicks and send coordinates to Streamlit
    click_js = """
    <script>
    function getMousePos(event) {
        const rect = document.querySelector('img').getBoundingClientRect();
        const x = event.clientX - rect.left;
        const y = event.clientY - rect.top;
        Streamlit.setComponentValue({x: x, y: y});
    }

    document.querySelector('img').addEventListener('click', getMousePos);
    </script>
    """
    # Display the JavaScript
    st.components.v1.html(click_js, height=0)

    # Get click coordinates from the frontend
    click_data = st.session_state.get("click_data", None)
    if click_data:
        x, y = click_data["x"], click_data["y"]
        st.write(f"Clicked at: ({x}, {y})")

        # Check which region was clicked
        for process, region in aspice_regions.items():
            x1, y1, x2, y2 = region["coords"]
            if x1 <= x <= x2 and y1 <= y <= y2:
                st.write(f"Clicked on {process}: {region['description']}")
                break
        else:
            st.write("Clicked outside defined regions.")
    else:
        st.write("Click on the image to detect the ASPICE process.")

    # Save click data to session state
    if st.button("Clear Click Data"):
        st.session_state.click_data = None
        

def main():
    aspice()
    
if __name__ == "__main__":
    main()



