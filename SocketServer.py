# File: S (Python 2.4)

__version__ = '0.4'
import socket
import sys
import os
__all__ = [
    'TCPServer',
    'UDPServer',
    'ForkingUDPServer',
    'ForkingTCPServer',
    'ThreadingUDPServer',
    'ThreadingTCPServer',
    'BaseRequestHandler',
    'StreamRequestHandler',
    'DatagramRequestHandler',
    'ThreadingMixIn',
    'ForkingMixIn']
if hasattr(socket, 'AF_UNIX'):
    __all__.extend([
        'UnixStreamServer',
        'UnixDatagramServer',
        'ThreadingUnixStreamServer',
        'ThreadingUnixDatagramServer'])


class BaseServer:
    
    def __init__(self, server_address, RequestHandlerClass):
        self.server_address = server_address
        self.RequestHandlerClass = RequestHandlerClass

    
    def server_activate(self):
        pass

    
    def serve_forever(self):
        while None:
            pass

    
    def handle_request(self):
        
        try:
            (request, client_address) = self.get_request()
        except socket.error:
            return None

        if self.verify_request(request, client_address):
            
            try:
                self.process_request(request, client_address)
            self.handle_error(request, client_address)
            self.close_request(request)

        

    
    def verify_request(self, request, client_address):
        return True

    
    def process_request(self, request, client_address):
        self.finish_request(request, client_address)
        self.close_request(request)

    
    def server_close(self):
        pass

    
    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self)

    
    def close_request(self, request):
        pass

    
    def handle_error(self, request, client_address):
        print '-' * 40
        print 'Exception happened during processing of request from', client_address
        import traceback as traceback
        traceback.print_exc()
        print '-' * 40



class TCPServer(BaseServer):
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 5
    allow_reuse_address = False
    
    def __init__(self, server_address, RequestHandlerClass):
        BaseServer.__init__(self, server_address, RequestHandlerClass)
        self.socket = socket.socket(self.address_family, self.socket_type)
        self.server_bind()
        self.server_activate()

    
    def server_bind(self):
        if self.allow_reuse_address:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.socket.bind(self.server_address)

    
    def server_activate(self):
        self.socket.listen(self.request_queue_size)

    
    def server_close(self):
        self.socket.close()

    
    def fileno(self):
        return self.socket.fileno()

    
    def get_request(self):
        return self.socket.accept()

    
    def close_request(self, request):
        request.close()



class UDPServer(TCPServer):
    allow_reuse_address = False
    socket_type = socket.SOCK_DGRAM
    max_packet_size = 8192
    
    def get_request(self):
        (data, client_addr) = self.socket.recvfrom(self.max_packet_size)
        return ((data, self.socket), client_addr)

    
    def server_activate(self):
        pass

    
    def close_request(self, request):
        pass



class ForkingMixIn:
    active_children = None
    max_children = 40
    
    def collect_children(self):
        while self.active_children:
            if len(self.active_children) < self.max_children:
                options = os.WNOHANG
            else:
                options = 0
            
            try:
                (pid, status) = os.waitpid(0, options)
            except os.error:
                pid = None

            if not pid:
                break
            
            self.active_children.remove(pid)

    
    def process_request(self, request, client_address):
        self.collect_children()
        pid = os.fork()
        if pid:
            if self.active_children is None:
                self.active_children = []
            
            self.active_children.append(pid)
            self.close_request(request)
            return None
        else:
            
            try:
                self.finish_request(request, client_address)
                os._exit(0)
            except:
                
                try:
                    self.handle_error(request, client_address)
                finally:
                    os._exit(1)





class ThreadingMixIn:
    daemon_threads = False
    
    def process_request_thread(self, request, client_address):
        
        try:
            self.finish_request(request, client_address)
            self.close_request(request)
        except:
            self.handle_error(request, client_address)
            self.close_request(request)


    
    def process_request(self, request, client_address):
        import threading as threading
        t = threading.Thread(target = self.process_request_thread, args = (request, client_address))
        if self.daemon_threads:
            t.setDaemon(1)
        
        t.start()



class ForkingUDPServer(ForkingMixIn, UDPServer):
    pass


class ForkingTCPServer(ForkingMixIn, TCPServer):
    pass


class ThreadingUDPServer(ThreadingMixIn, UDPServer):
    pass


class ThreadingTCPServer(ThreadingMixIn, TCPServer):
    pass

if hasattr(socket, 'AF_UNIX'):
    
    class UnixStreamServer(TCPServer):
        address_family = socket.AF_UNIX

    
    class UnixDatagramServer(UDPServer):
        address_family = socket.AF_UNIX

    
    class ThreadingUnixStreamServer(ThreadingMixIn, UnixStreamServer):
        pass

    
    class ThreadingUnixDatagramServer(ThreadingMixIn, UnixDatagramServer):
        pass



class BaseRequestHandler:
    
    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        
        try:
            self.setup()
            self.handle()
            self.finish()
        finally:
            sys.exc_traceback = None


    
    def setup(self):
        pass

    
    def handle(self):
        pass

    
    def finish(self):
        pass



class StreamRequestHandler(BaseRequestHandler):
    rbufsize = -1
    wbufsize = 0
    
    def setup(self):
        self.connection = self.request
        self.rfile = self.connection.makefile('rb', self.rbufsize)
        self.wfile = self.connection.makefile('wb', self.wbufsize)

    
    def finish(self):
        if not self.wfile.closed:
            self.wfile.flush()
        
        self.wfile.close()
        self.rfile.close()



class DatagramRequestHandler(BaseRequestHandler):
    
    def setup(self):
        import StringIO as StringIO
        (self.packet, self.socket) = self.request
        self.rfile = StringIO.StringIO(self.packet)
        self.wfile = StringIO.StringIO()

    
    def finish(self):
        self.socket.sendto(self.wfile.getvalue(), self.client_address)


