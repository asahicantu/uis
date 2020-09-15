class SDES:
    def __init__(self):
        # 10-bit Key permutation from SDES Standard
        # Emulating       3 5 2 7 4 10 1 9 8 6
        self.__key_p10 = [2,4,1,6,3,9,0,8,7,5]

        # 08-bit Key permutation from SDES Standard
        # Emulating      6 3 7 4 8 5 10 9
        self.__key_p8 = [5,2,6,3,7,4,9,8]

        # 08-bit plain text permutation from SDES Standard
        # Emulating        2 6 3 1 4 8 5 7
        self.__text_p8  = [1,5,2,0,3,7,4,6]


        # 08-bit inverse plain text  permutation from SDES Standard
        # Emulating            4 1 3 5 7 2 8 6
        self.__text_p8_inv  = [3,0,2,4,6,1,7,5]
        
        # 08-bit expansion/permutation  plain text  permutation from SDES Standard
        # Emulating           4 1 2 3 2 3 4 1
        self.__text_ep_p8  = [3,0,1,2,1,2,3,0]

        # P4 Permutation 
        # Emulating       2 4 3 1
        self.__text_p4 = [1,3,2,0]

        self.__text_size = 8


        self.__s0 = [ [1, 0, 3, 2],
                    [3, 2, 1, 0],
                    [0, 2, 1, 3],
                    [3, 1, 3, 2]]

        self.__s1 = [[0, 1, 2, 3],
                    [2, 0, 1, 3],
                    [3, 0, 1, 0],
                    [2, 1, 0, 3]]

        self.verbose = False

        
        

    @staticmethod
    def int2bin(integer, digits):
        if integer >= 0:
            return bin(integer)[2:].zfill(digits)
        else:
            return bin(2**digits + integer)[2:]

    @staticmethod
    def permute(binVal, permutator):
        return ''.join( [binVal[i] for i  in permutator ])

    @staticmethod 
    def halfSplitVal(binVal):
        binVal_len = len(binVal)//2
        val1 = binVal[0:binVal_len] 
        val2 = binVal[binVal_len:] 
        return val1, val2
    
    @staticmethod
    def circularLeftShift(binVal,bitCount):
        return binVal[bitCount:] + binVal[0:bitCount]
        
    @staticmethod
    def bin2int(binVal):
        return int(binVal,2)

    @staticmethod
    def leftShiftBits(binVal:int,n_bits = 1):
        return binVal << n_bits

    @staticmethod
    def get_smap_number(nibble,sbox):
        row = int( nibble[0] + nibble[3] ,2)
        col = int( nibble[1] + nibble[2] ,2)
        return sbox[row][col]

    @staticmethod
    def split_string(string,chunk_size):
        str_len = len(string)
        chunks = str_len//chunk_size
        retval = []
        for i in range(chunks):
            chunk = string[i*chunk_size:i*chunk_size + chunk_size]
            retval.append(chunk)
        offset = str_len % chunk_size
        if offset > 0:
            retval.append(string[-offset:])
        return retval

    @staticmethod
    def get_chunk_text_frequency(txt_list):
        chunk_dict = {}
        for item in txt_list:
            chunk_dict[item] = 1 if item not in chunk_dict else chunk_dict[item] + 1
        chunk_dict = {k: v for k, v in sorted(chunk_dict.items(), key=lambda item: item[1],reverse=True)}
        return chunk_dict

    @staticmethod
    def xor(val1,val2):
        return int(val1,2) ^ int(val2,2)

    def log(self,message):
        if self.verbose:
            print(message)

    def generate_key(self,key):
        key_size = 10
        if(len(key) > key_size ):
            raise ValueError(f"Invalid key {key}({key}), it has to be 10-bit maximum")

        permuted_key = SDES.permute(key, self.__key_p10)
        self.log(f'permuted_key:{permuted_key}')

        # Divide the permuted key in 2 chunks size 5 and then perform circular left shift 
        permuted_key_1 ,permuted_key_2 = SDES.halfSplitVal(permuted_key)
        self.log(f'split Key:{permuted_key_1}, {permuted_key_2}')

        # 1-bit Circular left shift
        permuted_key_1 = SDES.circularLeftShift(permuted_key_1,1)
        permuted_key_2 = SDES.circularLeftShift(permuted_key_2,1)

        self.log(f'Circular left shift:{permuted_key_1}, {permuted_key_2}')

        # Join again split-shift 5-bit keys
        k1 = permuted_key_1 + permuted_key_2
        self.log(f'K1:{k1}')

        # Permuting now by 8-bit key permutation
        k1 = SDES.permute(k1, self.__key_p8)        
        self.log(f'Permuted K1:{k1}')

        # 2-bit Circular left shift
        permuted_key_1 = SDES.circularLeftShift(permuted_key_1,2)
        permuted_key_2 = SDES.circularLeftShift(permuted_key_2,2)
        self.log(f'Circular left shift:{permuted_key_1}, {permuted_key_2}')

        # Join again split-shift 5-bit keys
        k2 = permuted_key_1 + permuted_key_2
        # Permuting now by 8-bit key permutation
        k2 = SDES.permute(k2, self.__key_p8)
        self.log(f'Permuted K2:{k2}')

        return k1,k2

    def f_complex(self, permuted_text, key):
        # 'l' and 'r' Stand both fro left and right most significant bits
        l , r = SDES.halfSplitVal(permuted_text)
        self.log(f'Split texts are  {l}, {r}')
        
        r_permuted = SDES.permute(r,self.__text_ep_p8)
        self.log(f'E/P permuted text is {r_permuted}')

        # Xor Function from R with K
        r_xor_k_num = SDES.xor(r_permuted,key) 
        r_xor_k = SDES.int2bin(r_xor_k_num,self.__text_size)
        self.log(f'XOR from permuted and k1 {r_permuted} {key} = {r_xor_k}')

        # Split Xor Resut by half
        r_xor_k_1,r_xor_k_2  = SDES.halfSplitVal(r_xor_k)
        self.log(f'Split by half: {r_xor_k_1} , {r_xor_k_2}')

        # Split nibble will now point to the S list
        # Coordinates in the sence of: [ a b  c  d ]
        # Where 
        # row = a d
        # col = b c       
        l_s0 = SDES.get_smap_number(r_xor_k_1,self.__s0)
        r_s1 = SDES.get_smap_number(r_xor_k_2,self.__s1)
        l_s0_bin = SDES.int2bin(l_s0,2)
        r_s1_bin = SDES.int2bin(r_s1,2)
        self.log(f'S values : {l_s0}:{l_s0_bin} , {r_s1}:{r_s1_bin}')
        s_out = l_s0_bin + r_s1_bin
        self.log(f'S out values are: {s_out}')
        #Perform final permutation for given s out value
        s_out_permuted = SDES.permute(s_out,self.__text_p4)
        self.log(f'Permuted S out is: {s_out_permuted}')
        
        s_xor_l_num = SDES.xor(s_out_permuted,l)
        s_xor_l = SDES.int2bin(s_xor_l_num,4)
        self.log(f'Xor of  {l} and {s_out_permuted} is {s_xor_l}')
        # Then swith nibble positions from placese where r goes to the first position and l to the right
        return s_xor_l, r
   
    def encrypt(self, text, key):
        #text_bin = SDES.int2bin(text,self.__text_size)
        if(len(text) > self.__text_size ):
            raise ValueError(f"Invalid text size {text}, it has to be 8-bit maximum")
        k1,k2 = self.generate_key(key)

        permuted_text = SDES.permute(text,self.__text_p8)
        self.log(f'Initial permutation of {text}: {permuted_text}')

        l,r  = self.f_complex(permuted_text,k1)
        out_val =  r + l
        self.log(f'out val 1st iteration is {out_val}')
        self.log(f'-------------')
        l,r = out_val = self.f_complex(out_val,k2)
        self.log(f'-------------')
        out_val =   l + r
        self.log(f'out val 2nd iteration is {out_val}')
        ip_inv = SDES.permute(out_val,self.__text_p8_inv)
        self.log(f'IP Inverse value is {ip_inv}')
        return ip_inv

    def decrypt(self,text,key):
        #text_bin = SDES.int2bin(ciphText,self.__text_size)
        if(len(text) > self.__text_size ):
            raise ValueError(f"Invalid text size {text}, it has to be 8-bit maximum")
        k1,k2 = self.generate_key(key)

        permuted_text = SDES.permute(text,self.__text_p8)
        self.log(f'Initial permutation of {text}: {permuted_text}')

        l,r  = self.f_complex(permuted_text,k2)
        out_val =  r + l
        self.log(f'out val 1st iteration is {out_val}')
        self.log(f'-------------')
        l,r = out_val = self.f_complex(out_val,k1)
        self.log(f'-------------')
        out_val =   l + r
        self.log(f'out val 2nd iteration is {out_val}')
        ip_inv = SDES.permute(out_val,self.__text_p8_inv)
        self.log(f'IP Inverse value is {ip_inv}')
        return ip_inv

    def encrypt3SDES(self,text,k1,k2):
        cipher = self.encrypt(text,k1)
        cipher = self.decrypt(cipher,k2)
        cipher = self.encrypt(cipher,k1)
        return cipher

    def decrypt3SDES(self,text,k1,k2):
        decipher = self.decrypt(text,k1)
        decipher = self.encrypt(decipher,k2)
        decipher = self.decrypt(decipher,k1)
        return decipher


    def crack(self,cipher):
        key = 0
        text = 0
        key_len = 2**10
        text_len = 2**8
        potential_keys = []
        while key < key_len:
            while text < text_len:
                key_str = self.int2bin(key,10)
                text_str = self.int2bin(text,8)
                p_cipher = self.encrypt(text_str,key_str)
                if p_cipher == cipher:
                   potential_keys.append(key)
                key +=1
                text +=1
        return potential_keys


