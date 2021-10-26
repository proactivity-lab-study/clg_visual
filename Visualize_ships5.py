# -*- coding: utf-8 -*-

import csv
from pylab import arange, plt
#from drawnow import drawnow

import ast

#import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt1 
import matplotlib.animation as animation1


import serial
import datetime
import traceback
import binascii
from struct import *
import time
import math

import re

import os
import base64
import cStringIO
import datetime
import json
import os
import Queue
import socket
import subprocess
import sys
import thread
import threading
import time
import traceback
import urllib2
import numpy as np

LOG_FILE      = "plotting.log" # Log file name, or None for no file logging
DO_VERBOSE = False

crane_file_name = "../logs_folder/log_tttw11_mote_01_1.2.log"


ship1_file_name = "../logs_folder/log_tttw11_mote_01_1.1.log"
ship2_file_name = "../logs_folder/log_tttw19_mote_19_2.1.log"
ship3_file_name = "../logs_folder/log_tttw19_mote_19_2.2.log"

last_line = "Cargo loading game"


X = 2
X = 4

xxx=list()
yyy=list()

plt.ion() #turn on interactive plotting
min_x = 0
max_x = 40

figure, ax = plt.subplots() 
t1, t2, t3, t4, t5, t6, crane_hit = ax.plot([],[], 'bo', [],[], 'go', [],[], 'ro', \
                                 [],[], 'co', [],[], 'mo', [],[], 'yo', [],[], 'bs')


t11 = ax.text(50, 3, ' ', fontsize=16)
t12 = ax.text(50, 6, ' ', fontsize=16)
t13 = ax.text(50, 9, ' ', fontsize=16)
t14 = ax.text(50, 12, ' ', fontsize=16)
t15 = ax.text(50, 15, ' ', fontsize=16)

Cargo_Text = ax.text(50, 50, ' ', fontsize=12) 
                                
                          
ax.set_xlim(-10, 60)
ax.set_ylim(-10, 60)
#Other stuff
ax.grid()

list_of_ships = []

crane_pos_x = 0
crane_pos_y = 0
cargo_placed = 0
crane_above_ship = 0
ships = {} # 
ship_times = {}
data = []
global_time = 0
ship_time = 0

def makeFig():
    plt.scatter(xxx,yyy) # 
    

def plotti(a, b, id, crane_above_ship):

    #xxx.append(a)
    #yyy.append(b) # 
    #drawnow(makeFig) 
    
    if id == 1:
        t1.set_xdata(a)
        t1.set_ydata(b)
        if crane_above_ship:
            #ax.text(a + 1, b + 1, r'$Cargo$', fontsize=12)
            Cargo_Text.set_text(r'$' + 'Cargo' + '$')
            #print a+1,b+1
            Cargo_Text.set_position((a+1,b+1))
        #else:
         #   Cargo_Text.set_text(r'$' + ' ' + '$')
    elif id == 2:
        t2.set_xdata(a)
        t2.set_ydata(b)
    elif id == 3:
        t3.set_xdata(a)
        t3.set_ydata(b)
    elif id == 4:
        t4.set_xdata(a)
        t4.set_ydata(b)
    elif id == 5:
        t5.set_xdata(a)
        t5.set_ydata(b)
    else:
        t6.set_xdata(a)
        t6.set_ydata(b)
    
      
    #Need both of these in order to rescale
    ax.relim()
    ax.autoscale_view()
    #We need to draw *and* flush
    figure.canvas.draw()
    figure.canvas.flush_events()


class gps_pos (object):
    def __init__(self, x, y, *args):
        self.x = x
        self.y = y
    def __repr__(self):
        return "%s.%s(%s, %s)" % (__name__, self.__class__.__name__, self.x, self.y)


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))


def extract_data_from_incoming_packet(k, group):

        print "start of extracting data "
        
        id = unpack("bbb", group)[0]
        pos_x = unpack("bbb", group)[1]
        pos_y = unpack("bbb", group)[2]
        
        print id, pos_x, pos_y

        #group_seq = group[1:]
        #sequence_numbers[k] = unpack("Ibbbbbbbb", group_seq)[0]
        #group_time = group[9:]
        #timestamp = unpack("I", group_time)[0]
                       
 
        aeg_millis = TimestampMillisec64()
        local_time_in_mill = aeg_millis - (aeg_millis/100000000)*100000000
        #if len(timestamps) > 0:
        #    print "id: " + str(unpack("bbbbbbbbbbbbb", group)[0]) + " time from last sensor reading:  " + str(timestamp - timestamps[len(timestamps) - 1])
        #timestamps[str(k)] = str(timestamp)


