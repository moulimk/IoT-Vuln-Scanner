import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """Create a database connection to a SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Create tables in the SQLite database"""
    try:
        sql_create_devices_table = """
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT,
            mac_address TEXT,
            manufacturer TEXT,
            device_type TEXT
        );
        """
        sql_create_vulnerabilities_table = """
        CREATE TABLE IF NOT EXISTS vulnerabilities (
            id TEXT PRIMARY KEY,
            device_type TEXT NOT NULL,
            source_identifier TEXT,
            published DATE,
            last_modified DATE,
            vuln_status TEXT,
            description TEXT,
            cvss_score REAL,
            severity TEXT,
            attack_vector TEXT,
            attack_complexity TEXT,
            privileges_required TEXT,
            user_interaction TEXT,
            scope TEXT,
            confidentiality_impact TEXT,
            integrity_impact TEXT,
            availability_impact TEXT,
            exploitability_score REAL,
            impact_score REAL,
            FOREIGN KEY (device_type) REFERENCES devices (device_type)
        );
        """
        conn.execute(sql_create_devices_table)
        conn.execute(sql_create_vulnerabilities_table)
    except Error as e:
        print(e)

def insert_device(conn, device_type):
    """Insert a new device into the devices table"""
    sql = '''INSERT INTO devices(device_type)
             VALUES(?)'''
    cur = conn.cursor()
    cur.execute(sql, (device_type,))
    conn.commit()
    return cur.lastrowid

def insert_vulnerability(conn, vulnerability, device_type):
    """Insert a new vulnerability into the vulnerabilities table if it does not exist"""
    cur = conn.cursor()
    cur.execute('SELECT id FROM vulnerabilities WHERE id = ?', (vulnerability.get('id'),))
    row = cur.fetchone()
    if row:
        print(f"Vulnerability {vulnerability.get('id')} already exists. Skipping insert.")
        return row[0]

    sql = '''INSERT INTO vulnerabilities(id, device_type, source_identifier, published, last_modified, vuln_status, description,
                                         cvss_score, severity, attack_vector, attack_complexity, privileges_required,
                                         user_interaction, scope, confidentiality_impact, integrity_impact, availability_impact,
                                         exploitability_score, impact_score)
             VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    cur.execute(sql, (
        vulnerability.get('id'),
        device_type,
        vulnerability.get('sourceIdentifier'),
        vulnerability.get('published'),
        vulnerability.get('lastModified'),
        vulnerability.get('vulnStatus'),
        ', '.join([desc['value'] for desc in vulnerability.get('descriptions', []) if desc['lang'] == 'en']),
        vulnerability.get('metrics', {}).get('cvssMetricV30', [{}])[0].get('cvssData', {}).get('baseScore'),
        vulnerability.get('metrics', {}).get('cvssMetricV30', [{}])[0].get('cvssData', {}).get('baseSeverity'),
        vulnerability.get('metrics', {}).get('cvssMetricV30', [{}])[0].get('cvssData', {}).get('attackVector'),
        vulnerability.get('metrics', {}).get('cvssMetricV30', [{}])[0].get('cvssData', {}).get('attackComplexity'),
        vulnerability.get('metrics', {}).get('cvssMetricV30', [{}])[0].get('cvssData', {}).get('privilegesRequired'),
        vulnerability.get('metrics', {}).get('cvssMetricV30', [{}])[0].get('cvssData', {}).get('userInteraction'),
        vulnerability.get('metrics', {}).get('cvssMetricV30', [{}])[0].get('cvssData', {}).get('scope'),
        vulnerability.get('metrics', {}).get('cvssMetricV30', [{}])[0].get('cvssData', {}).get('confidentialityImpact'),
        vulnerability.get('metrics', {}).get('cvssMetricV30', [{}])[0].get('cvssData', {}).get('integrityImpact'),
        vulnerability.get('metrics', {}).get('cvssMetricV30', [{}])[0].get('cvssData', {}).get('availabilityImpact'),
        vulnerability.get('metrics', {}).get('cvssMetricV30', [{}])[0].get('exploitabilityScore'),
        vulnerability.get('metrics', {}).get('cvssMetricV30', [{}])[0].get('impactScore')
    ))
    conn.commit()
    return cur.lastrowid
