#Lab: Download Accelerator

virtualenv env
source env/bin/activate
pip install requests


In this assignment, you will create an HTTP downloader that can download a file in parallel using a number of concurrent number of threads. You will use Python for this assignment.

The goals of this assignment are (1) to gain additional familiarity with using Python for writing networking code, and (2) to learn how to use threading in Python.
Downloader

The downloader uses the following command line syntax:

downloadAccelerator.py [-n threads] url

On starting, the downloader first sends a HEAD request to the web server specified in the URL, to determine the size of the object. If the object has a valid Content-Length field, it then downloads the object in parallel, using the specified number of threads. Each thread sends a GET request with a Range header that gives the range of bytes desired. For example, to get the first 100 bytes of a file:

Range: bytes=0-100

Be sure the GET request also requests the identity encoding:

Accept-Encoding: identity

so that it doesn't get a compressed response.

Range requests only work on static pages. You should use the CS 360 web pages as an example, including lecture notes for larger files. If you do not receive a 206 status code in the response, then you are working with a web page that does not support content ranges. In addition, the response should have a Content-Range header indicating the byte range of the response.

The downloader saves the file in the current directory, using the same name as given in the URL. If the URL ends with "/", then the name "index.html" is implied.

The downloader also reports, to standard output, the following:

[URL] [threads] [bytes] [seconds]

where [URL] is the URL given on the command line, [bytes] is the number of total bytes in the object, and [seconds] is a floating point number indicating the time taken to download the object, starting from when the threads are created and ending when the last thread finishes.

To verify that you downloaded the file correctly, use wget to download the file into a separate directory, and then diff to verify the files are the same.
Final Testing

Before running tests on these files, be sure your code is working. These files are hosted by the federal government, and we don't want to overload their systems.

Verify your code is working correctly using the CS 360 web site, including large files such as lecture notes. Once you verify that a diff of the original file and your downloaded file indicates they are the same, then proceed with these tests.

Download the small, medium, and large census files from the federal govenrment. These files are approximately 1 MB, 10 MB, and 100 MB. Use the diff program to verify that your downloaded files are exactly the same as the original file.
Submission

Create a tgz of your program directory. For example, if your code is in the directory called download-accelerator, then you would type this:

tar -czvf download-accelerator.tgz download-accelerator

Submit your tgz file using learningsuite.byu.edu.
Code Review

About a week after the labs are due, each student will email their code to two other students in the class. The TAs will publish a document showing who to email your code to. You will then run tests on your own code as well as the code from other students, using the code review sheet. Please print these sheets so that everyone has a consistent form. Turn in a printed code review sheet for both your code and their code. This will give you an opportunity to see how someone else's code works and to learn from how they have written their code.
Grading

Your lab will be tested as specified in the grading sheet. If you wish to receive help with your code, then you should print out clear and concise debugging information when the debugging flag (-d) is given on the command line. The more helpful and clear your debugging information is, the better your chances for getting useful help. You should apply this same standard to how you document your code.
