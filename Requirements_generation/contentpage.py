# def extract_full_section_until_next_main(pdf_path, search_title):
#     # Open the PDF file
#     pdf_document = fitz.open(pdf_path)
    
#     # Extract the Table of Contents (TOC)
#     toc = pdf_document.get_toc()

#     all_sections_pdf = fitz.open()

#     levels = {}
#     starpage=None
#     endpage=None
#     new_section_id=None
#     text=search_title
#     section=None

    

#     def increment_section_id(sec_id):
#         if "." in sec_id:
#             parts = sec_id.split(".")
             
#             parts[-1] = str(int(parts[-1]) + 1) 
#             return ".".join(parts)
#         else:
#             return str(int(sec_id) + 1)

#     def not_section_id(sec_id):
#         if "." in sec_id:
#             parts = sec_id.split(".")

#             part=str(int(parts[0])+1)
#             print(part)
#             return part
        
#     # Store TOC data in hierarchical levels.
#     for level, title_with_id, page in toc:
#         parts = title_with_id.split(" ", 1)  
#         if len(parts) == 2:
#             sec_id, title = parts  
#         else:
#             sec_id, title = "", title_with_id  

#         if level not in levels:
#             levels[level] = []

#         levels[level].append((sec_id, title, page)) 

   
#     found = False
#     for level, entries in levels.items():
#         for sec_id, title, page in entries:
#             # print(f"  {sec_id} - {title} (Page {page})")
#             if title == text:
#                 starpage=page
#                 if level == 1 or 2 or 3 or 4:       # filtering based on sec_id to page number
#                     new_section_id=new_section_id = increment_section_id(sec_id)
#                     section=sec_id

#                     print('kk',new_section_id)

#             if str(new_section_id) == sec_id:
#                 endpage=page

#                 found = True
#                 break  
            
#     if not found:
#         print("False - Not Found")
#         new_id=None    
#         new_id=not_section_id(section)

#         for level, entries in levels.items():
#             for sec_id, title, page in entries:
#                 if str(new_id) == sec_id:
#                     endpage=page
#                     found = True
#                     break 
#     print('gg',endpage)            
#     if not found:
#         print("False - Not Found")
#     if starpage - endpage ==0:
#         endpage=starpage+1
        
#     else:
#         endpage=endpage

#     # download pages specified
#     for page_num in range(starpage-1, endpage-1):
#         print(starpage)
#         print(endpage)
#         page = pdf_document.load_page(page_num)
#         all_sections_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
        
#     # Save the combined sections as one PDF
#     output_pdf_path = r"D:\RAG Projects\RAG proj\{search_title}.pdf"
#     all_sections_pdf.save(output_pdf_path)
#     pdf_document.close()

#     print(f"All sections have been extracted and saved to {output_pdf_path}.")
#     return output_pdf_path




# pdf_path = r"D:\RAG Projects\RAG proj\temp.pdf"
# search_title = "NvM_ReadPRAMBlock"
# extract_full_section_until_next_main(pdf_path, search_title)




# import streamlit as st
# import fitz
# import os



# def extract_full_section_until_next_main(pdf_path, search_title, output_dir):
#     # Open the PDF file
#     pdf_document = fitz.open(pdf_path)
    
#     # Extract the Table of Contents (TOC)
#     toc = pdf_document.get_toc()
#     print(toc)

#     all_sections_pdf = fitz.open()

#     levels = {}
#     starpage = None
#     endpage = None
#     new_section_id = None
#     text = search_title
#     section = None

#     def increment_section_id(sec_id):
#         if "." in sec_id:
#             parts = sec_id.split(".")
#             parts[-1] = str(int(parts[-1]) + 1) 
#             return ".".join(parts)
#         else:
#             return str(int(sec_id) + 1)

#     def not_section_id(sec_id):
#         if "." in sec_id:
#             parts = sec_id.split(".")
#             part = str(int(parts[0]) + 1)
#             return part

