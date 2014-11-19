#!python
#import system
import SimpleHTTPServer
import SocketServer
import subprocess
import fcntl
import io
import os
import time
import threading
import select
import re
import socket
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from firebase import firebase


# monitor these and send to firebase.
#[19:31:43] [Server thread/INFO]: chris_smith left the game
#[19:45:53] [User Authenticator #2/INFO]: UUID of player chris_smith is a96a31a1-34e5-40ee-9d32-72c463181e1e
#[19:45:53] [Server thread/INFO]: chris_smith[/74.125.59.76:45466] logged in with entity id 4016 at (133.5, 72.0, 
#256.5)
#[19:45:53] [Server thread/INFO]: chris_smith joined the game

PORT = 8000
FIREBASE_PROJECT = 'glaring-heat-2029'

class MyHttpServer(HTTPServer):
  def set_proc(self, proc):
    self.proc = proc;

class myHandler(BaseHTTPRequestHandler):
  #https://cs.corp.google.com/#piper///depot/google3/cityblock/omnomnom/onboard/webservice.py&sq=package:piper%20file://depot/google3%20-file:google3/(experimental%7Cobsolete)&q=BaseHTTPRequestHandler&type=cs&l=25
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()
    # Send the html message
    self.wfile.write("Hello World !" + self.path)

    # Read all the stdout, then send a request
    proc = self.server.proc
    try:
      fcntl.fcntl(proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
      ignored = proc.stdout.read()
      print "ignored text: " + ignored
    except IOError:
      print "EE hi 1"
      # raises on empty stdout
      pass
    proc.stdin.write("list\n")
    result = ""
    try:
      # Lame, but this sleep fixes a "resource not available problem"
      # I'm sure this is a better way.
      time.sleep(.1)
      # Not sure if this reads all the stdout or just 1k or something
      result += proc.stdout.read()
    except IOError, e:
      print "EE hi 2"
      print e
      # raises on empty stdout
      pass
    num_players = re.search("There are (\d+)/(\d+) players online", result.split("\n")[0]).group(1)
    players = []
    for player_line in result.split("\n")[1:]:
      print "PL: %s" % player_line
      match = re.search("\[Server thread/INFO]: (.+)", player_line)
      if match:
        players.append(match.group(1))
    print "RESULT = (%s)" % result
    print "NUM_PLAYERS = (%s)" % num_players
    print "PLAYERS = (%s)" % players

    # then read again.
    return


def AddOrRemovePlayer(player, fire, add=True):
  container_name = socket.gethostname()
  fire.put('/servers/%s/active' % container_name,
           player, add)

def start_watch_thread():
  # cheat and use subprocess popen of tail so we can get blocking reads
  # We are already in a thread.
  fire = firebase.FirebaseApplication('https://%s.firebaseio.com' % FIREBASE_PROJECT, None)

  proc = subprocess.Popen(["stdbuf", "--output=0", "tail", "-F", "logs/latest.log"],
                          stdout = subprocess.PIPE)
  while True:
    #for line in proc.stdout:
    line = proc.stdout.readline().rstrip()
    new_player = re.search("thread/INFO]: (.+) joined the game", line)
    quitter = re.search("thread/INFO]: (.+) left the game", line)

    # [09:41:21] [Server thread/INFO]: chris_smith joined the game
    if new_player:
      # TODO(check for this too)
      #  [User Authenticator #1/INFO]: UUID of player chris_smith is a96a31a1-34e5-40ee-9d32-72c463181e1e
      player = new_player.group(1)
      AddOrRemovePlayer(player, fire)

    # [18:37:27] [Server thread/INFO]: chris_smith left the game
    if quitter:
      player = quitter.group(1)
      AddOrRemovePlayer(player, fire, None)

    #print "LINE: [%s]" % line



def start_minecraft():
  proc = subprocess.Popen(["java", "-Xmx1G", "-Xms1G", "-jar", "minecraft_server.jar", "nogui"],
                          stdout = subprocess.PIPE,
                          stdin = subprocess.PIPE)
  #
  # Start a thread to watch the file latest.log and send results to firebase.
  watch = threading.Thread(target=start_watch_thread)
  #watch.daemon = True
  watch.start()

  return proc

def start_web_server(port, proc):
  httpd = MyHttpServer(('localhost', port), myHandler)
  httpd.set_proc(proc)
  print "serving at port", port
  httpd.serve_forever()


def main():
  proc = start_minecraft()
  #start_web_server(PORT, proc)

if __name__ == "__main__":
  main()
