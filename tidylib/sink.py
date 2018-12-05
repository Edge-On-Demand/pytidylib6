import ctypes
import sys
import threading
import platform


try:
    from cStringIO import StringIO
except ImportError:
    try:
        from StringIO import StringIO 
    except ImportError:
        from io import StringIO

__all__ = ['Sink', 'create_sink', 'destroy_sink']

#----------------------------------------------------------------------------#
# Globals

sinks = {} # of int: Sink
last_sink_id = 0
sink_id_lock = threading.Lock()

#----------------------------------------------------------------------------#
# ctypes type definitions

# Fix for Windows b/c tidy uses stdcall on Windows
if "Windows" == platform.system():
    functype = ctypes.WINFUNCTYPE
else:
    functype = ctypes.CFUNCTYPE

PutByteType = functype(None, ctypes.c_int, ctypes.c_char)


class TidyOutputSink(ctypes.Structure):
    """ Mirrors the _TidyOutputSink structure in tidy.h """
    _fields_ = [
        ('sinkData', ctypes.c_void_p),
        ('putByte', PutByteType)
        ]
        
#----------------------------------------------------------------------------#
# Python interface


class Sink(object):
    """ Represent a buffer to which Tidy writes errors with a callback function """
    def __init__(self, sink_id):
        self.data = StringIO()
        self.sink_id = sink_id
        self.struct = TidyOutputSink()
        self.struct.sinkData = ctypes.cast(
            ctypes.pointer(ctypes.c_int(sink_id)), ctypes.c_void_p)  # Windows fix
        write_func = self.data.write  # Avoid 2 attr accesses per byte

        def put_byte(sink_id, byte):
            # We don't need sink_id because we have a separate put_byte
            # function for each sink
            write_func(byte.decode('utf-8'))
        self.struct.putByte = PutByteType(put_byte)
        self._as_parameter_ = ctypes.byref(self.struct)
    
    def __str__(self):
        return self.data.getvalue()


def create_sink():
    """ Return a new Sink with a numeric ID incremented in a threadsafe way """
    global last_sink_id, sink_id_lock, sinks
    sink_id_lock.acquire()
    try:
        this_sink_id = last_sink_id
        last_sink_id = (last_sink_id + 1) % sys.maxsize
        # If you have more than maxint sinks open at a time, you're screwed
    finally:
        sink_id_lock.release()
    sink = Sink(this_sink_id)
    sinks[this_sink_id] = sink
    return sink


def destroy_sink(sink):
    """ Free a Sink object by eliminating the reference from the global map """
    global sinks
    del sinks[sink.sink_id]
    del sink
#----------------------------------------------------------------------------#
