## Gedit Restore Tabs

This is a plugin for [Gedit][1], the official text editor of the GNOME desktop
environment. 

This version was forked from Rael Gugelmin Cunha's branch (https://github.com/raelgc/gedit-restore-tabs) by Kasual (branch: https://github.com/Kasual/gedit-restore-tabs) to fix Python3 support, and by Juraj Bano (https://github.com/jurajbano/gedit-restore-tabs) to restore tabs in multiple windows.

This plugin is for Gedit versions 3 and above (including 3.8 and 3.10, included in Ubuntu 14.04).

**This plugin is NOT compatible with Gedit 2.x**.

Upon starting Gedit, this plugin will try restore all open documents from the 
*last* Gedit window that was closed.


## Installation

1. Download the source code form this repository or using the `git clone` command.
2. Copy the files to the Gedit plugins directory `~/.local/share/gedit/plugins/`.
3. Copy and compile the settings schema **as root**.
4. Restart Gedit.
5. Activate the plugin in the Gedit preferences dialog.

#### Example Installation for Ubuntu

    ```
    git clone git://github.com/dwbapst/gedit-restore-tabs.git
    cp restoretabs.* ~/.local/share/gedit/plugins/    
    sudo cp org.gnome.gedit.plugins.restoretabs.gschema.xml /usr/share/glib-2.0/schemas/
    sudo glib-compile-schemas /usr/share/glib-2.0/schemas/
    ```
Then restart Gedit, and activate the plugin by going to `Edit` > `Preferences`, select `Plugins` tab and check `Restore Tabs` entry.

[1]: http://www.gedit.org



