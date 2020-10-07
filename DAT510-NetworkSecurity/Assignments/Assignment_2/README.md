# DAT510-1 20H Network security and vulnerability.
## Assignment 2. Implement secure communications
### Asahi Cantu Moreno (student id: 253964)
#### October 7, 2020

## Summary
For this assignment a secure communications scenario has been implemented by using simplified cryptographic primitives  emulating real-world applications.
The assignment consists of two parts:

1. **Part I. Implementation of three types of cryptographic primitives:** 
   1. Symmetric ciphers - Using Python Crypto library and implementing AES mechanism
   2. Pseudorandom generators: BBS Generator was created as a pseudorandom number generator
   3. Public-key cryptography (PKC)-based key exchange protocol.: Diffie-Hellman mechanism was implemented as well as a key exchange mechanism

   The creation of this part involves the following files:
   
   * [BBS.py](src/BBS.py) - Created a Blum Blum Shub algorithm for pseudorandom numbering generation
   * [DH.py](src/DH.py) - Diffie Hellman algorithm implementation for key-exchange
   
2. **Part II. Web Server implementation for secure messaging key exchange**. 
   

A simple secure messaging application was implemented by working with multiple clients and a server, where all clients connect. The server then redirects all communication to specific or all clients by implementing Socketio protocol.
The architecture for client and server completely changed from Assignment 1 since now Client uses a desktop application as a graphic environment for secure messaging.

   * [Server.py](src/Server.py)  Server file which works as a messenger server
   * [Client.py](src/Client.py)  Client which works as a graphic interface for secure messaging

### Technical specifications
* Language used: Python 3.8
  * Jupyter notebooks
* Packages:
  * See [requirements.txt](src/requirements.txt] for further information
  * Flask  for server side implementation
  * Socketio for communication
  * Crypto for python cryptography


## Directory structure

```bash
|   README.md                          # This readme file
|   Report.pdf                         # Technical report of this assignment commpiled in LATEX
|   Report.pptx                        # Presentation with recorded voice for this assignment
+---src
|   |   Assignment_2.ipynb             # Implementation of Encryption algorithm and messaging emulation
|   |   BBS.py                         # Blum Blum pseudo random generator algorithm
|   |   Client.py                      # GUI for secure message transmission. Implements DH and  BBS
|   |   DH.py                          # Diffie-Hallman secure key exchange implementation
|   |   requirements.txt               # Python libraries used for this project
|   |   Server.py                      # Server implementation for secure message transmission. Implements Flask and Socketio
```

## How to use
### To execute part I 
1. Navigate to the directory 'src'
2. Run the command to install all the required packages to run the code properly 
    ```bash
    pip install -r requirements.txt
    ```
3. Open [Part1.ipynb](src/Part1.ipynb) in a web browser
   1. If running from console ensure to be positioned in the 'src' directory
   2. Run the command 
   ```bash
    jupyter notebook Part1.ipynb
   ```
   3. A Jupyter notebook will be open with the necessary code too re-run the simulation
### To execute part II
1. Navigate to the directory 'src'
2. Run the command
    ```bash
    pip install -r requirements.txt
    ```
    to install all the required packages to run the code properly 
2. Execute file [Server.py](src/Server.py)
   1. ```bash
       python Server.py
       ```
1. It will mount a flask server on port 5000. There is no need to go to the server on a web browser since all the implementation happens internally and is logged in a file. The server is now listening and waiting for users to connect
   
2. Open a new terminal and execute now [Client.py](src/Client.py)
   ```bash
    python Client.py
   ```
3. A graphical application will open and will ask you to write:
   1. The server url (by default is http://localhost:500)
   2. A user name, as an example you can type 'Alice'
   3. Click on the button 'Connect'
4. The client will try to communicate with the server and let you know if the connection is successful
5. Execute again the instruction from step 2 to open a new client from a new terminal
   1. The server URL (by default is http://localhost:500)
   2. A user name, as an example you can type 'Bob'
   3. Click on the button 'Connect'
6. Once connected the server will provide the available users to chat with.
7. If using *'Alice'* Client choose to connect with 'Bob' 
8. If using *'Bob'* Client choose to connect with 'Alice'
9. Wait until communication is established and keys are generated, now chat input box and button are enabled.
10. Write any message and click on  'send' button' observe how the message travels encrypted from one client to the other encrypted
11. Observe the logs for each one of the terminals and see how the message always travels encrypted.
### **Important!**
* Make sure to close the server connection once the test is finished to unlock the port connection
* Use [Report.pdf](Report.pdf) to read the technical report
* Use [Report.pptx](Report.pptx) to view the prepared presentation
* Follow [this link]() to watch the video presentation
* [Video Presentation link](https://youtu.be/cKevoex-4h8)
