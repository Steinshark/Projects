from pytube import YouTube 
from pydub import AudioSegment
from pydub.utils import make_chunks
import os 
import sys 
from binascii import hexlify
from pydub.exceptions import CouldntDecodeError
import ctypes
import numpy 
from networks import AudioGenerator,AudioDiscriminator
import torch 
import binascii
import hashlib

#Inizialize directories properly
if "linux" in sys.platform:
    DOWNLOAD_PATH           = r"/media/steinshark/stor_sm/music/downloads"
    CHUNK_PATH              = r"/media/steinshark/stor_sm/music/chunked\Scale5_60s"
    DATASET_PATH            = r"/media/steinshark/stor_lg/music/dataset\Scale5_60s"
else:
    DOWNLOAD_PATH           = r"C:\data\music\downloads"
    CHUNK_PATH              = r"C:\data\music\chunked\Scale5_60s"
    DATASET_PATH            = r"C:\data\music\dataset\Scale5_60s"

MINUTES                 = 0 

#Returns a deterministic hash of a string
def hash_str(input_str:str):
    return str(hashlib.md5(input_str.encode()).hexdigest())

#Downloads 1 URL 
def download_link(url:str,output_path:str,index=None,total=None): 

    #Grab video 
    yt_handle               = YouTube(url)

    #Telemetry
    if not index is None:
        tel_msg = f"downloading {url[:50]}\t[{index}/{total}]"
    else:
        tel_msg = f"downloading {url[:50]}"
    print(tel_msg,end='')
    yt_handle.streams.filter(only_audio=True).first().download(output_path=output_path)
    print(f"\t- success")

#Convert big-endian to little-endian
def big_to_little(hex,con=True):
    little_repr = bytearray.fromhex(hex)[::-1].hex()
    return int(little_repr,base=16) if con else little_repr

#Convert little-endian to big-endian
def little_to_big(hex,con=False):
    try:
        big_repr = bytearray.fromhex(hex)[::-1].hex()
    except TypeError:
        big_repr = bytearray.fromhex(str(hex))[::-1].hex()
    return int(big_repr,base=16) if con else big_repr

#Convert a wav file to a 2-channel numpy array
def read_wav(filename,sf,outputsize):
    file_hex        = open(filename,"rb").read().rstrip().hex()
    
    file_header     = file_hex[:8]
    chunk_size      = big_to_little(file_hex[8:16])
    format          = file_hex[16:24]

    subchk1_ID      = file_hex[24:32]
    subchk1_size    = big_to_little(file_hex[32:40])
    audio_fmt       = big_to_little(file_hex[40:44])
    num_channels    = big_to_little(file_hex[44:48])
    sample_rate     = big_to_little(file_hex[48:56])
    byte_rate       = big_to_little(file_hex[56:64])
    block_align     = big_to_little(file_hex[64:68])
    bits_per_sample = big_to_little(file_hex[68:72])
    subchk2_ID      = file_hex[72:80]    
    subchk2_size    = big_to_little(file_hex[80:88])

    data            = big_to_little(file_hex[96:],con=False)


    hex_per_sample  = int(num_channels*(bits_per_sample/8)*2)
    hex_per_channel = int(hex_per_sample/2)
    n_samples       = int(subchk2_size/(num_channels* (bits_per_sample/8)))


    max_val         = pow(2,(bits_per_sample)-1)

    ch1     = [0]   *   n_samples       # Pre-allocate arrays for decoded file
    ch2     = [0]   *   n_samples       # Pre-allocate arrays for decoded file


    #Decode file by reading hex, converting from 2's complement, 
    #and adding to proper channel 
    for i,sample in enumerate(range(n_samples)):
        try:
            sample_start    = int(i * hex_per_sample)
            sample_end      = int(sample_start +  hex_per_sample)

            #Convert hex to int value
            c1 = int(data[sample_start:sample_start+hex_per_channel],base=16)
            c2 = int(data[sample_start+hex_per_channel:sample_end],base=16)

            #Convert hex to 2s complement
            if c1&0x8000:
                c1 = c1 - 0x10000
            if c2&0x8000:
                c2 = c2 - 0x10000

            ch1[i] = c1/max_val
            ch2[i] = c2/max_val

        except ValueError:

            if ((n_samples - sample) / n_samples) < .001:
                pass
            else:
                print("-\tBAD")

    #Ensure output is correct length
    count = 0 
    flag = False 
    while len(ch1) < outputsize:
        ch1.append(ch1[-1])
        ch2.append(ch2[-1])
        count += 1 
        if count > 10000 and not flag :
            print(f"bad len on {filename} - {len(ch1)-10000}/{outputsize}")
            flag = True

    if len(ch1) > outputsize:
        ch1 = ch1[:outputsize]
    if len(ch2) > outputsize:
        ch2 = ch2[:outputsize]

    #Create and save the numpy array
    arr = numpy.array([ch1,ch2],dtype=float)
    if sf > 1:
        arr = downscale(arr,sf)
    
    numpy.save(filename,arr)

