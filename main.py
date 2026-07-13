from Utils.st_utils import *

def main():
    set_dashboard_style()
    session_state = configure_sidebar()
    draw_body(session_state)
    draw_footer()

if __name__ == "__main__":
    main()
