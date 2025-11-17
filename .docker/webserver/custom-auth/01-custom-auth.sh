#!/bin/bash

# Check if custom authentication is already configured
if [ ! -f "/usr/src/paperless/src/paperless/custom_auth.py" ]; then
    echo "Setting up custom API key authentication..."

    # Copy custom authentication file
    cp /custom-cont-init.d/custom_auth.py /usr/src/paperless/src/paperless/

    # Modify Django settings to include API key authentication
    echo "from .custom_auth import APIKeyAuthentication" >> /usr/src/paperless/src/paperless/settings.py
    echo "REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].insert(0, 'paperless.custom_auth.APIKeyAuthentication')" >> /usr/src/paperless/src/paperless/settings.py

    echo "Custom API key authentication configured."
else
    echo "Custom API key authentication already configured, skipping setup."
fi

# s6-overlay will handle the rest of the startup process
