from Utils.st_utils import *

def main():
    set_dashboard_style()
    sb_config = configure_sidebar()
    draw_body(sb_config)
    draw_footer()

if __name__ == "__main__":
    main()
