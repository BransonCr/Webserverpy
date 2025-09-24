# Assignment 3: Building a Simple Web Server
**Detailed Overview and Rubric**

In this assignment, you will have to opportunity to practice implementing a Layer 5 network protocol.  Use will use the HTTP protocol to build a simple web server in Python 3.  A skeleton has already been developed for you that allows the client (a web browser) to establish a socket connection to your server.  The program is written using Python 3, which is what you will use for the development.  Your job will to be able to process the incoming stream of bytes from the socket and perform the correct operations depending on the type of request.  You will need to use Telnet, Wireshark and a web browser to interact with your web server and analyze the traffic to it.  

# Details

| **Item**            | **Criteria** |
|----------------|---------------|
|**Assignment:** |	Work will be done individually
|**Assignment Submissions:** |	All submissions will be done via GitHub Classroom.|
|**Due Date:**	| Electronic submission Oct 5th, 2025  – end of day (23:59). You will need to commit your code to your local repository for the assignment and push it upstream to GitHub Classroom by this time.  Your code will be tested against an automated process for the validity of the correct responses as well as the correct document type, contents and length (and any supporting header fields).  Consider the minimum number of header field required for each operation.| 


To start with, you will need to ensure that the web server is working correctly.  Normally, a web server will run on port 80 but we will be running it on a different port from the ephemeral port range (between 1024 and 65535).  This port number is provided as an argument when launching the script.  If I was to run the server on port 6789, I would use the following syntax:

`python3 webserver.py -p 6789`

You will need to run the script from the command line (terminal) from inside your repository folder.  Please do not move it from this location.  If everything is good, you will see the following message:

`Server is running on port  6789`

`The server is ready to receive data....`

**You will need to be careful with your port selection as there are numerous things that can cause problems.**  On some OS's, if you use a port number from the well-known range, there will be issues and the program may halt.  Alternately, if the port is already bound (in use) it will through generate an exception, so you can try running it on another port.  You may also have issues with the windows firewall so please ensure you are able to connect.  

To check if you basic web server framework is working, open up a web browsers and in the url enter:

`http://localhost:6789`

**The value after the colon in the url is the port number you used to setup the server.  In this example, I am running on port 6789, but if I was using port 7000 during the setup, the url would be http://localhost:7000.**

The framework reads in a stream on bytes from the inbound port and it is up to you to process them correctly to handle the operations listed before.  You will need to correctly process and respond to the HTTP requests that come in from a browser.  

**To test your server:**

Your server can be tested in a number of different ways.  Firstly, open up a web browser and see what happens when you request resources (Wireshark is handy here to capture traffic here and understand what is going on).   You can also use Telnet to open up a connection to the localhost at the correct port and manually enter your requests.  