#     # Store TOC data in hierarchical levels.
#     for level, title_with_id, page in toc:
#         parts = title_with_id.split(" ", 1)  
#         if len(parts) == 2:
#             sec_id, title = parts  
#         else:
#             sec_id, title = "", title_with_id  

#         if level not in levels:
#             levels[level] = []

#         levels[level].append((sec_id, title, page)) 

#     found = False
#     for level, entries in levels.items():
#         for sec_id, title, page in entries:
#             if title == text:
#                 starpage = page
#                 if level in [1, 2, 3, 4]:  # Filtering based on sec_id to page number
#                     new_section_id = increment_section_id(sec_id)
#                     section = sec_id

#             if str(new_section_id) == sec_id:
#                 endpage = page
#                 found = True
#                 break  
            
#     if not found:
#         new_id = not_section_id(section) if section else None    
#         for level, entries in levels.items():
#             for sec_id, title, page in entries:
#                 if str(new_id) == sec_id:
#                     endpage = page
#                     found = True
#                     break 

#     if starpage is None:
#         return None

#     if not found:
#         return None

#     if starpage == endpage:
#         endpage = starpage + 1

#     # Download pages specified
#     for page_num in range(starpage - 1, endpage - 1):
#         page = pdf_document.load_page(page_num)
#         all_sections_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
        
#     # Save the extracted section as a new PDF
#     output_pdf_path = os.path.join(output_dir, f"{search_title}.pdf")
#     all_sections_pdf.save(output_pdf_path)
#     pdf_document.close()

#     return output_pdf_path




# # Streamlit UI
# # Set Page Title
# st.set_page_config(page_title="PDF Section Extractor", layout="wide")

# # Main Title
# st.title("📄 PDF Section Extractor")
# st.sidebar.page_link("RAG_Chat.py", label="RAG Chat 🤖")





# # File uploader
# uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# # Search title input
# search_title = st.text_input("Enter the title to Extract")

# if uploaded_file and search_title:
#     temp_pdf_path = "temp_uploaded.pdf"
    
#     # Save uploaded file
#     with open(temp_pdf_path, "wb") as f:
#         f.write(uploaded_file.read())

#     output_dir = "extracted_sections"
#     os.makedirs(output_dir, exist_ok=True)

#     extracted_pdf_path = extract_full_section_until_next_main(temp_pdf_path, search_title, output_dir)

#     if extracted_pdf_path:
#         with open(extracted_pdf_path, "rb") as f:
#             st.download_button("Download Extracted PDF", f, file_name=f"{search_title}.pdf", mime="application/pdf")
#     else:
#         st.error("Section not found in the PDF.")


# import streamlit as st
# import fitz
# import os
# import pandas as pd

# def extract_toc(pdf_path):
#     """Extract Table of Contents (TOC) from a PDF file"""
#     pdf_document = fitz.open(pdf_path)
#     toc = pdf_document.get_toc()

#     if not toc:
#         return None  # No TOC found

#     toc_data = []
#     for level, title, page in toc:
#         toc_data.append({"Level": level, "Title": title, "Page": page})

#     return pd.DataFrame(toc_data)

# def extract_full_section_until_next_main(pdf_path, search_title, output_dir):
#     """Extract full section based on the TOC title"""
#     pdf_document = fitz.open(pdf_path)
    
#     # Extract Table of Contents (TOC)
#     toc = pdf_document.get_toc()
#     # print(toc)

#     all_sections_pdf = fitz.open()
#     levels = {}
#     starpage = None
#     endpage = None
#     new_section_id = None
#     section = None

#     def increment_section_id(sec_id):
#         if "." in sec_id:
#             parts = sec_id.split(".")
#             parts[-1] = str(int(parts[-1]) + 1) 
#             return ".".join(parts)
#         else:
#             return str(int(sec_id) + 1)

#     def not_section_id(sec_id):
#         if "." in sec_id:
#             parts = sec_id.split(".")
#             part = str(int(parts[0]) + 1)
#             return part

