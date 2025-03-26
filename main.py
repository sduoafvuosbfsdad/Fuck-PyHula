import ctypes

lib = ctypes.CDLL(
    './pyhula-1.1.4/src/pyhula/pypack/fylo/controlserver.c'
)
print(lib)