# WiFi P&L Calculator

A Flask-based web application for calculating Profit & Loss (P&L) analysis for in-flight WiFi services. This tool helps airlines and service providers analyze the financial viability of WiFi offerings across different fleet configurations, flight routes, and pricing strategies.

## Overview

The WiFi P&L Calculator uses machine learning models to predict WiFi usage patterns and revenue potential based on:
- Fleet characteristics (aircraft types, seat counts, services)
- Flight information (routes, load factors, duration)
- Pricing strategies (text, browse, stream packages)
- Revenue sharing agreements

## Features

- **Fleet Management**: Configure short-haul and long-haul fleet information
- **Flight Analysis**: Define flight routes with origin/destination regions
- **Pricing Models**: Set up tiered pricing for text, browse, and stream packages
- **Revenue Sharing**: Configure revenue splits between wifi service provider, airlines, and third-party WISPs
- **ML Predictions**: Uses trained models to predict usage (MB) and take rates (TR)
- **Authentication**: AWS Cognito integration for secure access
- **Interactive UI**: Bootstrap-based responsive web interface

## Project Structure

```
├── pyroi.py                 # Main Flask application
├── flaskrun.py             # Flask server runner with SSL support
├── config.py               # Application configuration
├── constant.py             # Constants and UI configuration
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup configuration
├── roiinput.py            # Input validation and data models
├── roioutput.py           # Output formatting and calculations
├── InputTranslation.py    # Data transformation and ML model execution
├── roiauth.py             # AWS Cognito authentication
├── exception.py           # Custom exception classes
├── model/                 # ML models and data files
│   ├── MB_model_fake.pkl  # Machine learning model for MB prediction
│   ├── TR_model_fake.pkl  # Machine learning model for take rate prediction
│   ├── Route_Translation.csv # Route region translation table
│   └── FOC_*.csv          # Fleet operation cost data
├── static/                # Static assets (CSS, JS, images)
├── templates/             # Jinja2 HTML templates
└── test/                  # Unit tests
```

## Installation

### Prerequisites

- Python 3.7+
- pip package manager
- SSL certificates (for HTTPS)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd wifi-pnl-calculator
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up SSL certificates**:
   - Place SSL certificate files in `keys/` directory:
     - `keys/server.crt`
     - `keys/server.key`

4. **Configure environment**:
   - Update AWS Cognito settings in [`constant.py`](constant.py:101)
   - Modify configuration in [`config.py`](config.py:3) as needed

## Usage

### Running the Application

1. **Development mode**:
   ```bash
   python pyroi.py -P 5000
   ```

2. **Production mode with Gunicorn**:
   ```bash
   export FLASK_APP=pyroi.py
   gunicorn -w 2 -b 127.0.0.1:5000 pyroi:app
   ```

3. **Background deployment**:
   ```bash
   nohup gunicorn -w 2 -b 127.0.0.1:5000 pyroi:app &
   ```

### Accessing the Application

- **Local development**: `https://127.0.0.1:5000/`
- **Development environment**: `https://roi-calculator-wifi-dev.nextcloud.aero/`
- **Production environment**: `https://roi-calculator-wifi.nextcloud.aero/`

### Using the Calculator

1. **Authentication**: Log in using AWS Cognito credentials
2. **Fleet Configuration**: 
   - Define short-haul and long-haul fleet characteristics
   - Specify aircraft types, counts, seat configurations
   - Select available services (IFE, TV, Phone, OneMedia)
3. **Flight Information**:
   - Configure flight routes by origin/destination regions
   - Set load factors and night flight percentages
4. **Pricing Setup**:
   - Define pricing for text, browse, and stream packages
   - Configure revenue sharing percentages
   - Set wholesale pricing per MB
5. **Generate Results**: Submit the form to get P&L analysis

## Key Components

### Data Models

- **[`RoiInput`](roiinput.py:18)**: Main input validation and data structure
- **[`RoiFleet`](roiinput.py:160)**: Fleet configuration management
- **[`RoiFlight`](roiinput.py:226)**: Flight information handling

### Machine Learning

- **[`InputTranslation.py`](InputTranslation.py:1)**: Data preprocessing and model execution
- **[`RunModel()`](InputTranslation.py:284)**: ML model prediction function
- Uses scikit-learn models for MB usage and take rate predictions

### Authentication

- **[`roiauth.py`](roiauth.py:1)**: AWS Cognito integration
- Session management with 120-minute timeout
- OAuth2 flow implementation

## Configuration

### Environment Settings

The application supports multiple environments configured in [`config.py`](config.py:23):
- `dev`: Development configuration
- `prod`: Production configuration (default)

### UI Configuration

Pricing ranges and validation rules are defined in [`constant.py`](constant.py:53):
- Text package: $0-20 (global range: $1.25-16)
- Browse package: $0-35 (global range: $4.9-22.74)  
- Stream package: $0-75 (global range: $8.9-69)

## Testing

Run the test suite:
```bash
python -m pytest test/
```

## API Endpoints

- **`/`**: Main application interface
- **`/output`**: P&L calculation results (POST)
- **`/session`**: Session status check
- **`/logout`**: User logout
- **`/logout_cognito`**: AWS Cognito logout

## Dependencies

Key dependencies include:
- **Flask 1.0.2**: Web framework
- **pandas 0.23.4**: Data manipulation
- **scikit-learn 0.20.2**: Machine learning
- **numpy 1.15.4**: Numerical computing
- **python-jose 3.0.1**: JWT handling for authentication

See [`requirements.txt`](requirements.txt:1) for complete dependency list.

## Security

- HTTPS enforced with SSL certificates
- AWS Cognito authentication
- Session management with secure tokens
- Input validation and sanitization

## Contributing

1. Follow the existing code structure and patterns
2. Add appropriate error handling using custom exceptions
3. Update tests for new functionality
4. Ensure proper input validation for user data

## Notes
This is a simplified version of an online ML system for demo purpose only. 
