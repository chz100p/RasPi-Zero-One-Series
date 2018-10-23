#!/usr/bin/env python3
#coding: utf-8
#
# ファイル名：3_2adrszIRS-sample.py  python3用
# バージョン：2018/7/27 v1.0
#
# ビット・トレード・ワン社提供の 赤外線リモコン基板(型番：ADRSZIRS)用のツール
#　著作権者:(C) 2015 ビット・トレード・ワン社
#　ライセンス: ADL(Assembly Desk License)
#  実行方法：読込　./3_2adrszIRS-sample.py r
#　　　　　　書込　./3_2adrszIRS-sample.py w　5B0018002E001800
#　******使い方：コマンドライン　ツール
#学習リモコン→ラズパイ　読込コマンド（r:)：、 応答：データ
#　
#学習リモコン←ラズパイ　書込コマンド（w:)：、データ
#
#sample-data：ソニー	デジタルテレビ１	電源
#5B0018002E001800180018002E001800170018002E00190017001800170018002E00180018001800170018001700180017004F03

#
#　******Ｉ２Ｃ関係内部コマンド
#  cmd  R1_log_start       0x15  bus-write(ADR,cmd,n)
#  cmd  R2_log_stop        0x25  bus-write(ADR,cmd,n)
#  cmd  R3_data_num_read   0x35  bus-read(ADR,cmd,n)
#  cmd  R4_data_read       0x45  bus-read(ADR,cmd,n)
#  cmd  W1_data_num_write  0x19  bus-write(ADR,cmd,n)
#  cmd  W2_data_write      0x29  bus-read(ADR,cmd,n)
#  cmd  W3_trans_req       0x39  bus-read(ADR,cmd,n)
#
#

import smbus
from time import sleep

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This must match in the Arduino Sketch
#SLAVE_ADDRESS = 0x04 0x5a
#SLAVE_ADDRESS = 0x52

SLAVE_ADDRESS  =  0x5a
data_numH      =  0x31
data_numL      =  0x32
data_numHL     =  [0x00,0x31,0x32]
data_num       =  10
memo_no        =  0
block          =  []

#command
R1_log_start       =  0x15  #bus-write(ADR,cmd,n)
R2_log_stop        =  0x25  #bus-write(ADR,cmd,n)
R3_data_num_read   =  0x35  #bus-read(ADR,cmd,n)
R4_data_read       =  0x45  #bus-read(ADR,cmd,n)
W1_data_num_write  =  0x19  #bus-write(ADR,cmd,n)
W2_data_write      =  0x29  #bus-read(ADR,cmd,n)
W3_trans_req       =  0x39  #bus-read(ADR,cmd,n)


############# read command
def read_command():
    #print('start_read_command')
    bus.write_byte(SLAVE_ADDRESS, R1_log_start)
    sleep(5.0)
    bus.write_byte(SLAVE_ADDRESS, R2_log_stop)
    data_numHL = bus.read_i2c_block_data(SLAVE_ADDRESS, R3_data_num_read ,3)
    data_num = data_numHL[1]
    data_num *= 256
    data_num += data_numHL[2]
    print("data_num =",data_num)
    if data_num < 65535:
        #print("data_num =",data_num)
        block = []
        block_dat  = bus.read_i2c_block_data(SLAVE_ADDRESS, R4_data_read , 1)
        for i in range(data_num):
            block_dat  = bus.read_i2c_block_data(SLAVE_ADDRESS, R4_data_read , 4)
            block.append(block_dat[0])
            block.append(block_dat[1])
            block.append(block_dat[2])
            block.append(block_dat[3])
    #print(block)  #for denug
    else:
        print("data_num error=",data_num)
    
    return block

################# write command
def write_command(block2):
    #print('start_write_command')
    str_tmp = ""
    int_tmp = []
    for i in range(int(len(block2)/2)):
        str_tmp = block2[i*2] + block2[i*2+1]
        int_tmp.append( int(str_tmp, 16))
    print(int_tmp)
    print(len(int_tmp))
    data_num = int(len(int_tmp)/4)  #for test
    data_numHL = [0x31,0x32] #for test
    data_numHL[0] = int(data_num/256)
    data_numHL[1] = int(data_num%256)
    print(data_numHL ,data_numHL[0] ,data_numHL[1])
    bus.write_i2c_block_data(SLAVE_ADDRESS, W1_data_num_write ,  data_numHL)
    print(data_num)
    data_numHL = [0x31,0x32,0x33,0x34] #for test
    for i in range(data_num):
         data_numHL[0] = int_tmp[i*4+0]
         data_numHL[1] = int_tmp[i*4+1]
         data_numHL[2] = int_tmp[i*4+2]
         data_numHL[3] = int_tmp[i*4+3]
         bus.write_i2c_block_data(SLAVE_ADDRESS, W2_data_write , data_numHL)
    bus.write_byte(SLAVE_ADDRESS, W3_trans_req)


###########################   main

def command_read(args):
    res_data = read_command()
    for i in range(len(res_data)):
        print('{:02X}'.format(res_data[i]), end="")
    print()

def command_write(args):
    block2 = args.data
    write_command(block2)

import argparse

parser = argparse.ArgumentParser(description="ビット・トレード・ワン社提供の 赤外線リモコン基板(型番：ADRSZIRS)用のツール")
subparsers = parser.add_subparsers(dest='command')
subparsers.required = True # kludge

parser_read = subparsers.add_parser('read', aliases=['r'], help="学習リモコン→ラズパイ")
parser_read.set_defaults(func=command_read)

parser_write = subparsers.add_parser('write', aliases=['w'], help="学習リモコン←ラズパイ")
parser_write.set_defaults(func=command_write)
parser_write.add_argument('data', help='書込データ')

args = parser.parse_args()
args.func(args)
