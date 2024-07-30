from flask import Blueprint, render_template, request
from core.database import create_connection

def create_device_bp(conn):
    device_bp = Blueprint('device', __name__)

    @device_bp.route('/')
    def index():
        cursor = conn.cursor()
        cursor.execute('SELECT id, ip_address, mac_address, manufacturer, device_type FROM devices')
        devices = cursor.fetchall()
        device_dicts = [{'id': device[0], 'ip_address': device[1], 'mac_address': device[2], 'manufacturer': device[3], 'device_type': device[4]} for device in devices]
        conn.close()
        return render_template('index.html', devices=device_dicts)

    @device_bp.route('/device/<int:device_id>')
    def device_detail(device_id):
        cursor = conn.cursor()
        cursor.execute('SELECT id, ip_address, mac_address, manufacturer, device_type FROM devices WHERE id = ?', (device_id,))
        device = cursor.fetchone()
        cursor.execute('SELECT cve_id, description, severity, published_date, last_modified_date FROM vulnerabilities WHERE device_id = ?', (device_id,))
        vulnerabilities = cursor.fetchall()
        conn.close()
        return render_template('device_detail.html', device=device, vulnerabilities=vulnerabilities)

    return device_bp
