

import http.server
import subprocess

PORT = 8000

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        """Common code for GET and HEAD commands.
        This sends the response code and MIME headers.
        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.
        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        return f


def kill_zombie_sockets(port):
    try:
        done_proc = subprocess.check_output(f'lsof -i tcp:{port}', shell=True)
    except subprocess.CalledProcessError:
        return  # Only happens when there are no sockets.
    pids = set()
    lines = done_proc.splitlines()
    for line in lines[1:]:
        line = line.decode('utf-8')
        pieces = shlex.split(line)
        if len(pieces) < 2:
            continue
        pids.add(pieces[1])
    if pids:
        print('Found at least one zombie socket, killing.')
        for pid in pids:
            cmd = f'kill -9 {pid}'
            print('  ' + cmd)
            os.system(cmd)
    for pid in pids:
        print(pid)



if __name__ == "__main__":
    import os
    import socketserver



    self_dir = os.path.dirname(__file__)
    target_dir = os.path.join(self_dir, 'docs')
    os.chdir(target_dir)
    kill_zombie_sockets(PORT)
    Handler = CORSHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print(f"serving at port {PORT}")
    httpd.serve_forever()
