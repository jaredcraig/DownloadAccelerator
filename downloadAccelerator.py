import optparse
import sys
import httplib
import threading

class myThread(threading.Thread):
    def __init__(self, index, url, byte_range):
        self.content = ''
        super(myThread, self).__init__()
        self.url = url
        self.byte_range = byte_range
        self.index = index
        
    def run(self):
        host = self.url.split('/')[0]
        path = self.url[len(host):]
        conn = httplib.HTTPConnection(host)
        
        bytes = 'bytes=%d-%d' % (self.byte_range[0],self.byte_range[1])
        conn.request("GET", path, headers={'Range': bytes})
        resp = conn.getresponse()
        status = resp.status
        self.content = resp.read()
        print '<thread%2d> received %s' % (self.index,resp.getheader('content-range'))

class DownloaderAccelerator:
    def __init__(self, threads, url):
        self.port = 8000
        self.length = 0
        self.threads = threads
        self.url = url
        self.time = 0.0
        self.parse_options()
        self.run()

    def parse_options(self):
        parser = optparse.OptionParser(usage = "%prog [options]",
                                       version = "%prog 0.1")

        parser.add_option("-n","--threads",type="int",dest="threads",
                          default=5,
                          help="number of threads")

        parser.add_option("-u","--url",type="string",dest="url",
                          default="cs360.byu.edu/static/lectures/fall-2015/semaphores.pdf",
                          help="the url")

        (options,args) = parser.parse_args()
        self.threads = options.threads
        self.url = options.url

    def run(self):
        print("using (%d) threads to download '%s'" % (self.threads, self.url) )
        try:
            if (self.url.startswith('http')):
                self.url = self.url[7:]
            urlList = self.url.split('/')
            host = urlList[0]
            path = self.url[len(host):]
            if (len(path) == 0):
                path = '/index.html'
            conn = httplib.HTTPConnection(host)
            bytes = 'bytes=%d-%d' % (0, 299)
            conn.request("GET", path, headers={'Range': bytes, 'Accept-Encoding': 'identity'})
            resp = conn.getresponse()
            print resp.status, resp.reason
            self.length = resp.getheader('content-length')
            print resp.getheaders()
            if (self.length <= 0):
                raise IOError
            if resp.status == 206:
                self.start()
            elif resp.status == 200:
                self.download()
            else:
                print 'An error occurred: ',resp.status, resp.reason
        except:
            print 'error handling request'
            exit(0)

    def download(self):
        local_filename = ''
        url_list = self.url.split('/')
        host = url_list[0]
        path = self.url[len(host):]
        conn = httplib.HTTPConnection(host)

        if (len(url_list) == 1 or not url_list[-1]):
            local_filename = 'index.html'
            path == '/index.html'
        else:
            local_filename = url_list[-1]
        f = open(local_filename, 'wb')
        bytes = 'bytes=%d-%d' % (0, 299)
        conn.request("GET", path, headers={'Range': bytes, 'Accept-Encoding': 'identity'})
        resp = conn.getresponse()
        print resp.status, resp.reason
        print resp.getheaders()
        f.write(resp.read())
        f.close()
        
    def start(self):
        local_filename = self.url.split('/')[-1]
        threads = []
        chunk_size = self.length / self.threads
        start = 0
        stop = chunk_size
        print local_filename
        for i in range(self.threads):
            if (i == self.threads - 1):
                stop = self.length
            byte_range = [start,stop]
            t = myThread(i+1, self.url,byte_range,)
            start = stop + 1
            stop += chunk_size
            threads.append(t)
            t.start()

        f = open(local_filename, 'wb')
        for thread in threads:
            thread.join()
            f.write(thread.content)
        f.close()
        return local_filename

if __name__ == '__main__':
    d = DownloaderAccelerator(1, "http://www2.census.gov/geo/tiger/TIGER2013/TRACT/tl_2013_10_tract.zip")
