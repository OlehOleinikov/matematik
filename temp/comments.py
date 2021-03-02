# Приклад застосування фільтру натискання миші (зняття виділення зі списку)
# self.open_modalwin_settings.listView_voice_in.installEventFilter(self)
# self.open_modalwin_settings.listView_voice_in.viewport().installEventFilter(self)

# def eventFilter(self, source, event):
#     if ((source is self.open_modalwin_settings.listView_voice_in and
#          event.type() == QEvent.KeyPress and
#          event.key() == Qt.Key_Escape and
#          event.modifiers() == Qt.NoModifier) or
#         (source is self.open_modalwin_settings.listView_voice_in.viewport() and
#          event.type() == QEvent.MouseButtonPress and
#          not self.open_modalwin_settings.listView_voice_in.indexAt(event.pos()).isValid()) or
#         (source is self.open_modalwin_settings.listView_voice_in.viewport() and
#         event.type() == QEvent.MouseButtonPress and
#          not self.open_modalwin_settings.listView_voice_in.indexAt(event.pos()).isValid())):
#         self.open_modalwin_settings.listView_voice_in.selectionModel().clear()
#     return super(SettingsWindow, self).eventFilter(source, event)