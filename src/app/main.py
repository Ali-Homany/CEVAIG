import os
import base64
import streamlit as st


# SETUP
st.set_page_config(
    page_title="Code Explainer Video AI Generator",
    page_icon="🎬",
    layout="wide"
)
with open("./app/styling.css", "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# INITIALIZE session state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'project_source' not in st.session_state:
    st.session_state.project_source = None
if 'ignored_filetypes' not in st.session_state:
    st.session_state.ignored_filetypes = []
if 'num_explanations' not in st.session_state:
    st.session_state.num_explanations = 15
if 'voice_speed' not in st.session_state:
    st.session_state.voice_speed = 1.0
if 'custom_prompt' not in st.session_state:
    st.session_state.custom_prompt = ""
if 'explanations' not in st.session_state:
    st.session_state.explanations = []
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = None
if 'github_link' not in st.session_state:
    st.session_state.github_link = ""


# CLONES (methods to be replaced with actual app logic)
def get_explanations_clone(*args):
    """Simulate parsing and explaining a codebase"""
    return [
        {
            "text": "Alright, so the big idea here is to take a codebase and automatically generates video tutorials explaining the code structure and functionality.", 
            "file_path": "main.py", 
            "start_line": 1, 
            "end_line": 15
        },
        {
            "text": "Within `explainer`, `codebase_parser.py` is responsible for reading and preparing the codebase for analysis. It handles file traversal and code extraction.", 
            "file_path": "explainer/codebase_parser.py", 
            "start_line": 5, 
            "end_line": 28
        },
        {
            "text": "Now, `llms.py` is where we interact with the LLM itself. In this case, it's set up to generate natural language explanations of code sections.", 
            "file_path": "llms.py", 
            "start_line": 10, 
            "end_line": 42
        },
        {
            "text": "The `utils.py` file contains helper functions used throughout the project for file handling and text processing.", 
            "file_path": "utils.py", 
            "start_line": 7, 
            "end_line": 35
        },
        {
            "text": "Moving to `video_generator.py`, this is where we convert our explanations to video using text-to-speech and visual elements.", 
            "file_path": "video_generator.py", 
            "start_line": 12, 
            "end_line": 87
        },
    ]
def generate_video_clone(*args):
    """Returns sample video"""
    return "video_tutorial.mp4"
def get_files_types_clone(*args) -> list[str]:
    """Gets unique file types in the given project"""
    return ["py", "js", "html", "css", "java", 
            "cpp", "h", "go", "rb", "php", 
            "swift", "kt", "ts", "json", "yaml", 
            "md", "ipynb", "jsx", "ejs", "vue"]


# main container, we'll be used to wrap each step block
def create_step_container():
    return st.container()
# navigation (prev, next) used for several steps
def go_to_step(step):
    """Navigate between steps"""
    st.session_state.step = step
def display_navigation_buttons(curr_step=None, show_next: bool=True):
    """Display back and next navigation buttons"""
    back_step = curr_step - 1
    next_step = curr_step + 1
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if back_step:
            if st.button("Back", key=f"back_to_step{back_step}"):
                go_to_step(back_step)
    with col2:
        if next_step and show_next:
            if st.button("Next", key=f"go_to_step{next_step}"):
                go_to_step(next_step)


# LOGO
def load_and_display_logo():
    try:
        # check if logo.png exists in the current directory
        if os.path.exists("./app/logo.png"):
            with open("./app/logo.png", "rb") as f:
                logo_data = f.read()
                logo_b64 = base64.b64encode(logo_data).decode()
                return f'<img src="data:image/png;base64,{logo_b64}" alt="CEVAIG Logo" style="height: 160px;">'
        else:
            # Fallback to text if logo.png is not found
            return '<h1 style="font-family: \'Glacial Indifference\', sans-serif; color: #fff2db;">CEVAIG</h1>'
    except Exception as e:
        return '<h1 style="font-family: \'Glacial Indifference\', sans-serif; color: #fff2db;">CEVAIG</h1>'


# PROGRESS BAR
def display_progress_bar():
    """Display progress bar based on current step"""
    total_steps = 7  # Updated from 6 to 7
    progress = st.session_state.step / total_steps

    st.progress(progress)
    steps = ["Start", "Select Project", "Filter Files", "Configure", "Customize", "Generate", "Video"]
    cols = st.columns(len(steps))
    # create
    for i, (col, step_name) in enumerate(zip(cols, steps)):
        with col:
            if i + 1 < st.session_state.step:
                st.markdown(f"<div style='text-align: center; color: #0097a6;'>{step_name} ✓</div>", unsafe_allow_html=True)
            elif i + 1 == st.session_state.step:
                st.markdown(f"<div style='text-align: center; font-weight: bold; color: #fff2db;'>{step_name}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: center; color: #545454;'>{step_name}</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# HEADER
st.markdown(f"<div class='logo-header'>{load_and_display_logo()}</div>", unsafe_allow_html=True)
display_progress_bar()


# STEP 1: Landing Page
if st.session_state.step == 1:
    with create_step_container():
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; font-family: \"Glacial Indifference\", sans-serif; color: #fff2db;'>Generate video tutorials for any coding project in any language</h2>", unsafe_allow_html=True)
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        if st.button("GET STARTED"):
            go_to_step(2)


# STEP 2: Project Selection
elif st.session_state.step == 2:
    with create_step_container():
        st.markdown("<div class='step-header'>Select Your Project</div>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["GitHub Repository", "Local Project"])
        
        with tab1:
            st.session_state.github_link = st.text_input("GitHub Repository URL", value=st.session_state.github_link)
            if st.button("Connect Repository", key="github_button"):
                if st.session_state.github_link:
                    st.session_state.project_source = {"type": "github", "url": st.session_state.github_link}
                    go_to_step(3)
                else:
                    st.error("Please enter a valid GitHub repository URL")
        
        with tab2:
            uploaded_files = st.file_uploader("Upload Project Files", accept_multiple_files=True, type=None)
            if uploaded_files:
                st.session_state.uploaded_files = uploaded_files
            
            if st.button("Use Local Files", key="local_button"):
                if st.session_state.uploaded_files:
                    st.session_state.project_source = {"type": "local", "files": st.session_state.uploaded_files}
                    go_to_step(3)
                else:
                    st.error("Please upload at least one file")


# STEP 3: File Type Selection
elif st.session_state.step == 3:
    with create_step_container():
        st.markdown("<div class='step-header'>Choose What File Types to Ignore</div>", unsafe_allow_html=True)
        
        # Container with dark background
        with st.container():
            # Common file extensions
            file_types = get_files_types_clone()
            
            # Create a grid of checkboxes using columns
            cols_per_row = 5
            rows = len(file_types) // cols_per_row + (1 if len(file_types) % cols_per_row > 0 else 0)
            
            for row in range(rows):
                cols = st.columns(cols_per_row)
                for i in range(cols_per_row):
                    idx = row * cols_per_row + i
                    if idx < len(file_types):
                        ext = file_types[idx]
                        with cols[i]:
                            if st.checkbox(ext, value=ext in st.session_state.ignored_filetypes):
                                if ext not in st.session_state.ignored_filetypes:
                                    st.session_state.ignored_filetypes.append(ext)
                            else:
                                if ext in st.session_state.ignored_filetypes:
                                    st.session_state.ignored_filetypes.remove(ext)
            st.markdown("</div>", unsafe_allow_html=True)
        display_navigation_buttons(3)


# STEP 4: Configuration Settings
elif st.session_state.step == 4:
    with create_step_container():
        st.markdown("<div class='step-header'>Configure Your Explanations</div>", unsafe_allow_html=True)
        
        # Container with dark background
        with st.container():
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("<h3>Number of Explanations</h3>", unsafe_allow_html=True)
                num_explanations = st.slider(
                    "", 
                    min_value=5, 
                    max_value=30, 
                    value=st.session_state.num_explanations,
                    step=1
                )
                st.session_state.num_explanations = num_explanations
            
            with col2:
                st.markdown("<h3>Explainer Voice Speed</h3>", unsafe_allow_html=True)
                voice_speed = st.slider(
                    "", 
                    min_value=0.5, 
                    max_value=2.0, 
                    value=st.session_state.voice_speed,
                    step=0.1
                )
                st.session_state.voice_speed = voice_speed
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        display_navigation_buttons(4)


# STEP 5: Customize Explanation Tone
elif st.session_state.step == 5:
    with create_step_container():
        st.markdown("<div class='step-header'>Customize the Explanations Tone (Optional)</div>", unsafe_allow_html=True)
        
        # Container with dark background
        with st.container():
            # Allow empty prompt if user wants default behavior
            custom_prompt = st.text_area(
                "", 
                value=st.session_state.custom_prompt,
                height=200,
                placeholder="Leave empty to use default explanation style..."
            )
            st.session_state.custom_prompt = custom_prompt
            st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Back", key="back_to_step4"):
                go_to_step(4)
        with col2:
            if st.button("Generate Explanations", key="generate_explanations"):
                # In a real app, this would parse the codebase and generate explanations
                st.session_state.explanations = get_explanations_clone()
                go_to_step(6)


# STEP 6: Edit & Confirm Explanations
elif st.session_state.step == 6:
    with create_step_container():
        st.markdown("<div class='step-header'>Edit & Confirm Explanations</div>", unsafe_allow_html=True)
        
        # Container with dark background
        with st.container():
            # Display and allow editing of explanations
            explanations = st.session_state.explanations.copy()
            
            for i, explanation in enumerate(explanations):
                with st.expander(f"Explanation {i+1}: {explanation['file_path']}"):
                    # Explanation text (modifiable)
                    new_text = st.text_area(
                        "Edit explanation:", 
                        value=explanation['text'],
                        key=f"explanation_{i}",
                        height=100
                    )
                    st.session_state.explanations[i]['text'] = new_text
                    
                    # File path (not modifiable)
                    st.markdown(f"**File:** {explanation['file_path']}")
                    # Line range for highlighting (modifiable)
                    st.markdown("<div class='line-numbers-container'>", unsafe_allow_html=True)
                    st.markdown("**Line range:**")
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        start_line = st.number_input(
                            "Start Line", 
                            min_value=1, 
                            value=explanation['start_line'],
                            key=f"start_line_{i}"
                        )
                        st.session_state.explanations[i]['start_line'] = start_line
                    
                    with col2:
                        end_line = st.number_input(
                            "End Line", 
                            min_value=start_line, 
                            value=max(explanation['end_line'], start_line),
                            key=f"end_line_{i}"
                        )
                        st.session_state.explanations[i]['end_line'] = end_line
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        with col1:
            display_navigation_buttons(6, show_next=False)
        with col2:
            if st.button("Proceed to Video Generation", key="go_to_step7"):
                go_to_step(7)


# Step 7: Video Generation
elif st.session_state.step == 7:
    with create_step_container():
        st.markdown("<div class='step-header'>Generate Video</div>", unsafe_allow_html=True)
        
        # Container with dark background
        with st.container():
            st.markdown("<div class='info-text'>Click the button below to generate a video explanation of your code.</div>", unsafe_allow_html=True)
            
            if st.button("Generate Video", key="generate_video"):
                with st.spinner("Generating video..."):
                    try:
                        # Call the video generation function
                        video_path = generate_video_clone(st.session_state.explanations)
                        st.success(f"Video generated successfully at: {video_path}")
                        
                        # Display the video
                        video_file = open(video_path, 'rb')
                        video_bytes = video_file.read()
                        st.video(video_bytes)
                    except Exception as e:
                        st.error(f"Error generating video: {str(e)}")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Navigation button to go back
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Back to Explanations", key="back_to_step6"):
                go_to_step(6)
        with col2:
            # Create a download button
            st.markdown("<h3>Download Your Tutorial</h3>", unsafe_allow_html=True)
            st.markdown("<p>Your code explanation video is ready!</p>", unsafe_allow_html=True)
            st.download_button(
                label="DOWNLOAD VIDEO",
                data=b"This would be the actual video data",
                file_name="code_explainer_tutorial.mp4",
                mime="video/mp4"
            )
            st.markdown("</div>", unsafe_allow_html=True)
