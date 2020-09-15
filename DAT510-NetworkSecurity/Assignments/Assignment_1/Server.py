
from flask import Flask
from flask import request
from flask import render_template
from SDES import SDES
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
__k1 = '1000101110'
__k2 = '0110101110'
        
__sdes = SDES()

def before_request():
    app.jinja_env.cache = {}

@app.route('/')
def index():
     return render_template('index.html')
    

@app.route('/encrypt',methods=['GET'])
def encrypt():
    text = request.args.get('plainText')
    text_list = __sdes.split_string(text,1)
    text_bin = [ __sdes.int2bin(ord(x),8) for x in text_list ]
    cipher = ''
    for t_b in text_bin:
        cipher += __sdes.encrypt3SDES(t_b,__k1,__k2)
    return cipher

@app.route('/decrypt',methods=['GET'])
def decrypt():
    cipher = request.args.get('cipherText')
    cipher = __sdes.split_string(cipher,8)
    text =''
    for c in cipher:
        t_b = __sdes.decrypt3SDES(c,__k1,__k2)
        text += chr(int(t_b,2))
    return text


if __name__ == '__main__':
    app.run(port=8080)