Gedit Restore Tabs
==================

This is a plugin for [Gedit][1], the official text editor of the GNOME desktop
environment. It's a fork from the no more maintained [restore-tabs plugin](https://github.com/Quixotix/gedit-restore-tabs). 

This plugin is for Gedit versions 3.36 and above (included in Ubuntu 20.04).

**This plugin is NOT compatible with Gedit 2.x**.

Upon starting Gedit, this plugin will try restore all open documents from the 
*last* Gedit window that was closed.


Installation
------------

1. Download the source code from this repository and extract: 

       wget https://github.com/raelgc/gedit-restore-tabs/archive/master.zip -O gedit-restore-tabs.zip
       unzip gedit-restore-tabs.zip

2. After extract, copy the files to your Gedit plugins directory:

       cd gedit-restore-tabs-master
       mkdir -p ~/.local/share/gedit/plugins
       cp restoretabs.* ~/.local/share/gedit/plugins/

3. Copy and compile the settings schema as sudo/root:

       sudo cp org.gnome.gedit.plugins.restoretabs.gschema.xml /usr/share/glib-2.0/schemas/
       sudo glib-compile-schemas /usr/share/glib-2.0/schemas/

4. Restart Gedit.

5. Activate the plugin: go to `Edit` > `Preferences`, select `Plugins` tab and check `Restore Tabs` entry.

[1]: http://www.gedit.org
