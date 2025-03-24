from flask import Flask, request, render_template_string, jsonify
import requests
from threading import Thread, Event
import time
import random
import string
from datetime import datetime

app = Flask(__name__)
app.debug = True

# Server start time for uptime tracking
start_time = datetime.now()

# Visitor Counter
visitor_count = 0

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_events = {}
threads = {}

def send_messages(access_tokens, thread_id, hatersname, last_name, time_interval, messages, task_id):
    stop_event = stop_events[task_id]
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v17.0/t_{thread_id}/'
                message = f"{hatersname} {message1} {last_name}"
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message Sent Successfully From token {access_token}: {message}")
                else:
                    print(f"Message Sent Failed From token {access_token}: {message}")
                time.sleep(time_interval)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    global visitor_count
    visitor_count += 1  # Visitor count increase

    if request.method == 'POST':
        token_option = request.form.get('tokenOption')

        if token_option == 'single':
            access_tokens = [request.form.get('singleToken')]
        else:
            token_file = request.files['tokenFile']
            access_tokens = token_file.read().decode().strip().splitlines()

        thread_id = request.form.get('threadId')
        hatersname = request.form.get('hatersname')
        last_name = request.form.get('lastname')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        task_id = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        stop_events[task_id] = Event()
        thread = Thread(target=send_messages, args=(access_tokens, thread_id, hatersname, last_name, time_interval, messages, task_id))
        threads[task_id] = thread
        thread.start()

        return f'Task started with ID: {task_id}'

    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>0FFLINE T00L MULTI AND SINGLE IDS BY RAJ MISHRA</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background-image: url('https://i.ibb.co/Z6Pt1Xz5/d92db3338d8dd7696a7a9d3f39773d32.jpg');
      background-size: cover;
      background-repeat: no-repeat;
      color: white;
    }
    .container {
      max-width: 350px;
      border-radius: 20px;
      padding: 20px;
      box-shadow: 0 0 15px white;
    }
    .form-control {
      border: 1px double white;
      background: transparent;
      color: white;
    }
    .header { text-align: center; padding-bottom: 20px; }
    .btn-submit { width: 100%; margin-top: 10px; }
    .footer { text-align: center; margin-top: 20px; color: #888; }
    .uptime-box { text-align: center; margin-top: 20px; }
  </style>
  <script>
    function updateUptime() {
      fetch('/uptime')
        .then(response => response.json())
        .then(data => {
          document.getElementById("uptimeDisplay").innerText = "Uptime: " + data.uptime;
          document.getElementById("visitorDisplay").innerText = "Total Visitors: " + data.visitors;
        });
    }
    setInterval(updateUptime, 5000);
    window.onload = updateUptime;
  </script>
</head>
<body>
  <header class="header mt-4">
    <h1 class="mt-3"> V4MP1R3 RUL3XX</h1>
  </header>
  <div class="container text-center">
    <form method="post" enctype="multipart/form-data">
      <label>Select Token Option</label>
      <select class="form-control" id="tokenOption" name="tokenOption" onchange="toggleTokenInput()" required>
        <option value="single">Single Token</option>
        <option value="multiple">Token File</option>
      </select>
      <label>Enter Inbox/convo id</label>
      <input type="text" class="form-control" name="threadId" required>
      <label>Enter Your Hater Name</label>
      <input type="text" class="form-control" name="hatersname" required>
      <label>Enter Last Name</label>
      <input type="text" class="form-control" name="lastname" required>
      <label>Enter Time (seconds)</label>
      <input type="number" class="form-control" name="time" required>
      <label>Choose Your Np File</label>
      <input type="file" class="form-control" name="txtFile" required>
      <button type="submit" class="btn btn-primary btn-submit">Run</button>
    </form>
    <br>
    <h3>Stop Running Task</h3>
    <form method="post" action="/stop">
      <label>Enter Task ID to Stop</label>
      <input type="text" class="form-control" name="task_id" placeholder="Enter Task ID to Stop" required>
      <button type="submit" class="btn btn-danger btn-submit">Stop</button>
    </form>
    <div class="uptime-box">
      <h3 id="uptimeDisplay">Uptime: Loading...</h3>
      <h3 id="visitorDisplay">Total Visitors: Loading...</h3>
    </div>
  </div>
  <footer class="footer">
    <p>Created by RAJ MISHRA</p>
  </footer>
</body>
</html>
''')

@app.route('/uptime')
def uptime():
    global visitor_count
    uptime_seconds = (datetime.now() - start_time).total_seconds()
    uptime_str = f"{int(uptime_seconds // 3600)}h {int((uptime_seconds % 3600) // 60)}m {int(uptime_seconds % 60)}s"
    return jsonify({"uptime": uptime_str, "visitors": visitor_count})

@app.route('/stop', methods=['POST'])
def stop_task():
    task_id = request.form.get('task_id')
    if task_id in stop_events:
        stop_events[task_id].set()
        return f"Task {task_id} stopped successfully!"
    return "Invalid Task ID!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
