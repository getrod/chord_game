const express = require('express');
const app = express();
const http = require('http');
const server = http.createServer(app);
const { Server } = require("socket.io");
const io = new Server(server);

app.use(express.static(__dirname + '/public'));

app.get('/', (req, res) => {
  res.sendFile(__dirname + '/index.html');
});

io.on('connection', (socket) => {
  console.log('a user connected');

  socket.on('on question', (msg) => {
    console.log('on question called');
    io.emit('on question', msg);
  });

  socket.on('on score', (msg) => {
    console.log('recieved a score');
    io.emit('on score', msg);
  });

  socket.on('chord', (msg) => {
    console.log(msg);
    // emit the chord
    io.emit('chord', msg)
  });


  socket.on('question', (msg) => {
    io.emit('question', msg);
  });

  socket.on('get question', (msg) => {
    io.emit('get question', msg);
  });

  socket.on('settings', (msg) => {
    io.emit('settings', msg);
  });

  socket.on('get settings', (msg) => {
    io.emit('get settings', msg);
  });

  socket.on('default settings', (msg) => {
    io.emit('default settings', msg);
  });

  socket.on('get default settings', (msg) => {
    io.emit('get default settings', msg);
  });

  socket.on('change settings', (msg) => {
    io.emit('change settings', msg);
  });


  socket.on('score', (msg) => {
    io.emit('score', msg);
  });

  socket.on('random game', (msg) => {
    io.emit('random game', msg);
  });

  socket.on('number game', (msg) => {
    io.emit('number game', msg);
  });

});

server.listen(3000, () => {
  console.log('listening on *:3000');
});