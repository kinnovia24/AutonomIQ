import streamlit as st
import openai
import json
import pandas as pd
import networkx as nx
import plotly.express as px
from datetime import datetime
from io import BytesIO

# Initialize OpenAI (replace with your API key)
openai.api_key = "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"
def project_ai():

    # Fixed domain-specific epic templates
    DOMAINS = [
        "Software Architecture", "System Design", "Mechanical Design",
        "System Integration", "Safety Compliance", "Security Protocols"
    ]

    # Initialize session state
    if 'project' not in st.session_state:
        st.session_state.project = {
            'epics': [],
            'tasks': [],
            'dependencies': {},
            'critical_path': []
        }

    def generate_domain_epics(initiative):
        prompt = f"""Break this business initiative into domain-specific epics:
        {initiative}
        
        Required domains: {", ".join(DOMAINS)}
        
        For each epic provide:
        - 5-7 implementation tasks with durations
        - Key dependencies
        - Success metrics
        - Risk factors
        
        Format as JSON with: 
        {{
            "epics": [
                {{
                    "domain": "domain name",
                    "objective": "clear objective",
                    "tasks": [
                        {{
                            "name": "task name",
                            "duration": days,
                            "dependencies": [],
                            "owner_team": "team name",
                            "status": "Not Started"
                        }}
                    ],
                    "metrics": ["metric1", "metric2"],
                    "risks": [
                        {{
                            "description": "risk description",
                            "severity": "High/Medium/Low"
                        }}
                    ]
                }}
            ]
        }}"""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=7000,
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            st.error(f"AI Error: {str(e)}")
            return None

    def calculate_critical_path():
        G = nx.DiGraph()
        tasks = [task for epic in st.session_state.project['epics'] for task in epic['tasks']]
        
        # Add nodes with duration attribute
        for task in tasks:
            G.add_node(task['name'], duration=task['duration'])
        
        # Add edges based on dependencies
        for task in tasks:
            for dep in task.get('dependencies', []):
                if dep in G.nodes:
                    G.add_edge(dep, task['name'])
        
        if nx.is_directed_acyclic_graph(G):
            critical_path = nx.dag_longest_path(G, weight='duration')
            return critical_path
        return []

    def export_to_excel():
        # Create a DataFrame for Epics and Tasks
        epics_data = []
        for epic in st.session_state.project['epics']:
            for task in epic['tasks']:
                epics_data.append({
                    "Epic": epic['domain'],
                    "Objective": epic['objective'],
                    "Task": task['name'],
                    "Duration (days)": task['duration'],
                    "Dependencies": ", ".join(task.get('dependencies', [])),
                    "Owner": task['owner_team'],
                    "Status": task['status'],
                    "Metrics": ", ".join(epic['metrics']),
                    "Risks": ", ".join([risk['description'] for risk in epic['risks']])
                })
        
        df_epics_tasks = pd.DataFrame(epics_data)
        
        # Save to Excel
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_epics_tasks.to_excel(writer, sheet_name="Epics and Tasks", index=False)
        
        output.seek(0)
        return output

    def draw_gantt_chart(view_type):
        if view_type == "Detailed Project":
            # Prepare data for the Detailed Project Gantt chart
            gantt_data = []
            start_date = datetime.now().date()
            
            for epic in st.session_state.project['epics']:
                current_date = start_date
                for task in epic['tasks']:
                    end_date = current_date + pd.DateOffset(days=task['duration'])
                    gantt_data.append({
                        "Task": task['name'],
                        "Start": current_date,
                        "Finish": end_date,
                        "Duration": task['duration'],
                        "Epic": epic['domain'],
                        "Owner": task['owner_team'],  # Add Owner to the DataFrame
                        "Status": task['status'],     # Add Status to the DataFrame
                        "Dependencies": ", ".join(task.get('dependencies', []))  # Add Dependencies
                    })
                    current_date = end_date
            
            title = "Detailed Project Plan"
        
        elif view_type == "Critical Path":
            # Prepare data for the Critical Path Gantt chart
            critical_path = calculate_critical_path()
            if not critical_path:
                st.warning("Could not determine critical path - check task dependencies.")
                return
            
            tasks = {task['name']: task for epic in st.session_state.project['epics'] for task in epic['tasks']}
            start_date = datetime.now().date()
            
            gantt_data = []
            current_date = start_date
            for task_name in critical_path:
                task = tasks[task_name]
                end_date = current_date + pd.DateOffset(days=task['duration'])
                gantt_data.append({
                    "Task": task_name,
                    "Start": current_date,
                    "Finish": end_date,
                    "Duration": task['duration'],
                    "Epic": next(epic['domain'] for epic in st.session_state.project['epics'] 
                                if task in epic['tasks']),
                    "Owner": task['owner_team'],  # Add Owner to the DataFrame
                    "Status": task['status'],     # Add Status to the DataFrame
                    "Dependencies": ", ".join(task.get('dependencies', []))  # Add Dependencies
                })
                current_date = end_date
            
            title = "Project Critical Path"
        
        # Create Gantt chart
        fig = px.timeline(
            gantt_data,
            x_start="Start",
            x_end="Finish",
            y="Task",
            color="Epic",
            title=title,
            labels={"Task": "Task Name", "Start": "Start Date", "Finish": "End Date", "Epic": "Epic Domain"},
            hover_data=["Owner", "Status", "Dependencies"]  # Ensure these columns exist in gantt_data
        )
        
        # Update layout
        fig.update_yaxes(categoryorder="total ascending")
        fig.update_layout(
            xaxis_title="Timeline",
            yaxis_title="Tasks",
            showlegend=True,
            legend_title="Epics"
        )
        
        return fig, gantt_data

    # Streamlit UI
    st.title("Cross-Domain Project Planner")
    st.subheader("Business Initiative to Technical Implementation")

    # Business Input Section
    with st.expander("🚀 Enter Business Initiative", expanded=True):
        business_initiative = st.text_area("Describe your business initiative:", height=150)
        
        # Buttons for generating Epics and exporting to Excel
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Generate Domain Epics"):
                if business_initiative:
                    with st.spinner("Analyzing domains and generating implementation plan..."):
                        plan = generate_domain_epics(business_initiative)
                        if plan:
                            st.session_state.project['epics'] = plan['epics']
                            st.success(f"Generated {len(plan['epics'])} domain epics!")
        with col2:
            if st.button("Export to Excel"):
                if st.session_state.project['epics']:
                    excel_file = export_to_excel()
                    st.download_button(
                        label="📥 Download Excel",
                        data=excel_file,
                        file_name="project_plan.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.warning("No Epics generated yet. Generate Epics first.")

    # Epic Display Section
    if st.session_state.project['epics']:
        st.header("Domain Implementation Plans")
        
        # Create tabs for each domain
        tabs = st.tabs([epic['domain'] for epic in st.session_state.project['epics']])
        
        for idx, (tab, epic) in enumerate(zip(tabs, st.session_state.project['epics'])):
            with tab:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(epic['domain'])
                    st.markdown(f"**Objective:** {epic['objective']}")
                    
                    # Task Management
                    st.markdown("### 🛠 Implementation Tasks")
                    for task in epic['tasks']:
                        with st.expander(f"{task['name']} ({task['duration']} days)"):
                            st.markdown(f"**Owner:** {task['owner_team']}")
                            st.markdown(f"**Status:** {task['status']}")
                            st.markdown(f"**Dependencies:** {', '.join(task.get('dependencies', [])) or 'None'}")
                            
                with col2:
                    st.markdown("### 📈 Success Metrics")
                    for metric in epic['metrics']:
                        st.write(f"- {metric}")
                    
                    st.markdown("### ⚠️ Risks")
                    for risk in epic['risks']:
                        st.error(f"{risk['description']} ({risk['severity']})")

    # Gantt Chart Section
    if st.session_state.project['epics']:
        st.header("Project Visualization")
        
        # Buttons to switch between Detailed Project and Critical Path
        col1, col2 = st.columns(2)
        with col1:
            show_detailed = st.button("Show Detailed Project")
        with col2:
            show_critical_path = st.button("Show Critical Path")
        
        # Display the selected view
        if show_detailed:
            st.header("Detailed Project Plan")
            fig, gantt_data = draw_gantt_chart("Detailed Project")
            st.plotly_chart(fig, use_container_width=True)
        elif show_critical_path:
            st.header("Project Critical Path")
            fig, gantt_data = draw_gantt_chart("Critical Path")
            st.plotly_chart(fig, use_container_width=True)
            
            # Display critical path sequence
            critical_path = calculate_critical_path()
            if critical_path:
                st.markdown("### Critical Path Sequence")
                st.write(" → ".join(critical_path))
            else:
                st.warning("Could not determine critical path - check task dependencies.")