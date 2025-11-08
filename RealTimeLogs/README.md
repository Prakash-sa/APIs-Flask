# Real-Time Log Streaming Examples

This folder demonstrates multiple strategies for pushing large log updates from the filesystem to API consumers using Flask.

| File | Technique | Notes |
| --- | --- | --- |
| `sse_server.py` | Server-Sent Events | Streams `text/event-stream` updates from `follow_log`. |
| `long_polling_server.py` | Long polling | Clients hit `/logs/long-poll?pos=<offset>` and hold the connection until new lines exist. |
| `polling_server.py` | Simple polling API | Clients periodically call `/logs/latest` to fetch batches. |
| `websocket_server.py` | WebSocket (Flask-SocketIO) | Emits `log_entry` events as soon as data is appended. |
| `ajax_app.py` + `templates/ajax_client.html` | AJAX front end | Static HTML page that polls the REST endpoint using `fetch` every 3 seconds. |
| `log_reader.py` | Shared helpers | Provides tailing utilities and a shared log file at `logs/sample.log`. |

Each service exposes `POST /logs` so you can simulate a new entry:

```bash
curl -X POST http://localhost:5000/logs \
     -H "Content-Type: application/json" \
     -d '{"message":"Processed another 5,000 lines"}'
```

Run any server with `python3 RealTimeLogs/<file>.py`. New log entries are appended to `logs/sample.log` and broadcast with the selected strategy.
