# Souvenir - An application for creating Audio Memories

## Description

Souvenir is a client-server application for recording and storing audio files using python. Audio files are stored in a repository folder and organized using an instance of MongoDB.

## Usage

The server is started in the command shell, and runs a Flask instance that routes communications with the client. 

The client applicaiton is a simple GUI-based interactive prompt, which provides the user with the capability to either record an audio to the server or retrieve an audio from the server. A limit of 60 seconds of audio can be recorded for storage and transmission purposes, since the repository is meant to run on a Raspberrypi loaded with Ubuntu, or a similar low-cost, high-efficiency device.

## Libraries Used:
* Flask: *interactions between client/server*
* PyMongo: *mongodb instantiation for server*
* Flask_HTTPBasicAuth: *authenticating to server*
* PyQt5: *GUI creation*
* io: *bytestream conversion*
* Requests: *interactions between client/server*
* PyAudio: *sound recording and playback*
* Wave: *sound recording and playback*
* OS: *file saving and removal*
* sys: *interactions with the host system*

## Future Updates (Ran Out of Time):
* Use of GridFS with mongodb for storage of files
* Zeroconf integration for automatic connectivity
* Better performance and threading
