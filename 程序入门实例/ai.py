import win32gui,re
class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__ (self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """基于类名来查找窗口"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, class_name_wildcard_list):
        """传递给win32gui.EnumWindows()，检查所有打开的顶级窗口"""
        class_name,wildcard=class_name_wildcard_list
        if win32gui.GetClassName(hwnd)==class_name and re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, class_name,wildcard):
        """根据类名，查找一个顶级窗口，确保其类名相符，且标题可以用正则表达式匹配对应的通配符"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback,[class_name, wildcard])
        return self._handle

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

    def get_hwnd(self):
        """return hwnd for further use"""
        return self._handle

if __name__=="__main__":
    myWindowMgr=WindowMgr()
    '''查找一个类名为SunAwtFrame，窗口标题中含【银行余额】字符串的窗口，并返回它的句柄；如果没找到，返回None'''
    excelHwnd=myWindowMgr.find_window_wildcard("SunAwtFrame",".*?永中简报.*?")
    print(excelHwnd)