def TimestampMillisec64():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


def get_line_number(phrase, lines):
    #with open(file_name) as f:
    for i in range(1,20):
        #print "prhaze before comparison is:" + str(phrase)
        if phrase == lines[-i]:

            #print "FOUND phraze inside the loooooooooooop index is: " + str(i)
            return i
    return 1

            #print "inside the loooooooooooooop phrase is: " + str(lines[-i])
            #print "index is:" + str(i)
            
    


class FileReaderClient():
    def __init__(self, crane_file_name, ship2_file_name, ship1_file_name, ship3_file_name):
        self.is_running = False
        self._cached_stamp_cfn1 = 0
        self._cached_stamp_sfn1 = 0
        self.cfn1 = crane_file_name   
        self.sfn1 = ship1_file_name 
        self.sfn2 = ship2_file_name 
        self.sfn3 = ship3_file_name 
        #try:
        #    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #    sock.connect((self.ip, self.port))
        #    self.sock = sock
        #except Exception as e:
        #    log("Network error connecting to %s:%s (%s). Will try to reconnect.", self.ip, self.port, e) 

    def run(self):
        self.is_running = True
        global crane_pos_y
        global crane_pos_x
        global cargo_placed


        print "def run has started"
        f = open(self.cfn1, "r")
        lines = f.read().splitlines()
        f.close()
        last_line = lines[-1]
        
        while True:
            try:
                plotti(crane_pos_x, crane_pos_y, 1, cargo_placed)
            except Exception as e:
                log("plot process error")

            #CRANE messages
            stamp_cfn1 = os.stat(self.cfn1).st_mtime
            #stamp_sfn1 = os.stat(self.sfn1).st_mtime
            if stamp_cfn1 != self._cached_stamp_cfn1:
                self._cached_stamp_cfn1 = stamp_cfn1
                    # File has changed, so do something...
                print ("has file been changed?")
                try:
                    f = open(self.cfn1, "r")
                    lines = f.read().splitlines()
                    f.close()
                    i = get_line_number(last_line, lines)
                    
                    if lines[-i] == lines[-1]:
                        #print "last line is the last one"
                        last_line = lines[-1]
                        try:
                            process_data(last_line)
                        except Exception as e:
                            log("data process error")   
                    else:
                                                
                        for x in reversed(range(1,i+1)):
                            #print "start processing data with index: " + str(x)
                            last_line = lines[-x]
                            try:
                                process_data(last_line)
                            except Exception as e:
                                log("data process error")
                    #last_line = lines[-1]
                    
                    data = last_line
                    if not data and self.is_running: # Empty data 
                        print ("not data and self.is_running")

                except Exception as e:
                    if self.is_running:
                        log("file read error")

            #ship 1 messages
            #elif stamp_sfn1 != self._cached_stamp_sfn1:
            #    self._cached_stamp_sfn1 = stamp_sfn1
            #        # File has changed, so do something...
            #    try:
            #        f = open(self.sfn1, "r")
            #        lines = f.read().splitlines()
            #        last_line = lines[-1]
            #        f.close()
            #        data = last_line
            #        if not data and self.is_running: # Empty data 
            #            print ("not data and self.is_running")

            #    except Exception as e:
            #        if self.is_running:
            #            log("file read error")

######################################################################

