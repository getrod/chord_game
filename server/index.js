const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");            // v for audio_event
const io = new Server(server, {cors: {origin: '*'}, maxHttpBufferSize:  1e8});

app.get('/', (req, res) => {
  res.send('Midi Server!')
});

io.on('connection', (socket) => {
  console.log('a user connected');

  socket.on('midi_ports', (ports) => {
    console.log(ports)
  });

  socket.on('is_port_open', (is_open) => {
    console.log(`port open: ${is_open}`)
  });

  socket.on('midi_event', (midi_event) => {
    console.log(`${midi_event}`)
    io.emit('midi_event', midi_event);
  });

  socket.on('midi_track_event', (midi_event) => {
    io.emit('midi_track_event', midi_event);
  });

  // AUDIO

  socket.on('track_audio_req', (track) => {
    io.emit('track_audio_req', track);
  });

  socket.on('track_audio_res', (audio_res) => {
    io.emit('track_audio_res', audio_res);
  });

  // MOTIF

  socket.on('motif_compile', (motif_string) => {
    io.emit('motif_compile', motif_string);
  });

  socket.on('motif_compile_complete', (motif) => {
    io.emit('motif_compile_complete', motif);
  });

  socket.on('motif_compile_error', (e) => {
    io.emit('motif_compile_error', e);
  });
});

server.listen(3000, () => {
  console.log('listening on *:3000');
});