The framework has be setup to generate a 404 page with some basic html.  You should see this page and regardless of the resource you ask for (initially), you will always get a 404 initially.  It will be your job to add the additional functionality.  You will need to inspect the code to understand what the components are doing.  You will find some helpful hints in the programming section of chapter 2.  **In reality, Python offers some packages that will handle all of your HTTP requests for you but you are not permitted to use them for this assignment.  You will need to analyze and build your responses based on the raw stream of bytes and construct the proper responses in a byte-oriented fashion.  Utilizing a library that is intended to support HTTP processing will result in a mark of 0.**  You might find it handy to use regular expressions to handle the input processing as well as using libraries for raw file handling and OS operations (I've imported them in the skeleton, so you might want to have a look at what they can do for managing certain operations).  **A series of test files have been included for you to use.  Please use these for your testing and do not move them as they will used in the final evaluation of your web server.  Do not change the location of these key files, but you are welcome to add other files.**

While there are multiple methods supported by HTTP, **you will implement only the GET method for HTTP 1.1 in a minimal fashion.**  The client will generate different get requests and you will need to interpret and generate the correctly formatted response.  Things to be careful of is the number of spaces, carriage returns and line feed as they matter!  **You will need to consult the RFC for HTTP for details (https://tools.ietf.org/html/rfc7231).  Consider if things are case sensitive (for URLs, the shouldn't be).**

**In your responses, you will need to (at a minimum) provide information regarding the type of the resource, the size of the resources, in addition to information regarding your server (name your server something nice) as well as the requested resource in the proper format.   You will also need to have information regarding the date (check the requirements in the RFC - section 7.1.1.2.).**

**Here are the different items that need to be handled:**

**1.Returning the basic html page:** There server needs to handle a basic request for an HTML  file.  If a user enters a request as http://localhost:6789/index.html, the server will need to check that the file exists on the path (the path is relative to the location of the server and return the file with the correct response codes.  If it is not there, return the Not Found error code and necessarily details).

**2.Return a nested html page:**  Same as above, but be able to return an arbitrarily nested resource such as http://localhost:6789/nested/index.html

**3.Handle the case for default index.html requests:**  If a client requests only http://localhost:6789 or http://localhost:6789/, the server should look for and return index.html from the path. 

**4.Requests for HTM and HTML:** the server needs to handle both requests for HTM and HTML file.

**5.Path and files without extensions:**  If the client submits a request for http://localhost:6789/test it should automatically check for test.html but it the requests for
http://localhost:6789/test/, it will return the index.html file within the test sub-folder (processed as http://localhost:6789/test/index.html).  Files without an extension will be assumed to be of the type .html or .htm.  If the file does not exist, it must return a file not found response. 

**6.Requests for non-binary objects:** If the client requests a .css, .js, .json it should return the correct resources (headers + file).  Remember that these are all text-based objects.

**7. Requests for binary objects:** If the client requests a .png, .jpg, .jpeg, .gif, .ico, .pdf . it should return the correct resources (header + file).  Remember that these are all binary objects.

**8. Media formats:** If any other media format is requested (other that what is covered items 4, 6 & 7), the server needs to response with an unsupported media type response (Check RFC for this: 6.5.13).  Thus if you request an xml document (which is unsupported on the server) as http://localhost:6789/bob.xml, it will respond with the corresponding error code, regardless of if the file exists or not.  

**9. Unsupported Requests:** If any other request method is used 'POST', 'HEAD', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', or 'TRACE' the server will respond with a method not allowed response (Check RFC for this: 6.5.5).  This response MUST add an additional field in the header that lists to the client making the request, the allowable methods.  In the case of your server, it will only allow the GET method.

**10. BONUS:** Allow server to support conditional gets.  Normally a client would not make a conditional get request, unless it was a proxy server.  For the bonus, implement the server side support of the conditional get.   To test this, you will need to use Telnet to connect to your local server and manually build the GET request with the appropriate fields.  Recall that the conditional get will return the file requested if the file is newer than the date in the request otherwise the server will respond with a Not Modified response. 

The following items will be tested (these files are included in the src folder - port number is up to you to set, but if you leave it empty this is what it will default to):

| **URL Request**  | **Expected Behaviour** |
|-------------------------------------|:-------------:|
| http://localhost:6789 	|		-> should return index.html |
| http://localhost:6789/	|		-> should return index.html |
| http://localhost:6789/index.html |	-> should return index.html |
| http://localhost:6789/zelda.png |		-> should return zelda.png and be viewable in browser |
| http://localhost:6789/zelda.jpg	|	-> should return zelda.jpg and be viewable in browser |
| http://localhost:6789/zelda.gif	|	-> should return zelda.gif and be viewable in browser | 
| http://localhost:6789/zelda.png	|	-> should return zelda.png and be viewable in browser |
| http://localhost:6789/test.css	|	-> should return test.css and the css is viewable in browser |
| http://localhost:6789/test.json |		-> should return test.json and the css is viewable in browser |
| http://localhost:6789/test.js	|	-> should return test.js and the js is viewable in browser |
| http://localhost:6789/sample.pdf |	-> should return sample.pdf and the browser should download or display in new tab. |
| http://localhost:6789/test	|	-> should return text.html, which is a page styled with test.css and has an external image |
| http://localhost:6789/nested 	|	-> should return nested.html |
| http://localhost:6789/nested/ 	|	-> should return nested/index.html |
| http://localhost:6789/nested/css |	-> should return nested/css.html, which is a page styled with an embedded style sheet and image |
| http://localhost:6789/test.xml |		-> should return that this media format is unsupported |
| http://localhost:6789/robertPaulson|	 -> should return that this file is not found |
| A 'POST', 'HEAD', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', or 'TRACE' | -> should return that these methods are not allowed (you will need to figure out how to test this). |

If the basic functionally of the server is working, you should be able to view http://localhost:6789/index.html which has some text, a picture of zelda, a button that when you click it presents a JavaScript alert message box that says "My Javascript works!"

**Rubric:** The assignment will be marked as follows:

| **Rubric** | **Max Score** | **Value** |
|-------------------------------------|:-------------:|:----------:|
|Basic HTML response (item 1)|	/2 |	|
|Nested HTML response (item 2)| /2 |	| 
|Default request file (item 3)|	/2 |	|
|HTM/HTML files (item 4) |	/2 |	|
|Path and files without extensions (item 5) | /4 |	|
|Serve required text based files (item 6) | /2 |	|
|Serve required binary files (item 7) | /2 |	|
|Unsupported media (item 8) | /2 |	|
|Unsupported methods (item 9)| /3|	|
|Invalid files | /1 |	|
|Bonus (item 10) | /2 |	|		
|-------------------------------------|---------------|------------|
|Total	| /22 |	 |
|-------------------------------------|---------------|------------|

**Total possible marks 24/22**

**Note:**  It is critical that the protocol is strictly adhered to.  This means that your responses must be well-formed to be valid.  Malformed responses will be considered invalid and points will not be awarded (tests will fail). 

**TIPS:**  Start with the basic operations and test as you go.   Using the skeleton provided, this surprisingly can be done with a minimum amount of code.   The final solution (which is inefficiently coded with this skeleton is less that 200 lines of code (including bonus item). 

**TIPS:**  If you add additional package, you will need to update your requirements.txt otherwise testing might fail. 

**TIPS:**  If your server crashes as some point, and you need to restart, you may have to change to a different port number.  Your server should keep running between requests.  

**TIPS:** A REGEX (regular express processor) may be handy here :)

**TIPS:** Please review the comments in the code. 