#     # Store TOC data in hierarchical levels
#     for level, title_with_id, page in toc:
#         parts = title_with_id.split(" ", 1)  
#         if len(parts) == 2:
#             sec_id, title = parts  
#         else:
#             sec_id, title = "", title_with_id  

#         if level not in levels:
#             levels[level] = []

#         levels[level].append((sec_id, title, page)) 

#     found = False
#     for level, entries in levels.items():
#         for sec_id, title, page in entries:
#             if title == search_title:
#                 starpage = page
#                 if level in [1, 2, 3, 4]:  # Filtering based on sec_id to page number
#                     new_section_id = increment_section_id(sec_id)
#                     section = sec_id

#             if str(new_section_id) == sec_id:
#                 endpage = page
#                 found = True
#                 break  
            
#     if not found:
#         new_id = not_section_id(section) if section else None    
#         for level, entries in levels.items():
#             for sec_id, title, page in entries:
#                 if str(new_id) == sec_id:
#                     endpage = page
#                     found = True
#                     break 

#     if starpage is None:
#         return None

#     if not found:
#         return None

#     if starpage == endpage:
#         endpage = starpage + 1

#     # Download pages specified
#     for page_num in range(starpage - 1, endpage - 1):
#         page = pdf_document.load_page(page_num)
#         all_sections_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
        
#     # Save the extracted section as a new PDF
#     output_pdf_path = os.path.join(output_dir, f"{search_title}.pdf")
#     all_sections_pdf.save(output_pdf_path)
#     pdf_document.close()

#     return output_pdf_path

# # Streamlit UI
# # Set Page Title
# st.set_page_config(page_title="PDF Section Extractor", layout="wide")

# # Hide Streamlit's default page navigation
# hide_menu_style = """
#     <style>
#     [data-testid="stSidebarNav"] {display: none;}
#     </style>
# """
# st.markdown(hide_menu_style, unsafe_allow_html=True)

# # Main Title
# st.title("📄 PDF Section Extractor")
# st.sidebar.page_link("RAG_Chat.py", label="RAG Chat 🤖")

# # File uploader
# uploaded_file = st.file_uploader("📂 Upload a PDF file", type=["pdf"])

# if uploaded_file:
#     temp_pdf_path = "temp_uploaded.pdf"
    
#     # Save uploaded file
#     with open(temp_pdf_path, "wb") as f:
#         f.write(uploaded_file.read())

#     st.subheader("📑 Extracted Table of Contents")

#     # Extract TOC
#     toc_df = extract_toc(temp_pdf_path)

#     if toc_df is not None:
#         # Display TOC in a table format
#         st.dataframe(toc_df, use_container_width=True)

#         # Provide a CSV Download Button
#         csv = toc_df.to_csv(index=False).encode('utf-8')
#         st.download_button("📥 Download TOC as CSV", csv, "table_of_contents.csv", "text/csv")

#         # # Allow user to select a section from TOC dropdown
#         # section_titles = toc_df["Title"].tolist()
#         # selected_section = st.selectbox("🔍 Select a Section to Extract", section_titles)

#         # if selected_section:
#         #     output_dir = "extracted_sections"
#         #     os.makedirs(output_dir, exist_ok=True)

#         #     extracted_pdf_path = extract_full_section_until_next_main(temp_pdf_path, selected_section, output_dir)

#         #     if extracted_pdf_path:
#         #         with open(extracted_pdf_path, "rb") as f:
#         #             st.download_button("📥 Download Extracted Section", f, file_name=f"{selected_section}.pdf", mime="application/pdf")
#         #     else:
#         #         st.error("⚠️ Section not found in the PDF.")
#     else:
#         st.error("⚠️ No Table of Contents found in this PDF.")

# # Search title input
# search_title = st.text_input("Enter the title to Extract")

# if uploaded_file and search_title:
#     output_dir = "extracted_sections"
#     os.makedirs(output_dir, exist_ok=True)

#     extracted_pdf_path = extract_full_section_until_next_main(temp_pdf_path, search_title, output_dir)

