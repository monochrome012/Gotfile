from libqtile.config import Click, Drag, Group, Key
from libqtile.lazy import lazy

mod = "mod4"
terminal = "alacritty"

keys = [
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod], "comma", lazy.next_screen()),
    Key([mod], "period", lazy.prev_screen()),
    Key([mod, "shift"], "f", lazy.window.toggle_floating()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "Return", lazy.spawn(terminal)),
    Key([mod], "b", lazy.hide_show_bar("top")),
    Key([mod], "space", lazy.spawn("rofi -show run -font 'SourceCodePro 15'")),
    Key([mod], "q", lazy.window.kill()),
    Key([], "XF86MonBrightnessUp",
        lazy.spawn("/home/liuhao/Scripts/light_up.sh")),
    Key([], "XF86MonBrightnessDown",
        lazy.spawn("/home/liuhao/Scripts/light_down.sh")),
    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("/home/liuhao/Scripts/volume_up.sh")),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("/home/liuhao/Scripts/volume_down.sh")),
    Key([], "XF86AudioMute",
        lazy.spawn("/home/liuhao/Scripts/volume_mute.sh")),
    Key([], "Print", lazy.spawn("flameshot gui")),

    # Tile
    Key([mod], "j", lazy.group.next_window()),
    Key([mod], "k", lazy.group.prev_window()),
    Key([mod], "h", lazy.layout.decrease_ratio()),
    Key([mod], "l", lazy.layout.increase_ratio()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_down()),
    Key([mod], "i", lazy.layout.increase_nmaster()),
    Key([mod], "d", lazy.layout.decrease_nmaster()),

    # # Bsp
    # Key([mod], "n", lazy.group.next_window()),
    # Key([mod], "p", lazy.group.prev_window()),
    # Key([mod], "j", lazy.layout.down()),
    # Key([mod], "k", lazy.layout.up()),
    # Key([mod], "h", lazy.layout.left()),
    # Key([mod], "l", lazy.layout.right()),
    # Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    # Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    # Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    # Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    # Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    # Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    # Key([mod, "mod1"], "h", lazy.layout.flip_left()),
    # Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    # Key([mod, "control"], "j", lazy.layout.grow_down()),
    # Key([mod, "control"], "k", lazy.layout.grow_up()),
    # Key([mod, "control"], "h", lazy.layout.grow_left()),
    # Key([mod, "control"], "l", lazy.layout.grow_right()),
    # Key([mod, "shift"], "n", lazy.layout.normalize()),
    # Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
]

groups = [Group(i) for i in "123456789"]

for number, i in enumerate(groups):
    keys.append(
        Key([mod], str(number + 1), lazy.group[i.name].toscreen(toggle=False)))
    keys.append(
        Key([mod, "shift"], str(number + 1), lazy.window.togroup(i.name)))

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod],
        "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size(),
    ),
    Click(
        [mod],
        "Button2",
        lazy.window.bring_to_front(),
    ),
]

from libqtile.config import DropDown, ScratchPad

groups.append(
    ScratchPad("scratchpad", [
        DropDown(
            "term",
            "/usr/bin/alacritty",
            x=0.1,
            y=0.1,
            height=0.8,
            width=0.8,
        )
    ]), )

keys.extend([
    Key([mod,"shift"], 'space', lazy.group['scratchpad'].dropdown_toggle('term')),
])
