import os
import streamlit as st
from utils.video_utils import save_video
from utils.tts import SpeechTextConverter
from core import get_explanations, generate_video, CACHE_DIR
from helper import (
    get_app_styling,
    read_logo_image,
    get_files_types,
    copy_local_folder,
    is_valid_github_repo_url,
    clone_github_repo
)
# to avoid torch error
import torch
import types
if hasattr(torch, "classes"):
    torch.classes.__path__ = types.SimpleNamespace(_path=[])


# SETUP
st.set_page_config(
    page_title="Code Explainer Video AI Generator",
    page_icon="🎬",
    layout="wide"
)
st.markdown(f"<style>{get_app_styling()}</style>", unsafe_allow_html=True)


# INITIALIZE TTS
@st.cache_resource
def init_tts():
    return SpeechTextConverter()


# INITIALIZE session state
if 'step' not in st.session_state:
    st.session_state.step = 1
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
if 'project_title' not in st.session_state:
    st.session_state.project_title = ""
if 'project_subtitle' not in st.session_state:
    st.session_state.project_subtitle = ""
if 'video_bytes' not in st.session_state:
    st.session_state.video_bytes = None


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
        logo_b64 = read_logo_image()
        return f'<img src="data:image/png;base64,{logo_b64}" alt="CEVAIG Logo" style="height: 160px;">'
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
        st.markdown("<h2 style='text-align: center; font-family: \"Glacial Indifference\", sans-serif; color: #fff2db;'>Generate video tutorials for any coding project in any language</h2>", unsafe_allow_html=True)
        title = st.text_input("Project Title", key="project_title")
        subtitle = st.text_input("Project Subtitle", key="project_subtitle")
        if st.button("GET STARTED"):
            if title:
                go_to_step(2)
            else:
                st.error('Enter the project title to continue')


# STEP 2: Project Selection
elif st.session_state.step == 2:
    with create_step_container():
        st.markdown("<div class='step-header'>Select Your Project</div>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Local Project", "GitHub Repository"])
        
        with tab1:
            user_project_dir = st.text_input("Local Project Directory Path")
            if st.button("Use Local Directory", key="local_button"):
                if user_project_dir and os.path.exists(user_project_dir):
                    copy_local_folder(user_project_dir)
                    go_to_step(3)
                else:
                    st.error("Please enter a valid project directory path")
        with tab2:
            st.session_state.github_link = st.text_input("GitHub Repository URL", value=st.session_state.github_link)
            if st.button("Connect Repository", key="github_button"):
                if (st.session_state.github_link
                    and is_valid_github_repo_url(st.session_state.github_link)):
                    clone_github_repo(st.session_state.github_link)
                    go_to_step(3)
                else:
                    st.error("Please enter a valid GitHub repository URL")
        display_navigation_buttons(2, show_next=False)


# STEP 3: File Type Selection
elif st.session_state.step == 3:
    with create_step_container():
        st.markdown("<div class='step-header'>Choose What File Types to Ignore</div>", unsafe_allow_html=True)
        
        # Container with dark background
        with st.container():
            # Common file extensions
            file_types = get_files_types()
            
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
                st.session_state.explanations = get_explanations()
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
                        value=explanation['explanatory_text'],
                        key=f"explanation_{i}",
                        height=100
                    )
                    st.session_state.explanations[i]['explanatory_text'] = new_text
                    
                    # File path (not modifiable)
                    st.markdown(f"**File:** {explanation['file_path']}")
                    # Line range for highlighting (modifiable)
                    st.markdown("<div class='line-numbers-container'>", unsafe_allow_html=True)
                    st.markdown("**Line range:**")
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        start_line = st.number_input(
                            "Start Line",
                            min_value=0,
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
                        tts = init_tts()
                        # Call the video generation function
                        video = generate_video(
                            tts,
                            st.session_state.explanations,
                            st.session_state.project_title,
                            st.session_state.project_subtitle
                        )
                        video_path = f"{CACHE_DIR}{st.session_state.project_title}.mp4"
                        save_video(video, video_path)
                        st.success(f"Video generated successfully at: {video_path}")
                        
                        # Display the video
                        video_file = open(video_path, 'rb')
                        video_bytes = video_file.read()
                        st.session_state.video_bytes = video_bytes
                    except Exception as e:
                        st.error(f"Error generating video: {str(e)}")
            if st.session_state.video_bytes:
                st.video(st.session_state.video_bytes)
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
                        data=st.session_state.video_bytes,
                        file_name="code_explainer_tutorial.mp4",
                        mime="video/mp4"
                    )
                    st.markdown("</div>", unsafe_allow_html=True)
