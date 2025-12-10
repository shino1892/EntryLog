from ctypes import *
from config import LIBPAFE_PATH

FELICA_POLLING_ANY = 0xffff

def get_felica_idm():
    libpafe = cdll.LoadLibrary(LIBPAFE_PATH)

    libpafe.pasori_open.restype = c_void_p
    pasori = libpafe.pasori_open()

    libpafe.pasori_init(pasori)

    libpafe.felica_polling.restype = c_void_p
    felica = libpafe.felica_polling(pasori, FELICA_POLLING_ANY, 0, 0)

    idm = c_ulonglong()
    libpafe.felica_get_idm.restype = c_void_p
    libpafe.felica_get_idm(felica, byref(idm))

    libpafe.free(felica)
    libpafe.pasori_close(pasori)

    return "%016X" % idm.value
