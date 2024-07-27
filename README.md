 IoT Scanner

The IoT Scanner is an advanced security tool for smart homes, designed to detect, analyze, and secure IoT devices. Built from scratch with a modular approach, it enhances the functionalities of the IoT Inspector project.

 Features

1. Device Detection and Network Scanning:
   - ARP-based network scanning to detect connected devices.
   - Device identification using the IEEE OUI database.

2. Traffic Analysis:
   - Traffic rate analysis to provide detailed network usage statistics.
   - Global network traffic insights.

3. Data Anonymization:
   - Ensures privacy by anonymizing sensitive network data.

4. User Interface:
   - Developed as a Flask web application.
   - Device list displaying detected devices with detailed information.
   - Sidebar for easy navigation.
   - Overview page summarizing global network statistics.
   - Detailed device pages showing specific information and traffic statistics.
   - Settings page for user configuration.
   - Consent management for data collection.
   - Survey components for user feedback.

 Project Structure

- core:
  - `arp_scanner.py`: Handles network scanning using ARP requests.
  - `device_identifier.py`: Identifies devices using the IEEE OUI database.
  - `traffic_rate.py`: Analyzes network traffic rates for detected devices.
  - `anonymization.py`: Implements data anonymization methods.
  - `global_stats.py`: Maintains global network statistics.

- ui:
  - templates:
    - `index.html`: Displays the list of detected devices.
    - `device_detail.html`: Shows detailed information for each device.
    - `overview.html`: Provides an overview of global network statistics.
    - `settings.html`: Allows configuration of scanner settings.
    - `sidebar.html`: Template for sidebar navigation.
    - `consent.html`: Manages user consent.
    - `survey.html`: UI for user surveys.
  - `device_list.py`: Manages device listing and detail view routes.
  - `consent.py`: Handles consent management routes.
  - `sidebar.py`: Manages sidebar navigation template.
  - `template.py`: Provides template rendering utilities.

- data:
  - `oui.txt`: Contains the IEEE OUI database for device identification.

- scripts:
  - `start.py`: Main script to initialize and run the Flask application.

 Installation
		
   ```bash (linux)
   git clone <repository_url>](https://github.com/moulimk/IoT-Vuln-Scanner.git
   cd IoT-Scanner
   python3 -m venv env
   source /env/bin/activate
   python3 IoT-Scanner/scripts/start.py

   ```cmd (windows)
   git clone <repository_url>](https://github.com/moulimk/IoT-Vuln-Scanner.git
   cd IoT-Scanner
   python3 -m venv env
   source \env\bin\activate.bat
   python3 IoT-Scanner\scripts\start.py
