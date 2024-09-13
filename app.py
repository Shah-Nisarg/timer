import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class TimerApp(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super(TimerApp, self).__init__(icon, parent)
        self.parent = parent
        self.setToolTip('Timer App')
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = 0

        # Create the menu
        self.menu = QtWidgets.QMenu(parent)
        self.create_timer_menu()
        self.setContextMenu(self.menu)

        # Handle tray icon activation
        self.activated.connect(self.on_click)

    def create_timer_menu(self):
        # Timer durations
        durations = [1, 5, 10, 15]  # minutes

        for minutes in durations:
            action = QtWidgets.QAction(f'Start {minutes}-Minute Timer', self)
            action.triggered.connect(lambda checked, m=minutes: self.start_timer(m))
            self.menu.addAction(action)

        self.menu.addSeparator()
        quit_action = QtWidgets.QAction('Quit', self)
        quit_action.triggered.connect(QtWidgets.qApp.quit)
        self.menu.addAction(quit_action)

    def start_timer(self, minutes):
        self.remaining_time = minutes * 60  # Convert minutes to seconds
        self.timer.start(1000)  # Timer updates every second
        self.showMessage('Timer Started', f'{minutes}-minute timer has started.')
        self.update_tooltip()

    def update_timer(self):
        self.remaining_time -= 1
        if self.remaining_time <= 0:
            self.timer.stop()
            self.showMessage('Timer Finished', 'Time is up!', icon=QtWidgets.QSystemTrayIcon.Critical)
            self.setIcon(QtGui.QIcon('red_icon.webp'))  # Change to a red icon
            # Optionally, make the icon blink
            self.blink_icon(True)
        else:
            self.update_tooltip()

    def update_tooltip(self):
        minutes, seconds = divmod(self.remaining_time, 60)
        self.setToolTip(f'Time Remaining: {minutes}:{seconds:02d}')

    def blink_icon(self, enable):
        if enable:
            self.blink_timer = QtCore.QTimer()
            self.blink_timer.timeout.connect(self.toggle_icon)
            self.blink_timer.start(500)  # Blink every half second
        else:
            self.blink_timer.stop()
            self.setIcon(QtGui.QIcon('timer_icon.webp'))

    def toggle_icon(self):
        current_icon = self.icon()
        if current_icon.cacheKey() == self.original_icon.cacheKey():
            self.setIcon(QtGui.QIcon('red_icon.webp'))
        else:
            self.setIcon(self.original_icon)

    def on_click(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            # Left-click action (optional)
            pass

def main():
    app = QtWidgets.QApplication(sys.argv)

    # Load icons
    timer_icon = QtGui.QIcon('timer_icon.webp')  # Your default icon
    red_icon = QtGui.QIcon('red_icon.webp')      # Icon when time is up

    tray_app = TimerApp(timer_icon)
    tray_app.original_icon = timer_icon  # Save the original icon for blinking
    tray_app.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
