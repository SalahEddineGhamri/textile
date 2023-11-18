"""
Manages the file open and close
"""


class File:
  """
  wrapper of file
  """

  _file_path = ""
  _data = ""
  _mode = ""
  _file = None

  def __init__(self, file_path, mode):
    self._file_path = file_path
    self._mode = mode

  def getData(self):
    return self._data

  def __enter__(self):
    try:
      self._file = open(self._file_path, self._mode)
      self._data = self._file.read()
    except FileNotFoundError:
      pass
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    # print(exc_type, exc_value, traceback)
    self._file.close()
