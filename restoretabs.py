import os
import logging, sys
import threading
from gi.repository import GObject, GLib, Gtk, Gio, Gedit

SETTINGS_SCHEMA = "org.gnome.gedit.plugins.restoretabs"

class RestoreTabsWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "RestoreTabsWindowActivatable"
    _temp_handler = None
    _curr_instance = 0
    _split_symbol='#'
    _curr_delete_window=False

    window = GObject.property(type=Gedit.Window)
    instance_count = 0
    uris = []
    lock=threading.Lock()

    def __init__(self):
        GObject.Object.__init__(self)
        self._handlers = []

    def do_activate(self):
        """
        Connect signal handlers.
        """
        logging.basicConfig(stream=sys.stderr, level=logging.ERROR)

        handlers = []
        handler_id = self.window.connect("delete-event", self.on_window_delete_event)
        self._handlers.append(handler_id)

        handler_id = self.window.connect("tab-added", self.on_window_tab_added)
        self._handlers.append(handler_id)

        handler_id = self.window.connect("tab-removed", self.on_window_tab_removed)
        self._handlers.append(handler_id)

        settings = Gio.Settings.new(SETTINGS_SCHEMA)
        uris = settings.get_value('uris')

        if uris:
            RestoreTabsWindowActivatable.lock.acquire()
            for uri in uris:
                if uri not in RestoreTabsWindowActivatable.uris:
                    RestoreTabsWindowActivatable.uris.append(uri)
            # temporary handler to catch the first time a window is shown
            self._temp_handler = self.window.connect("show", self.on_window_show, RestoreTabsWindowActivatable.uris)
            RestoreTabsWindowActivatable.lock.release()

    def do_deactivate(self):
        """
        Disconect any signal handlers that were added in do_activate().
        """
        [self.window.disconnect(handler_id) for handler_id in self._handlers]

    def do_update_state(self):
        pass

    def add_uri(self,uri):
        code = str(self._curr_instance)+RestoreTabsWindowActivatable._split_symbol+uri

        RestoreTabsWindowActivatable.lock.acquire()
        if code not in RestoreTabsWindowActivatable.uris:
            logging.debug("tab added "+code)
            RestoreTabsWindowActivatable.uris.append(code)
            settings = Gio.Settings.new(SETTINGS_SCHEMA)
            settings.set_value('uris', GLib.Variant("as", RestoreTabsWindowActivatable.uris))
        RestoreTabsWindowActivatable.lock.release()

    def remove_uri(self,uri):
        if self._curr_delete_window :
            logging.debug ("ignore remove on delete window")
            return

        code = str(self._curr_instance)+RestoreTabsWindowActivatable._split_symbol+uri

        RestoreTabsWindowActivatable.lock.acquire()
        if code in RestoreTabsWindowActivatable.uris:
            logging.debug("tab removed "+code)
            RestoreTabsWindowActivatable.uris.remove(code)
            settings = Gio.Settings.new(SETTINGS_SCHEMA)
            settings.set_value('uris', GLib.Variant("as", RestoreTabsWindowActivatable.uris))
        RestoreTabsWindowActivatable.lock.release()

    def on_window_tab_added(self, window, tab):
        """
        add tab to list
        """
        logging.debug("tab added")

        gfile = tab.get_document().get_location()
        if gfile:
            logging.debug ("gfile not null")
            self.add_uri(gfile.get_uri())

    def on_window_tab_removed(self, window, tab):
        """
        remove tab from list
        """
        logging.debug("tab removed")

        gfile = tab.get_document().get_location()
        if gfile:
            logging.debug ("gfile not null")
            self.remove_uri(gfile.get_uri())

    def on_window_delete_event(self, window, event, data=None):
        """
        save tabs, not saved at previous events may be
        """
        self._curr_delete_window=True
        for document in window.get_documents():
            gfile = document.get_location()
            if gfile:
                self.add_uri(gfile.get_uri())

        RestoreTabsWindowActivatable.lock.acquire()
        RestoreTabsWindowActivatable.instance_count -= 1
        RestoreTabsWindowActivatable.lock.release()
        return False

    def on_window_show(self, window, uris):
        """
        Only restore tabs if this window is the first Gedit window instance.
        """
        self.window.disconnect(self._temp_handler)
        self._temp_handler = None

        RestoreTabsWindowActivatable.lock.acquire()
        self._curr_instance = RestoreTabsWindowActivatable.instance_count
        logging.debug ("curr instance = "+str(self._curr_instance))
        RestoreTabsWindowActivatable.instance_count += 1
        RestoreTabsWindowActivatable.lock.release()

        active_tab = self.window.get_active_tab()
        # in gedit <= 3.6, tabs are added before the window is shown
        # in gedit >= 3.8, tabs are added after
        if active_tab:
            self.on_tab_added(window, active_tab)

        for uri in uris:
            logging.debug ("restoring "+uri)
            num_str,uri_str = uri.split(RestoreTabsWindowActivatable._split_symbol)

            if self._curr_instance != int(num_str):
                logging.debug ("not current instance, ignoring "+num_str)
                continue

            if not os.path.isfile(uri_str if uri_str[:7]!='file://' else uri_str[7:]):
                logging.debug ("file not exist, removing from list "+uri_str)
                continue

            location = Gio.file_new_for_uri(uri_str)
            tab = self.window.get_tab_from_location(location)
            if not tab:
                self.window.create_tab_from_location(location, None, 0,
                                                     0, False, True)

        if not active_tab:
            self._temp_handler = window.connect("tab-added", self.on_tab_added)

    def on_tab_added(self, window, tab):
        """
        Close the first tab if it is empty.
        """
        logging.debug ("on_tab_added")

        if tab.get_state() == Gedit.TabState.STATE_NORMAL and tab.get_document().is_untouched():
            def close_tab():
                window.close_tab(tab)
                return False
            try:
                GLib.idle_add(close_tab)
            except TypeError:
                GObject.idle_add(close_tab)

        if self._temp_handler is not None:
            window.disconnect(self._temp_handler)
            self._temp_handler = None

