import os
import ast
import time
from gi.repository import GObject, GLib, Gtk, Gio, Gedit


SETTINGS_SCHEMA = "org.gnome.gedit.plugins.restoretabs"


class RestoreTabsWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "RestoreTabsWindowActivatable"
    window = GObject.property(type=Gedit.Window)


    def __init__(self):
        GObject.Object.__init__(self)
        self._handlers = []


    def do_activate(self):
        """
        Connect signal handlers.
        """
        handlers = []

        handler_id = self.window.connect("delete-event",
                                         self.on_window_delete_event)
        self._handlers.append(handler_id)

        handler_id = self.window.connect("tab-added",
                                         self.on_tab_change_event)
        self._handlers.append(handler_id)

        handler_id = self.window.connect("tab-removed",
                                        self.on_tab_change_event)
        self._handlers.append(handler_id)

        handler_id = self.window.connect("active-tab-state-changed",
                                         self.on_tab_change_event)
        self._handlers.append(handler_id)

        # temporary handler to catch the first time a window is shown
        self._temp_handler = self.window.connect("show", self.on_window_show)


    def do_deactivate(self):
        """
        Disconect any signal handlers that were added in do_activate().
        """
        [self.window.disconnect(handler_id) for handler_id in self._handlers]


    def do_update_state(self):
        pass


    def is_first_window(self):
        """
        Return True if the window being added is the first window instance.
        """
        print("is_first_window")
        app = Gedit.App.get_default()
        if len(app.get_windows()) <= 1:
            return True
        else:
            return False


    def on_window_delete_event(self, window, event, data=None):
        print("on_window_delete_event")
        uris = []
        app = Gedit.App.get_default()
        for document in app.get_documents():
            gfile = document.get_location()
            if gfile:
                uris.append(gfile.get_uri())
        for document in window.get_documents():
            gfile = document.get_location()
            # print(gfile.get_uri())
            if gfile:
                uris.remove(gfile.get_uri())
        settings = Gio.Settings.new(SETTINGS_SCHEMA)
        settings.set_value('uris', GLib.Variant("as", uris))
        print(uris)
        return False


    def on_tab_change_event(self, window, tab=None):
        print("on_tab_change_event")
        uris = []
        app = Gedit.App.get_default()
        for windows_list in app.get_windows():
            window_uris = []
            for document in windows_list.get_documents():
                # print(dir(window))
                gfile = document.get_location()
                if gfile:
                    window_uris.append(gfile.get_uri())
            uris.append(str(window_uris))
        if len(uris) > 0:
            settings = Gio.Settings.new(SETTINGS_SCHEMA)
            settings.set_value('uris', GLib.Variant("as", uris))
        print(uris)
        return False


    def on_window_show(self, window, data=None):
        print("on_window_show")
        """
        Only restore tabs if this window is the first Gedit window instance.
        """
        if self.is_first_window():
            tab = self.window.get_active_tab()
            if tab and tab.get_state() == 0 and not tab.get_document().get_location():
                self.window.close_tab(tab)
            settings = Gio.Settings.new(SETTINGS_SCHEMA)
            uris = settings.get_value('uris')
            app = Gedit.App.get_default()
            if uris:
                for count, uri in enumerate(uris, 1):
                    if count == 1:
                        w = self.window
                    else:
                        w = app.create_window(None)
                        w.show()
                        w.activate()
                    # print(uri)
                    if uri != "[]" or uri != "":
                        uri = ast.literal_eval(uri)
                        # print("URI: {}".format(uri))
                        for document_uri in uri:
                            location = Gio.file_new_for_uri(document_uri)
                            tab = w.get_tab_from_location(location)
                            # print(dir(tab))
                            if not tab:
                                w.create_tab_from_location(location, None, 0,
                                                           0, False, True)
            self.window.disconnect(self._temp_handler)
        # while time.sleep(60):
            uris = []
            for document in window.get_documents():
                gfile = document.get_location()
                if gfile:
                    uris.append(gfile.get_uri())
            settings = Gio.Settings.new(SETTINGS_SCHEMA)
            settings.set_value('uris', GLib.Variant("as", uris))
