import win32service
import win32event
import win32serviceutil
import servicemanager
from src.leap.bitmask_root.windows.windows_implementation import *


class WinInstaller(win32serviceutil.ServiceFramework):
    _svc_name_ = "bitmask-root"
    _svc_display_name_ = "Bitmask Root"
    _svc_description_ = "Administrative service for bitmask client"
    _stoped = False
    _server = None

    def __init__(self, args):
        self._server = BitmaskRootWindows("tcp://%s:%s" % (host, port))
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self._stoped = True

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self._server.start()
        self.main()

    def main(self):
        while True:
            if self._stoped:
                self._server.close()
                break
            pass

 
if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(WinInstaller)
