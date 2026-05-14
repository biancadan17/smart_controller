from flask import Flask, render_template_string
import serial
import threading
import time

app = Flask(__name__)


ser = serial.Serial('COM3', 9600, timeout=1)

date_sistem = {"temp": "0", "flood": "0"}

def citire_seriala():
    global date_sistem
    while True:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if "TEMP:" in line and "FLOOD:" in line:
                    parts = line.split('|')
                    date_sistem["temp"] = parts[0].split(':')[1]
                    date_sistem["flood"] = parts[1].split(':')[1]
        except:
            pass
        time.sleep(0.1)


threading.Thread(target=citire_seriala, daemon=True).start()

HTML = """
<body style="background-color: {{ 'red' if flood == '1' else 'white' }}; text-align: center; font-family: Arial;">
    <h1>Monitorizare Sistem IoT</h1>
    <h2 style="font-size: 50px;">Temperatura: {{ temp }} °C</h2>
    <h2 style="font-size: 50px;">Status: {{ 'INUNDATIE!' if flood == '1' else 'SIGUR' }}</h2>
    <script>setTimeout(function(){location.reload();}, 1000);</script>
</body>
"""

@app.route('/')
def index():
    return render_template_string(HTML, temp=date_sistem['temp'], flood=date_sistem['flood'])

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
