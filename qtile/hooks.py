import subprocess

from libqtile import hook


# Run the autostart.sh script on startup
@hook.subscribe.startup
def startup():
    subprocess.call("autostart.sh")
