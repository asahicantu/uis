# DAT510-1 20H Network security and vulnerability.
## Assignment 3. Implement A Digital Signature Scheme
### Asahi Cantu Moreno (student id: 253964)
#### October 31, 2020

## Summary
With the implementation of encryption algorithms and key exchange mechanisms,it is important now to make use of the digital signature standards for message authen-tication  and  verification  and  implement  the  non-repudiation  principle  as  well.   Thisreport  explains  the  implementation  of  such  digital  signature  schemes  and  its  imple-mentation via python code for a chat messages application able to share public keysand verify a message or a file once it has been received.  A PKI1is implemented, whereit is assumed that there is already a trusted authority in charge of verifying that thepublic key shared from user to user is authentic and information exchange is reliable.Creation of public and private keys per user is created in an asymmetric way, whereboth users create their own public and private keys and then they share such publickeys and a signature of the given information, where it is lately hashed and verifiedagainst the original message encrypted with the public key.  The RSA2algorithm of1024 bits was implemented. 

## Implementation of a digital signaure and verifications ystem** 
   1. Asymmetric ciphers - Using Python Crypto library and implementing RSA-1024 and SHA-512 algorithms
   2. A simple secure messaging application was implemented by working with multiple clients and a server, where all clients connect. The server then redirects all communication to specific or all clients by implementing Socketio protocol. The architecture for client and server completely changed from Assignment 1 since now Client uses a desktop application as a graphic environment for secure messaging.
   
   The creation of this part involves the following files:
   
   * [DSS.py](src/DSS.py) - Created Digital Signatur Scheme for RSA key generation, message signature and verification
   * [Server.py](src/Server.py)  Server file which works as a messenger server
   * [Client.py](src/Client.py)  Client which works as a graphic interface for secure messaging

### Technical specifications
* Language used: Python 3.8
  * Packages:
  * See [requirements.txt](src/requirements.txt] for further information
  * Flask  for server side implementation
  * Socketio for communication
  * Crypto for python cryptography
  * WXPython


## Directory structure

```bash
|   README.md                          # This readme file
|   Report.pdf                         # Technical report of this assignment commpiled in LATEX
|   Report.pptx                        # Presentation with recorded voice for this assignment
+---src
|   |   DSS.py                         # Digital Signature Scheme module for key generation and message signature
|   |   Client.py                      # GUI for secure message transmission. Implements DSS
|   |   requirements.txt               # Python libraries used for this project
|   |   Server.py                      # Server implementation for secure message transmission. Implements Flask and Socketio
```

## How to use and execute
1. Navigate to the directory 'src'
2. Run the command
    ```bash
    pip install -r requirements.txt
    ```
    to install all the required packages to run the code properly 

    if for some reason 'pycryptodome' does not install or any other problem arises follow these steps:
    ```bash
         pip install pycryptodomex --no-binary :all:
         pip install --upgrade setuptools
         pip install -U wxPython
         pip install python-socketio
         pip install flask
         pip install pycryptodomex
         pip install sympy
         pip install Flask-SocketIO
    ```
   

3. Execute file [Server.py](src/Server.py)
   1. ```bash
       python Server.py
       ```
4. It will mount a flask server on port 5000. There is no need to go to the server on a web browser since all the implementation happens internally and is logged in a file. The server is now listening and waiting for users to connect
   
5. Open a new terminal and execute now [Client.py](src/Client.py)
   ```bash
    python Client.py
   ```
6. A graphical application will open and will ask you to write:
   1. The server url (by default is http://localhost:500)
   2. A user name, as an example you can type 'Alice'
   3. Click on the button 'Connect'
7. The client will try to communicate with the server and let you know if the connection is successful
8. Execute again the instruction from step 2 to open a new client from a new terminal
   1. The server URL (by default is http://localhost:500)
   2. A user name, as an example you can type 'Bob'
   3. Click on the button 'Connect'
9. Once connected the server will provide the available users to chat with.
10. If using *'Alice'* Client choose to connect with 'Bob' 
11. If using *'Bob'* Client choose to connect with 'Alice'
12. Wait until communication is established and keys are generated, now chat input box and button are enabled.
13. Write any message and click on  'send' button' observe how the message travels signed from one client to the other and be verified
14. Observe the logs for each one of the terminals and see how the message always travels encrypted.
### **Important!**
* Make sure to close the server connection once the test is finished to unlock the port connection
* Use [Report.pdf](Report.pdf) to read the technical report
* Use [Report.pptx](Report.pptx) to view the prepared presentation
* Follow [this link](https://youtu.be/cX2wv9rICms) to watch the video presentation
* [Video Presentation link](https://youtu.be/cX2wv9rICms)


 


