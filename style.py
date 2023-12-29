import streamlit as st  # Import Streamlit for creating web applications

# Function to set the page container style
def set_page_container_style(
        max_width: int = 1500, max_width_100_percent: bool = False,
        padding_top: int = 1, padding_right: int = 10, padding_left: int = 1, padding_bottom: int = 10
    ):
        
        # If max_width_100_percent is True, the maximum width is set to 100%
        # Otherwise, it's set to the value of max_width
        if max_width_100_percent:
            max_width_str = f'max-width: 100%;'
        else:
            max_width_str = f'max-width: {max_width}px;'

        # CSS to modify the layout of the Streamlit page
        st.markdown(
            f'''
            <style>
                .reportview-container .css-1lcbmhc .css-1outpf7 {{
                    padding-top: 35px;
                }}
                .reportview-container .main .block-container {{
                    {max_width_str}
                    padding-top: {padding_top}rem;
                    padding-right: {padding_right}rem;
                    padding-left: {padding_left}rem;
                    padding-bottom: {padding_bottom}rem;
                }}
            </style>
            ''',
            unsafe_allow_html=True
        )

# Function to apply additional styles to the Streamlit page
def style():

    # Setting the page layout to wide mode
    st.set_page_config(layout="wide")

    # CSS for padding in the block container
    st.markdown("""
                    <style>
                        .appview-container .main .block-container {{
                            padding-top: {padding_top}rem;
                            padding-bottom: {padding_bottom}rem;
                            }}

                    </style>""".format(
                    padding_top=1, padding_bottom=1
                ),
                unsafe_allow_html=True
            )

    # Including Bootstrap CSS for additional styling options for the header of the application
    st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

    st.markdown("""
    <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #5848d5;">
    <a class="navbar-brand" href="https://www.kraken.com/" target="_blank"><b>KRAKEN</b></a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
        <li class="nav-item active">
            <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="https://github.com/mcastrocach/ppad/" target="_blank">GitHub</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="https://pypi.org/project/KrakenPythonMarcosRodrigo/0.1.0/" target="_blank">PyPi</a>
        </li>
        <li class="nav-item">
            <a class="nav-link" href="https://hub.docker.com/repository/docker/dixrow/krakenpythonmarcosrodrigo/general" target="_blank">Docker</a>
        </li>
        </ul>
    </div>
    </nav>
    """, unsafe_allow_html=True)

    # Calling the set_page_container_style function with specific parameters
    set_page_container_style(
            max_width = 1100, max_width_100_percent = True,
            padding_top = 0, padding_right = 10, padding_left = 5, padding_bottom = 10
    )

    # CSS to hide the main menu, footer, and header of the Streamlit page
    hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
    st.markdown(hide_st_style, unsafe_allow_html=True)