def process_data(data):
    global crane_pos_x
    global crane_pos_y


    global list_of_ships

    global cargo_placed
    global last_line
    global crane_above_ship
    global ships
    global ship_times
    
    global global_time
    global ship_time

    global t11
    global t12
    global t13
    global t14
    global t15


  
    test = data.split("|")
    #print test[-1]
    msg = test[-1]
    
    
    #for x in test:
    #    print x + "\n" 
        #values = ast.literal_eval(x)
        #id = values[0]
    
    if msg[:11] == 'Crane state':
        #print "crane status message received"
        #SERIAL_CRANE_LOCMSG 1
        """
        typedef nx_struct serialCraneLocMsg { //this struct is actually not used, length depends on how many winners there are
            nx_uint8_t length;
            nx_uint8_t messageID;
            nx_uint8_t xLoc;
            nx_uint8_t yLoc;
            nx_uint8_t isCargoPlaced;
            nx_uint8_t popularCmdWinner1;
            nx_uint8_t popularCmdWinner2;
            //nx_uint8_t popularCmdWinner3;
            //nx_uint8_t popularCmdWinner4;
        } serialCraneLocMsg;
        """

        crane_pos_x, crane_pos_y, cargo_placed = map(int, re.findall(r'\d+', msg))
        #print crane_pos_x
        #print crane_pos_y
        #print cargo_placed

        #pos_x = values[1]
        #pos_y = values[2]
        #cargo_placed = values[3]
        #winning_ship = 0
        #print values
        #if len(values) > 3:
        #    winning_ship = values[4]
        winners = ""
        #print values
        #print len(values)
        
        #if len(values) > 4:
        #    for x in xrange(4,len(values)):
        #        winners += str(values[x]) + " "

        #pos = gps_pos(crane_pos_x,crane_pos_y)

        #print "message from crane: " + str(id) + ", my new positsion is: " + str(pos_x) + " " + str(pos_y)
        for i in ships:
            if ships[i] == [crane_pos_x, crane_pos_y]:
                print "CRANE IS ABOVE SHIP"
                #print str(ships[i]) + " " + str(i)

        if cargo_placed:
            print "ROUND won by ship: " + winners + "CARGO PLACED"
            crane_above_ship = 1
        else:
            #print "ROUND won by ship: " + winners + " CARGO not placed yet"
            crane_above_ship = 0
       
        #try:
        #    plotti(crane_pos_x, crane_pos_y, 1, crane_above_ship)
        #except Exception as e:
        #    log("plot process error")
        
        
        # count global and ship clocks
        #if global_time > 0:
        #    global_time -= 1

        
       
        #print ship_times.keys()

        #if ship_times.keys() > 0:
    

        for ii in ship_times.keys():

            if ship_times[ii] > 0:
                ship_times[ii] -= 1
                
                if ii == 0:
                    t11.set_text('$' + str(list_of_ships[ii]) + ": " + str(ship_times[ii]) + '$')
                if ii == 1:
                    t12.set_text('$' + str(list_of_ships[ii]) + ": " + str(ship_times[ii]) + '$')
                if ii == 2:
                    t13.set_text('$' + str(list_of_ships[ii]) + ": " + str(ship_times[ii]) + '$')                            
                if ii == 3:
                    t14.set_text('$' + str(list_of_ships[ii]) + ": " + str(ship_times[ii]) + '$')   
                if ii == 4:
                    t15.set_text('$' + str(list_of_ships[ii]) + ": " + str(ship_times[ii]) + '$')
        

        
        #try:
            #plotti(pos.x, pos.y, 1, crane_above_ship)
        #except Exception as e:
        #    log("plot unsuccesscull")


        #if global_time == 0:
        #    print "GAME is OVER"
        
        #print "---------------------> NEW ROUND <---------------------"
        return 1

        

        
    #elif id == 2:
    elif msg[:8] == 'New ship':
        print "New ship message received"
    
        ship_id, pos_x, pos_y, cargo, dTime = map(int, re.findall(r'\d+', msg))
    
        """
        typedef nx_struct newShipSerialMsg {
            nx_uint8_t length;
            nx_uint8_t messageID;
            nx_uint8_t shipID;
            nx_uint8_t xLoc;
            nx_uint8_t yLoc;
            nx_uint16_t dTime;  
        } newShipSerialMsg;
        """
                            
        #ship_id = values[1] #ship id is a two byte value. 32bit int. 5602
        if ship_id not in list_of_ships:
            list_of_ships.append(ship_id)
        ##list_of_ships.index(values[1]) returns index of specific ship 
        #
        #pos_x = values[2]
        #pos_y = values[3]
        #ship_times[ship_id] = dTime
        ship_times[list_of_ships.index(ship_id)] = dTime
        
        pos = gps_pos(pos_x,pos_y)
        crane_above_ship = 0
        print "ship " + str(ship_id) + " has entered the game" + " Time left: " + str(dTime)
        print "ship " + str(ship_id) + " position is: " + str(pos.x) + "-" + str(pos.y)

        
        ax.text(pos_x - 2, pos_y - 2, r'$'+str(ship_id)+'$', fontsize=12)
        
        if list_of_ships.index(ship_id) == 1:
            t11.set_text('$' + str(ship_id) + ": " + str(dTime) + '$')
        if list_of_ships.index(ship_id) == 2:
            t12.set_text('$' + str(ship_id) + ": " + str(dTime) + '$')
        if list_of_ships.index(ship_id) == 3:
            t13.set_text('$' + str(ship_id) + ": " + str(dTime) + '$')
        if list_of_ships.index(ship_id) == 4:
            t14.set_text('$' + str(ship_id) + ": " + str(dTime) + '$')
        if list_of_ships.index(ship_id) == 5:
            t15.set_text('$' + str(ship_id) + ": " + str(dTime) + '$')
        """
        if ship_id == 5:
            t5.set_text('$' + str(ship_id) + ": " + str(values[4]) + '$')
        if ship_id == 6:
            t6.set_text('$' + str(ship_id) + ": " + str(values[4]) + '$')
        if ship_id == 7:
            t7.set_text('$' + str(ship_id) + ": " + str(values[4]) + '$')
        if ship_id == 14:
            t14.set_text('$' + str(ship_id) + ": " + str(values[4]) + '$')
        if ship_id == 8:
            t8.set_text('$' + str(ship_id) + ": " + str(values[4]) + '$')
        """    
        plotti(pos.x, pos.y, list_of_ships.index(ship_id) + 2, crane_above_ship)
    #elif id == 3:
    elif msg[:9] == 'Game time':
        print "Global time message received"
        gTime = map(int, re.findall(r'\d+', msg))
        """
        typedef nx_struct gTimeSerialMsg {
            nx_uint8_t length;
            nx_uint8_t messageID;
            nx_uint16_t gTime;  
        } gTimeSerialMsg;
        """
        global_time = gTime
        crane_above_ship = 0
        print "---------------------> NEW  GAME <---------------------"
        print "global time is: " + str(global_time)                      
        




    #elif id == 111:
    elif msg[:9] == 'Crane com':
        print "Crane command message received"
        sender_id, command = map(int, re.findall(r'\d+', msg))
        
        if command == 1:
            print "Ship " + str(sender_id) + " CRANE move UP"
        if command == 2:
            print "Ship " + str(sender_id) + " CRANE move DOWN"
        if command == 3:
            print "Ship " + str(sender_id) + " CRANE move LEFT"
        if command == 4:
            print "Ship " + str(sender_id) + " CRANE move RIGHT"
        if command == 5:
            print "Ship " + str(sender_id) + " CRANE place CARGO"

    elif id == 112:
        sender_id = values[1]
        pos_x = values[2]
        pos_y = values[3]
        pos = gps_pos(pos_x,pos_y)
    else:
        return 1


#def log(a,b,c):
#    """Logs the data received from socket to database."""
#    print a
def log(text, *args):
    """
    Logs a timestamped message to file and to console.

    @param   args  string format arguments, if any, to substitute in text
    """
    
    now = datetime.datetime.now()
    finaltext = text % args if args else text
    if "\n" in finaltext: # Indent all linebreaks
        finaltext = finaltext.replace("\n", "\n\t\t")
    msg = "%s,%03d\t%s\n" % (now.strftime("%Y-%m-%d %H:%M:%S"), now.microsecond / 1000,
                             finaltext)
    if LOG_FILE:
        with open(LOG_FILE, "a") as f:
            f.write(msg)
#    if DO_VERBOSE:
    msg_print = (msg[:2000] + "..") if len(msg) > 2000 else msg
    sys.stderr.write(msg_print)



observer = FileReaderClient(crane_file_name, ship1_file_name, ship2_file_name, ship3_file_name)
observer.run()


f.close()
