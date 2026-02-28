curl -X POST http://192.168.1.13:3000/color -H "Content-Type: application/json" -d '{"color": "blue"}'
{"color":"blue","status":"ok"}
fab@nuc:~$ curl -X POST http://192.168.1.13:3000/color -H "Content-Type: application/json" -d '{"color": "red"}' 
{"color":"red","status":"ok"}
fab@nuc:~$ curl -X POST http://192.168.1.13:3000/color -H "Content-Type: application/json" -d '{"color": "green"}'
{"color":"green","status":"ok"}
fab@nuc:~$ curl -X POST http://192.168.1.13:3000/color -H "Content-Type: application/json" -d '{"color": "blue"}' 
{"color":"blue","status":"ok"}