#     if extracted_pdf_path:
#         with open(extracted_pdf_path, "rb") as f:
#             st.download_button("Download Extracted PDF", f, file_name=f"{search_title}.pdf", mime="application/pdf")
#     else:
#         st.error("Section not found in the PDF.")

import streamlit as st
import fitz
import os
import pandas as pd

def extract_toc(pdf_path):
    """Extract list of topics from  specification"""
    pdf_document = fitz.open(pdf_path)
    toc = pdf_document.get_toc()
    if not toc:
        return None  
    toc_data = [{"Level": level, "Title": title, "Page": page} for level, title, page in toc]
    return pd.DataFrame(toc_data)

def extract_full_section_until_next_main(pdf_path, search_title, output_dir):
    """Extract full section based on the TOC title"""
    pdf_document = fitz.open(pdf_path)
    toc = pdf_document.get_toc()
    if not toc:
        return None
    
    levels = {}
    startpage = None
    endpage = None
    new_section_id = None
    section = None

    def increment_section_id(sec_id):
        if "." in sec_id:
            parts = sec_id.split(".")
            parts[-1] = str(int(parts[-1]) + 1) 
            return ".".join(parts)
        else:
            return str(int(sec_id) + 1)

    def not_section_id(sec_id):
        if "." in sec_id:
            parts = sec_id.split(".")
            return str(int(parts[0]) + 1)

    for level, title_with_id, page in toc:
        parts = title_with_id.split(" ", 1)  
        sec_id, title = parts if len(parts) == 2 else ("", title_with_id)
        levels.setdefault(level, []).append((sec_id, title, page))

    found = False
    for level, entries in levels.items():
        for sec_id, title, page in entries:
            if title == search_title:
                startpage = page
                if level in [1, 2, 3, 4]:  
                    new_section_id = increment_section_id(sec_id)
                    section = sec_id

            if str(new_section_id) == sec_id:
                endpage = page
                found = True
                break
            
    if not found:
        new_id = not_section_id(section) if section else None    
        for level, entries in levels.items():
            for sec_id, title, page in entries:
                if str(new_id) == sec_id:
                    endpage = page
                    found = True
                    break 

    if startpage is None:
        return None
    if not found:
        return None
    if startpage == endpage:
        endpage = startpage + 1

    all_sections_pdf = fitz.open()
    for page_num in range(startpage - 1, endpage - 1):
        page = pdf_document.load_page(page_num)
        all_sections_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
        
    output_pdf_path = os.path.join(output_dir, f"{search_title}.pdf")
    all_sections_pdf.save(output_pdf_path)
    pdf_document.close()

    return output_pdf_path

def show_pdf_parser():
    """Displays the PDF parser UI in Streamlit"""
    # st.set_page_config(page_title="PDF Section Extractor", layout="wide")

    hide_menu_style = """
        <style>
        [data-testid="stSidebarNav"] {display: none;}
        </style>
    """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

    st.title("📄 Specification Extractor")

    uploaded_file = st.file_uploader("📂 Upload specification file", type=["pdf"])
    if uploaded_file:
        temp_pdf_path = "temp_uploaded.pdf"
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.read())

        st.subheader("📑 Extracted Table of Contents")
        toc_df = extract_toc(temp_pdf_path)

        if toc_df is not None:
            st.dataframe(toc_df, use_container_width=True)
            csv = toc_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download TOC as CSV", csv, "table_of_contents.csv", "text/csv")
        else:
            st.error("⚠️ No Table of Contents found in this PDF.")

    search_title = st.text_input("Enter the title to Extract")
    if uploaded_file and search_title:
        output_dir = "extracted_sections"
        os.makedirs(output_dir, exist_ok=True)

        extracted_pdf_path = extract_full_section_until_next_main(temp_pdf_path, search_title, output_dir)

        if extracted_pdf_path:
            with open(extracted_pdf_path, "rb") as f:
                st.download_button("Download Extracted PDF", f, file_name=f"{search_title}.pdf", mime="application/pdf")
        else:
            st.error("Section not found in the PDF.")

if __name__ == "__main__":
    show_pdf_parser()
