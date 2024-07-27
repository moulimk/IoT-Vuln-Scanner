from flask import Blueprint, render_template, request, redirect

consent_bp = Blueprint('consent_bp', __name__)

@consent_bp.route('/consent', methods=['GET'])
def consent():
    return render_template('consent.html')

@consent_bp.route('/save_consent', methods=['POST'])
def save_consent():
    consent = request.form.get('consent')
    # Save consent status
    return redirect('/')
