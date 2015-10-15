import optparse
import sys
import httplib
import threading

class DownloaderAccelerator:
    def __init__(self, threads, url):
        self.port = 8000
        self.range = 0
        self.length = 0
        self.threads = threads
        self.url = url
        self.rmin = 0
        self.time = 0.0
        self.rmax = 1024
        self.host = ''
        self.path = ''
        self.finished = False
        self.lock = threading.Lock()
        self.parse_options()
        self.run()

    def parse_options(self):
        parser = optparse.OptionParser(usage = "%prog [options]",
                                       version = "%prog 0.1")

        parser.add_option("-t","--threads",type="int",dest="threads",
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
            host = self.url.split('/')[0]
            path = self.url[len(host):]
            conn = httplib.HTTPConnection(host)
            conn.request("HEAD", path);
            resp = conn.getresponse()
            self.length = int(resp.getheader('content-length'))
            
            if (self.length <= 0):
                raise IOError
            self.start()

        except:
            print "HTTP ERROR!"
            exit(0)

    def start(self):
        local_filename = self.url.split('/')[-1]
        print '%s(%d) bytes' % (local_filename, self.length)
        f = open(local_filename, 'wb')
        self.startThreads(f)
        print 'url:%s threads:%d size:%d time:%f' % (self.url,self.threads,self.length,self.time)
        f.close()
        return local_filename

    def startThreads(self, f):
        threads = []
        for i in range(self.threads):
            t = threading.Thread(target = self.download, args=(i+1, f,))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join(60)
            if thread.isAlive():
                print "Waited too long ... aborting"
                return

    def download(self, i, f):
        host = self.url.split('/')[0]
        path = self.url[len(host):]
        while (True):
            self.lock.acquire()
            if (self.rmax >= self.length):
                if (self.finished):
                    self.lock.release()
                    break
                self.finished = True

            bytes = 'bytes=%d-%d' % (self.rmin, self.rmax)
            conn = httplib.HTTPConnection(host)
            conn.request("GET", '/', headers={'Range': 'bytes=0-299'})
            resp = conn.getresponse()
            print resp.status
            print 'downloading range %d-%d out of %d total bytes' %(self.rmin,self.rmax,self.length)
            print 'thread %d\treceived %s bytes' % (i,ls
            r.headers.get('Content-Length'))
            self.lock.release()
            break

            if (r.status_code == 200):
                self.rmax = self.length
                finished = True
            if r.content:
                f.write(r.content)

            if (self.rmax + 1024 <= self.length):
                self.rmin = self.rmax + 1
                self.rmax += 1024
            else:
                self.rmin = self.rmax + 1
                self.rmax = self.length

            self.lock.release()

if __name__ == '__main__':
    d = DownloaderAccelerator(1, "http://www2.census.gov/geo/tiger/TIGER2013/TRACT/tl_2013_10_tract.zip")
