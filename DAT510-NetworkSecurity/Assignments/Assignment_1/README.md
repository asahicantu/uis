# DAT510-1 20H Network security and vulnerability.
## Assignment 1. Cryptanalysis of primitive ciphers
### Asahi Cantu Moreno (student id: 253964)
#### September 15, 2020

## Summary

The study of encryption algorithms, techniques and potential vulnerability detection are very important for the understanding and detection of potential risks related to
the information transmission over insecure channels. In this assignment a study of the cryptanalysis, the statistical techniques to detect encryption algorithm vulnerabilities
and the potential threats of wrong or obsolete algorithms is performed in a two-partcode development which involves:

1. **Part I. Polyalphabetic ciphers**. Divided in two different tasks where two
ciphered text paragraphs are given to be deciphered by statistical techniques and
brute force attacks. Text was ciphered with a poly-alphabetic substitution cipher.
Techniques such as word frequency analysis and n-gram frequency analysis are
performed to start retrieving the core of the text and eventually find the potential
encryption key by knowing the initial parameters of the encryption algorithm.
For the second task another ciphered text is analyzed and several keys found by
brute-forcing and different decipher techniques which basically consist using the
same tools from the first task and special text comparison to find the optimal
encryption algorithm.
2. **Part II. Simplified DES**. The development of an SDES and triple SDES algorithm provides the insights and abilities to understand how encryption algorithms
work under real implementations. Once developed it some keys, plain text and
ciphered texts are required to be found, where also special statistical analysis is
performed to decipher ciphered messages in order to demonstrate the vulnerability of such encryption mechanism and how these techniques can be easily bypassed
by malicious third-parties. Finally the development of a mini web server is performed to analyse the potential vulnerabilities for the encryption algorithm on
the back end.


### Technical specifications
* Language used: Python 3.8
  * Jypyter notebooks
* Packages:
  * matplotlib for plots and charts
  * Flask  for server side implementation


## How to use

1. Run the command
    ```bash
    pip install -r requirements.txt
    ```
    to inistall all the required packages to run the code properly 
2. Open [Part1.ipynb](Part1.ipynb)
   1. If required run the command 
   ```bash
    jupyter notebook Part1.ipynb
   ```
   2. If required re-run the code and visualize all the results from implemented algorithms
3. Open [Part2.ipynb](Part2.ipynb)
   1. Required files:
      1. [SDES.py](SDES.py) Class implementation for SDES/3SDES algorithms
      2. [ctx1.txt](ctx1.txt) SDES ciphered string
      3. [ctx2.txt](ctx2.txt) 3SDED ciphered string
      4. Some immages available in [Assets](Assets) folder
   2. If required run the command 
   
   ```bash
    jupyter notebook Part2.ipynb
   ```
   3. If required re-run the code and visualize all the results from implemented algorithms
4. Use [Server.py](Server.py) to visualize the server implememntation
   1. Run the command
   ```bash
    python server.py
   ```

   1. It will mount a flask server on port 8080. once the command is run you can browse the code example by going to  [http://127.0.0.1:8080/ ](http://127.0.0.1:8080/)

   2. **Important!** Make sure to close the server connection once the test is finished to unlock the port connection
5. Use [Report.pdf](Report.pdf) to read the technical report
6. Use [Report.pptx](Report.pptx) to view the prepared presentation

## Directory structure

```bash
/
|   Assignment_1.pdf    # PDF version of the assignment and the tasks to be solved
|   ctx1.txt            # Ciphered binary text encrypted with SDES
|   ctx2.txt            # Ciphered binary text encrypted with 3SDES
|   Part1.ipynb         # Part 1 of given assignment (can be viewed in Assignment_1.pdf )
|   Part2.ipynb         # Part 1 of given assignment (can be viewed in Assignment_2.pdf )
|   README.md           # This readme file
|   Report.pdf          # Technical report of this assignment commpiled in LATEX
|   Report.pptx         # Presentation with recorded voice for this assignment
|   requirements.txt    # Python packages to be installed and run jupyter notebooks as well as Serve.py
|   SDES.py             # Implementation of SDES and 3SDES algorithm
|   Server.py           # Implementation of a mini web server using Flask
|
+---Assets              # Assets folder with images used for the presentation of this assignment
|       bigramfreqmatrix2.png
|       bigramfreqtop.png
|       bigramfreqtoplist.png
|       cypher_book.png
|
+---templates           # Templates folder used by Flask.
|       index.html      # Main page of mini web server showing basic functionality and description of the excercise
|
+---tex                 # Latex Folder. Is the source code where the report was developed. Report.pdf
|   |   main.tex        # Main Latex File
|   |   references.bib  # References
|   |
|   \---assets          # Images used for this report
|           3SDESCrack.png
|           3SDES_Test.png
|           bruteforce.png
|           CipherText.png
|           cryptstatistics.png
|           CryptStatisticsDict.png
|           cypher_book.png
|           SDESCrack.png
|           SDES_Test.png
|           ServerCrypt.png
|           ServerDecrypt.png
|           ServerIndex.png
|           timeconsumption.png
|
```