#Chunks a file into 'chunk_length' millisecond-sized chunks
def chunk_file(fname:str,chunk_length:int,output_path:str): 

    #Convert fname to hash 
    fhash           = hash_str(fname)[:10]

    #Check that file has not been chunked 
    fname_check     = f"{fhash}_0.wav"
    if os.path.exists(fname_check):
        print("\tAudio has already been chunked!") 
        return 0

    #Chunk audio
    full_audio  = AudioSegment.from_file(fname,"mp4")
    chunks      = make_chunks(full_audio,chunk_length=chunk_length)

    #Save files
    for i,chunk in enumerate(chunks):
        filename    = f"{fhash}_{i}.wav"
        full_path   = os.path.join(output_path,filename)
        chunk.export(full_path,format="wav")
    
    print(f"\tsaved {i} chunks")
    return i*1000*chunk_length

#Downloads a list of files 
def download_all(filenames):

    for url in filenames:

        if "CATEGORY" in url:
            #Get category being downloaded
            cat                 = url.replace("CATEGORY","").replace("|","")
            download_out_path   = os.path.join(DOWNLOAD_PATH,cat)

            #Create path dir if it does not exist
            if not os.path.exists(download_out_path):
                os.mkdir(download_out_path)
                print(f"created path for category: {cat}")
            
        else:
            download_link(url,download_out_path)

#Chunks the audio from a given category 
def chunk_all(chunk_length:int,category:str):
    
    global MINUTES

    audio_base_path = os.path.join(DOWNLOAD_PATH,category)
    audio_out_path  = os.path.join(CHUNK_PATH,category)

    #Ensure the output path exists 
    if not os.path.exists(audio_out_path):
        os.mkdir(audio_out_path)
        print(f"created path for audio outputs: {audio_out_path}")

    #Chunk the files 
    for fname in os.listdir(audio_base_path):

        #Chunk the file 
        audio_source_path   = os.path.join(audio_base_path,fname) 
        print(f"Chunking {audio_source_path}")
        MINUTES += chunk_file(audio_source_path,1000*chunk_length,audio_out_path)
    
    print(f"added {MINUTES} to dataset")

#Convert all wav files to numpy
def read_all(category:str,sf=1,start=-1,end=-1):

    #Ensure dataset path exists 
    if not os.path.exists(DATASET_PATH):
        os.mkdir(DATASET_PATH)
    
    #build source and save paths
    audio_source_path       = os.path.join(CHUNK_PATH,category)
    audio_output_path       = os.path.join(DATASET_PATH,category)
    if not os.path.exists(audio_output_path):
        os.mkdir(audio_output_path)

    #Get chunks to convert 
    filenames   = os.listdir(audio_source_path)
    if not start == -1:
        filenames = filenames[start:end]
    total = len(filenames)
    
    #Create arrays
    for i,filename in enumerate(filenames):
        output_full_path    = os.path.join(audio_output_path,f"{hash_str(filename)[:10]}.npy")

        #Check for existing 
        print(f"Converting{output_full_path}\t{i}/{total}",end='')
        if os.path.exists(output_full_path):
            print(f"-already existed!")
            continue 
        read_wav(os.path.join(CHUNK_PATH,filename),sf=sf)
        print(f"- success")
    return 

#Convert to a 2s comlement 
def reg_to_2s_compl(val,bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val      

#Convert a numpy array to a wav file 
def reconstruct(arr_in:numpy.array,output_file:str):

    #Bring all values back up to 32000
    arr_in *= 32768
    arr_in = numpy.minimum(arr_in,32766)
    arr_in = numpy.maximum(arr_in,-32766)

    #Convert to python list 
    ch1     = list(arr_in[0])[:5291999]
    ch2     = list(arr_in[1])[:5291999]

    data    = []
    #Convert values back to 2s complement
    for c1_i,c2_i in zip(range(len(ch1)),range(len(ch2))):
        val1            = int(ch1[c1_i])
        hex_repr_2s_1   = str(binascii.hexlify(val1.to_bytes(2,byteorder='big',signed=True)))[2:-1]

        val2            = int(ch2[c2_i])
        hex_repr_2s_2   = str(binascii.hexlify(val2.to_bytes(2,byteorder='big',signed=True)))[2:-1]

        data.append(hex_repr_2s_1)
        data.append(hex_repr_2s_2)
    

    data = "".join(data)

    header  = "52494646a4ff420157415645666d7420100000000100020044ac000010b10200040010006461746180ff420100000000"


    data    = little_to_big(data)


    file = open(output_file,"wb") 
    file.write(bytes.fromhex(header))
    file.write(bytes.fromhex(str(data)))
    file.close()

#Scale a numpy array down 
def downscale(arr_in:numpy.array,sf:int):

    import time 
    ch1_split   = [arr_in[0][i*sf:(i+1)*sf] for i in range(int(len(arr_in[0])/sf))]
    ch2_split   = [arr_in[1][i*sf:(i+1)*sf] for i in range(int(len(arr_in[1])/sf))]
    
    ch1_avg     = [sum(item)/sf for item in ch1_split]
    ch2_avg     = [sum(item)/sf for item in ch2_split]
    
    arr_out     = numpy.array([ch1_avg,ch2_avg])

    return arr_out

#Scale a numpy array back up
def upscale(arr_in,sf):
    return numpy.repeat(arr_in,sf,axis=1)



if __name__ == "__main__":

    ####################################################################################    
    #                                      DOWNLOAD                                    # 
    ####################################################################################    
    links = open