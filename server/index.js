const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server, {cors: {origin: '*'}});

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

  socket.on('midi_track', (track) => {
    console.log(track)
    io.emit('midi_track', track);
  });
});

server.listen(3000, () => {
  console.log('listening on *:3000');
});