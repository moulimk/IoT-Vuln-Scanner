from flask import Blueprint, render_template, jsonify, current_app
import os

def load_devices():
    use_mock = os.getenv('USE_MOCK_ARP_OUTPUT', 'False') == 'True'
    if use_mock:
        from tests.mock_arp_output import mock_arp_output
        return mock_arp_output
    else:
        return current_app.config.get('devices', [])

def create_device_bp():
    device_bp = Blueprint(
        'device', __name__,
        template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    )

    @device_bp.route('/')
    def index():
        return render_template('index.html')

    @device_bp.route('/devices')
    def get_devices():
        devices = load_devices()
        return jsonify(devices)

    @device_bp.route('/device/<ip>')
    def device_detail(ip):
        devices = load_devices()
        device = next((d for d in devices if d["ip_address"] == ip), None)
        if device:
            return render_template('device_detail.html', device=device)
        else:
            return "Device not found", 404

    @device_bp.route('/overview')
    def overview():
        stats = {"total_packets": 1000, "total_bytes": 500000, "rate_pps": 10, "rate_bps": 5000}
        return render_template('overview.html', stats=stats)

    @device_bp.route('/settings')
    def settings():
        return render_template('settings.html')

    @device_bp.route('/consent')
    def consent():
        return render_template('consent.html')

    @device_bp.route('/survey')
    def survey():
        return render_template('survey.html')

    return device_bp
