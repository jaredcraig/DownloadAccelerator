import requests
import optparse
import threading
import os

class myThread(threading.Thread):
    def __init__(self, index, url, byte_range):
        self.content = ''
        super(myThread, self).__init__()
        self.url = url
        self.byte_range = byte_range
        self.index = index
        self.content = ''

    def run(self):
        bytes = '%d-%d' % (self.byte_range[0], self.byte_range[1])
        r = requests.get(self.url, headers={'Range': 'bytes=%s' % bytes, 'Accept-Encoding': 'identity'})
        print '<thread%2d> received [%s]' % (self.index,r.headers.get('Content-Range'))
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                self.content += chunk

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
        parser = optparse.OptionParser(usage = "%prog -n <number of threads> -u <url>",
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
        try:
            if (not self.url.startswith('http')):
                self.url = 'http://' + self.url
            if (self.url.endswith('/')):
                self.url += 'index.html'
            elif (len(self.url.split('/')) == 1):
                self.url += '/index.html'

            r = requests.head(self.url)
            if (r.status_code != 200):
                raise IOError
                
            self.length = int(r.headers.get('Content-Length'))
            if (r.headers.get('Accept-Ranges') == 'bytes'):
                self.start()
            elif (r.status_code == 200):
                self.threads = 1
                self.start()
            else:
                raise IOError
        finally:
            print r.status_code, r.reason
        exit(0)

    def start(self):
        print("using (%d) threads to download '%s'" % (self.threads, self.url) )
        local_filename = self.url.split('/')[-1]
        threads = []
        chunk_size = self.length / self.threads
        start = 0
        stop = chunk_size
        for i in range(self.threads):
            if (i == self.threads - 1):
                stop = self.length
            byte_range = [start,stop]
            t = myThread(i+1, self.url, byte_range,)
            start = stop + 1
            stop += chunk_size
            threads.append(t)
            t.start()

        f = open(local_filename, 'wb')
        for thread in threads:
            thread.join()
            f.write(thread.content)
        f.close()
        print "'%s' saved [%d/%d]" % (local_filename, os.path.getsize(local_filename), self.length)

if __name__ == '__main__':
    d = DownloaderAccelerator(5, 'cs360.byu.edu/static/lectures/fall-2015/semaphores.pdf')
