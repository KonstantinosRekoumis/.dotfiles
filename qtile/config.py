# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from audio import my_audio_mixer 

# Global Config Variables 
#Dracula color theme
theme = {"background": "#282a36",
        "current": "#44475a",
        "selection": "#44475a",
        "foreground": "#f8f8f2",
        "comment": "#6272a4",
        "cyan": "#8be9fd",
        "green": "#50fa7b",
        "orange": "#ffb86c",
        "pink": "#ff79c6",
        "purple": "#bd93f9",
        "red": "#ff5555",
        "yellow": "#f1fa8c"}

layout_params = {
        "border_focus": theme["cyan"],
        "border_width": 4,
        "margin": 5
}
mod = "mod4"
terminal = guess_terminal()
audio_mixer = my_audio_mixer()

def delta_vol(qtile,am:my_audio_mixer,incr:bool):
    am.delta_master_sink_volume(incr)

def mute(qtile,am:my_audio_mixer):
    am.enable_sink()

# add 'PlayPause', 'Next' or 'Previous'
music_cmd = ('dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify '
             '/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.')
def next_prev(action):
    def f(qtile):
        qtile.cmd_spawn(music_cmd + action)
    return f

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "s", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "w", lazy.spawn("rofi -show window"), desc="Launch rofi windows"),
    Key([mod], "r", lazy.spawn("rofi -show run"), desc="Launch rofi launcher"),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Screenshot"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Toggle Floating mode
    Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle floating"),
    # Toggle Keyboard layout
    Key([mod],'space', lazy.widget["keyboardlayout"].next_keyboard(), desc="Next keyboard layout."),
    # Audio Control
    Key([],'XF86AudioRaiseVolume',lazy.function(delta_vol,audio_mixer,True), desc = "Increment main audio output\'s volume"),
    Key([],'XF86AudioLowerVolume',lazy.function(delta_vol,audio_mixer,False), desc = "Decrement main audio output\'s volume"),
    Key([],'XF86AudioMute',lazy.function(mute,audio_mixer), desc = "Mute main audio output"),
    # https://github.com/qtile/qtile-examples/blob/master/sweenu/keys.py
    Key([], 'XF86AudioPlay', lazy.spawn(music_cmd + 'PlayPause')),
    Key([], 'XF86AudioNext', lazy.function(next_prev('Next'))),
    Key([], 'XF86AudioPrev', lazy.function(next_prev('Previous'))),
]


group_names = [ 
    ("MAIN",{"layout": "matrix"}),
    ("WWW1",{"layout": "matrix"}),
    ("WWW2",{"layout": "matrix"}),
    ("COMM",{"layout": "matrix"}),
    ("MUS", {"layout": "matrix"}),
    ("VID", {"layout": "matrix"}),
    ("STM", {"layout": "matrix"}),
    ("MISC",{"layout": "matrix"})
]
groups = [Group(name, **_kwargs) for name, _kwargs in group_names]

for i, group in enumerate(groups):
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                str(i+1),
                lazy.group[group.name].toscreen(),
                desc="Switch to group {}".format(group.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "control"],
                str(i+1),
                lazy.window.togroup(group.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(group.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # mod1 + shift + letter of group = move focused window to group
            Key([mod, "shift"], str(i+1), lazy.window.togroup(group.name),
                desc="move focused window to group {}".format(group.name)),
        ]
    )

layouts = [
    layout.Columns( **layout_params ),
    layout.Max( **layout_params ),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    layout.Matrix( **layout_params ),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="UbuntuMono",
    fontsize=19,
    padding=3,
    background = theme['background']
)
extension_defaults = widget_defaults.copy()
core_widgets = [ 
            # widget.TextBox(
            #     text = '⋛',
            #     background = theme['red']'#780907',
            #     foreground = theme["foreground"],
            # ),
            widget.CPU(
                foreground = theme["red"],
                format = '⨘ CPU {freq_current}GHz {load_percent}% ⨘'
            ),
            widget.Memory(
                foreground = theme["green"],
                format = '⨘ RAM: {MemUsed: .0f}{mm}/{MemTotal: .0f}{mm} ⨘'),
            widget.Net(
                foreground = theme["yellow"],
                format='⨘ Net ({interface}) : {down} ↓↑ {up} ⨘'),
            widget.KeyboardLayout(
                foreground = theme["cyan"],
                display_map = {
                    'us' : '⨘ 🇺🇸 US ⨘',
                    'gr' : '⨘ 🇬🇷 GR ⨘'},
                configured_keyboards = ['us','gr']),
            widget.Clock(
                foreground = theme["purple"],
                format=" ⨘ %A, %d-%m-%Y %I:%M %p ⨘"),
            widget.TextBox(
                text = '⨘ 🔊',
                foreground = theme["orange"],
                fontsize = 25
            ),
            widget.PulseVolume(
                foreground = theme["orange"],
            ),
            widget.TextBox(
                text = '⨘',
                foreground = theme["orange"],
                fontsize = 25
            ),
            # widget.BatteryIcon(battery=0)
            ]
widgets_0 = [ 
            widget.CurrentLayoutIcon(),
            widget.GroupBox(),
            widget.Prompt(),
            widget.WindowName(),
            # widget.Chord(
            #     chords_colors={
            #         "launch": ("#ff0000", "#ffffff"),
            #     },
            #     name_transform=lambda name: name.upper(),
            # ),
            *core_widgets,
            widget.Systray(),
            widget.QuickExit(),
            ]
widgets_1 = [
            widget.CurrentLayoutIcon(), 
            widget.GroupBox(),
            widget.WindowName(),
            widget.Chord(
                chords_colors={
                    "launch": ("#ff0000", "#ffffff"),
                },
                name_transform=lambda name: name.upper(),
            ),
            *core_widgets
            ]

screens = [
    Screen(
        wallpaper = "/home/konstantinos/Downloads/pexels-satoshi-hirayama-4058530.jpg",
        wallpaper_mode = "fill",
        top=bar.Bar(
            widgets_0,
            40,
            border_width=[0, 0, 2, 0],  # Draw top and bottom borders
            border_color=[theme["cyan"],theme["cyan"],theme["cyan"],theme["cyan"]],  # Borders are magenta
            background = theme["background"]
        ),
    ),
    Screen(
        wallpaper = "/home/konstantinos/Downloads/pexels-satoshi-hirayama-4058530.jpg",
        wallpaper_mode = "fill",
        top=bar.Bar(
            widgets_1,
            40,
            border_width=[0, 0, 2, 0],  # Draw top and bottom borders
            border_color=["#0f8c88", "000000", "#0f8c88", "000000"]  # Borders are magenta
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
