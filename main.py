import sys
from PySide6.QtWidgets import QApplication
from models.settings import Settings
from views.mainView import MainView
from LocalLogging.logger import FileLogger, ConsoleLogger

def parseArgs() -> tuple[bool, bool]:
   verbose = False
   console = False
   if len(sys.argv) > 1:
      for arg in sys.argv:
         if arg == 'verbose':
            verbose = True
         if arg == 'console':
            console = True
   return (verbose, console)

def main() -> None:
   verbose, console = parseArgs()
   app = QApplication(sys.argv)
   app.setApplicationName('Datasheets')
   app.setDesktopFileName('Datasheets')

   #region Layout
   logger = ConsoleLogger(True)
   logger.setNext(FileLogger('Datasheets', True))
   logger.start()
   settings = Settings(logger)
   # settings.openSettings()
   logger.setVerbose(settings.verbose if not verbose else verbose)
   logger.setConsole(settings.console if not console else console)
   try:
      # mainView = MainViewGrid()
      mainView = MainView(logger, settings)
      mainView.show()
      status = app.exec()
      print(status)
      sys.exit(status)
   except Exception as e:
      logger.error(e, 'Uncaught Error.')
   settings.saveSettings()
   logger.stop()
   #endregion


if __name__ == '__main__':
   main()
else:
   print('File is not a module.')