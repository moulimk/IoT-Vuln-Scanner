from flask import Blueprint, render_template, jsonify, current_app
import os
from core.database import get_db_connection

def create_device_bp():
    device_bp = Blueprint('device', __name__, template_folder='templates')

    def load_devices():
        use_mock = os.getenv('USE_MOCK_ARP_OUTPUT', 'False') == 'True'
        if use_mock:
            from tests.mock_arp_output import mock_arp_output as devices
        else:
            devices = []
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM devices")
            rows = cursor.fetchall()
            for row in rows:
                device = {
                    "id": row["id"],
                    "mac_address": row["mac_address"],
                    "ip_address": row["ip_address"],
                    "manufacturer": row["manufacturer"],
                    "device_type": row["device_type"]
                }
                devices.append(device)
            conn.close()
        return devices

    @device_bp.route('/')
    def index():
        devices = load_devices()
        return render_template('index.html', devices=devices)

    @device_bp.route('/devices')
    def get_devices():
        devices = load_devices()
        return jsonify(devices)

    @device_bp.route('/device/<int:device_id>')
    def device_detail(device_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
        device = cursor.fetchone()
        cursor.execute('''
            SELECT v.*
            FROM vulnerabilities v
            JOIN device_vulnerabilities dv ON v.id = dv.vulnerability_id
            WHERE dv.device_id = ?
        ''', (device_id,))
        vulnerabilities = cursor.fetchall()
        conn.close()
        return render_template('device_detail.html', device=device, vulnerabilities=vulnerabilities)

    return device_bp
