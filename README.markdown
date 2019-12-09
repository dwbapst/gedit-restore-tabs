## Gedit Restore Tabs

This is a plugin for [Gedit][1], the official text editor of the GNOME desktop
environment. 

This plugin was originally written by Micah Carrick, and licensed to distribute under the GNU GPL 3.0 License (apparently?). The particular version in this repository/branch was forked from Rael Gugelmin Cunha's branch (https://github.com/raelgc/gedit-restore-tabs) by Kasual (branch: https://github.com/Kasual/gedit-restore-tabs) to fix Python3 support, and by Maxim Akristiniy (branch: (https://github.com/AMV007/gedit-restore-tabs) to add save and restore tabs in multiple windows.

This plugin is for Gedit versions 3 and above (including 3.8 and 3.10, included in Ubuntu 14.04).

**This plugin is NOT compatible with Gedit 2.x**.

Upon starting Gedit, this plugin will try restore all open documents from the 
*last* Gedit window that was closed.


### Installation

1. Download the source code form this repository or using the `git clone` command.
2. Copy the files to the Gedit plugins directory `~/.local/share/gedit/plugins/`.
3. Copy and compile the settings schema **as root**, because we need to add a `glib` schema, and gedit looks in the /usr/ directory in the file system - so we'll need to put the newly compiled schemas database there, and that requires root privileges.
4. Restart Gedit.
5. Activate the plugin in the Gedit preferences dialog.

#### Example Installation for Ubuntu

Clone the repo and move to it.

    git clone git://github.com/dwbapst/gedit-restore-tabs.git -b branch-hill
    cd ./gedit-restore-tabs/
    
Copy all the files that begin with `restoretabs.*` to the local plugins folder.
    
    cp restoretabs.* ~/.local/share/gedit/plugins/    
    
The following commands need to be done with root privileges
    
    sudo cp org.gnome.gedit.plugins.restoretabs.gschema.xml /usr/share/glib-2.0/schemas/
    sudo glib-compile-schemas /usr/share/glib-2.0/schemas/
    
Then restart Gedit, and activate the plugin by going to `Edit` > `Preferences`, select `Plugins` tab and check `Restore Tabs` entry.

[1]: http://www.gedit.org
