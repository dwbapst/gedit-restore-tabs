Gedit Restore Tabs
==================

This is a plugin for [Gedit][1], the official text editor of the GNOME desktop
environment. 

This plugin is for Gedit versions 3 and above (including 3.8 and 3.10, included in Ubuntu 14.04).

**This plugin is NOT compatible with Gedit 2.x**.

Upon starting Gedit, this plugin will try restore all open documents from the 
*last* Gedit window that was closed.


Installation
------------

1. Download the source code form this repository or using the `git clone` command:

    git clone git://github.com/raelgc/gedit-restore-tabs.git

2. Copy the files to the Gedit plugins directory `~/.local/share/gedit/plugins/`.

    cp restoretabs.* ~/.local/share/gedit/plugins/

3. Copy and compile the settings schema **as root**.

    sudo cp org.gnome.gedit.plugins.restoretabs.gschema.xml /usr/share/glib-2.0/schemas/
    sudo glib-compile-schemas /usr/share/glib-2.0/schemas/

4. Restart Gedit.

5. Activate the plugin in the Gedit preferences dialog.

[1]: http://www.gedit.org



