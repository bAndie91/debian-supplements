# Use it

## Gtk2

For Gtk2 apps edit `~/.gtkrc-2.0`:

```
gtk-cursor-theme-name="xcore-large"
gtk-cursor-theme-size=64
```

## Gtk3

For Gtk3 apps edit `~/.config/gtk-3.0/settings.ini`:

```
[Settings]
gtk-cursor-theme-name=xcore-large
gtk-cursor-theme-size=64
```

(no quotes around `xcode-large`)

## GSettings

- for Gtk3 apps with Wayland backend
- Gtk4
- SDL3

```
gsettings set org.gnome.desktop.interface cursor-theme xcore-large
gsettings set org.gnome.desktop.interface cursor-size 64
```

## Xlib

For bare Xlib apps (via libXcursor, libxcb-cursor), FLTK and Qt6 (in same cases),
set Xresources and apply by `xrdb -merge`:

```
Xcursor.theme: xcore-large
Xcursor.size: 64
```

override by env vars:

```
export XCURSOR_THEME=xcore-large XCURSOR_SIZE=64
xsetroot -cursor_name left_ptr
icewm --restart
```


# Notes

Every cursor is scaled by size/16, so left_ptr at size 64 is four times
its native height. If the arrow looks too big or too small compared with
other themes at the same nominal size, change BASE.

Sizes like 24 (×1.5) and 72 (×4.5) can’t be pixel-exact, so those get
anti-aliased edges. 32, 48 and 96 are exact multiples of 16 and stay
crisp.

The core font has no animated or “arrow + busy” cursor, so
left_ptr_watch, progress and wait are aliased to the plain watch glyph.
Modern names such as not-allowed and zoom-in have no core equivalent, so
apps that ask for them fall back to the default arrow.

Some Xorg drivers limit hardware cursors to 64×64 or 128×128, as
mentioned before. If 96 looks clipped or corrupted, that is the cause,
and 64 or 72 will work.
