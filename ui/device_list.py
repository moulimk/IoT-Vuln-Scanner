# ui/device_list.py

from flask import Blueprint, render_template, jsonify, request, redirect
import pandas as pd

device_bp = Blueprint('device_bp', __name__)

devices = pd.DataFrame()
traffic_analyzer = None
global_stats = None
ip_map = {}

@device_bp.route('/')
def index():
    return render_template('index.html')

@device_bp.route('/devices')
def get_devices():
    return jsonify(devices.to_dict(orient='records'))

@device_bp.route('/device/<anon_ip>')
def get_device(anon_ip):
    original_ip = ip_map.get(anon_ip, None)
    if original_ip is None:
        return "Device not found", 404
    
    device = devices[devices['ip'] == anon_ip].iloc[0].to_dict()
    if traffic_analyzer:
        stats = traffic_analyzer.get_device_statistics(original_ip)
        device.update(stats)
    return render_template('device_detail.html', device=device)

@device_bp.route('/overview')
def overview():
    stats = global_stats.get_global_statistics() if global_stats else {}
    return render_template('overview.html', stats=stats)

@device_bp.route('/settings', methods=['GET'])
def settings():
    return render_template('settings.html')

@device_bp.route('/save_settings', methods=['POST'])
def save_settings():
    setting1 = request.form.get('setting1')
    setting2 = request.form.get('setting2')
    # Save settings as needed
    return redirect('/settings')

def set_devices(device_data):
    global devices
    devices = device_data

def set_traffic_analyzer(analyzer):
    global traffic_analyzer
    traffic_analyzer = analyzer

def set_global_stats(stats):
    global global_stats
    global_stats = stats

def set_ip_map(mapping):
    global ip_map
    ip_map = mapping
