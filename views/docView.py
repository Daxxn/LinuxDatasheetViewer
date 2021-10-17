from PySide6.QtWidgets import QGridLayout, QWidget

class DocViewer(QWidget):
   def __init__(self, logger, settings, parent = None) -> None:
      super(DocViewer, self).__init__(self, parent)
      self.logger = logger
      self.settings = settings

      self.baseGrid = QGridLayout()

      self.setLayout(self.baseGrid)