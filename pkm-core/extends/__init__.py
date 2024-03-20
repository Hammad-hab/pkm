#  ███████╗██╗  ██╗████████╗███████╗███╗   ██╗███████╗██╗ ██████╗ ███╗   ██╗███████╗
#  ██╔════╝╚██╗██╔╝╚══██╔══╝██╔════╝████╗  ██║██╔════╝██║██╔═══██╗████╗  ██║██╔════╝
#  █████╗   ╚███╔╝    ██║   █████╗  ██╔██╗ ██║███████╗██║██║   ██║██╔██╗ ██║███████╗
#  ██╔══╝   ██╔██╗    ██║   ██╔══╝  ██║╚██╗██║╚════██║██║██║   ██║██║╚██╗██║╚════██║
#  ███████╗██╔╝ ██╗   ██║   ███████╗██║ ╚████║███████║██║╚██████╔╝██║ ╚████║███████║
#  ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═══╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝
#  This is the Extensions file. You can use this to extend pkm's behavior.
#  Do not modify directly

EXTENSIONS = {
    # Program control customizations
    "on_before_start": lambda: 0,
    "on_after_start": lambda: 0,
    "on_app_end": lambda: 0,
    "on_app_start": lambda: 0,
    
    # Log customizations
    "error_attrs": [],
    "success_attrs": [],
    "warning_attrs": [],
    "info_attrs": [],
    
    # Progress bar customizations
    "progress_absence": "░",
    "progress_fill": "▓",
    "progress_bar_start": "[",
    "progress_bar_end": "]",
}
