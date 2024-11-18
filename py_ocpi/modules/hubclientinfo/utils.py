import requests

from py_ocpi.core.config import logger, settings


class HubTopologyHandler:
    def __init__(self, hub_url, party_id, country_code, token):
        self.hub_url = hub_url
        self.party_id = party_id
        self.country_code = country_code
        self.token = token
        self.headers = {"Authorization": f"Token {self.token}"}

    def register_with_hub(self):
        """Register this EMSP with the OCPI Hub."""
        registration_data = {
            "party_id": self.party_id,
            "country_code": self.country_code,
        }
        response = requests.post(
            f"{self.hub_url}/register",
            json=registration_data,
            headers=self.headers,
            timeout=30
        )
        return response.json() if response.status_code == 200 else None

    def route_message(self, endpoint, payload):
        """Route messages to other parties via the hub."""
        response = requests.post(  # nosec
            f"{self.hub_url}/{endpoint}",
            json=payload,
            headers=self.headers,
            timeout=30
        )
        return response.json() if response.status_code == 200 else None

    def handle_incoming_message(self, payload):
        """Handle incoming messages from the hub."""
        # Implement specific logic based on message type
        message_type = payload.get("type")
        if message_type == "COMMAND":
            return self.process_command(payload)
        # Other message types can be processed here
        return {"status": "Unknown message type"}

    def process_command(self, payload):
        """Process commands received from the hub."""
        command = payload.get("command")
        # Here you would add the specific command handling logic
        if command == "START_SESSION":
            return self.start_session(payload)
        if command == "STOP_SESSION":
            return self.stop_session(payload)
        return {"status": "Unknown command"}

    def start_session(self, payload):
        """Handle starting a session."""
        # Process the session start, likely involves interacting with the EVSE
        # or other systems.
        session_id = payload.get("session_id")
        # Placeholder response
        return {"status": f"Session {session_id} started successfully"}

    def stop_session(self, payload):
        """Handle stopping a session."""
        session_id = payload.get("session_id")
        # Placeholder response
        return {"status": f"Session {session_id} stopped successfully"}


def register_enapi_emsp_with_hub():
    """Register the EMSP with the hub and log the process."""
    logger.info("Starting registration with the hub...")
    handler = HubTopologyHandler(
        hub_url=settings.ENAPI_HUB_URL,
        party_id=settings.PARTY_ID,
        country_code=settings.COUNTRY_CODE,
        token=settings.ENAPI_HUB_TOKEN
    )
    response = handler.register_with_hub()
    if response:
        logger.info("Registration successful.")
    else:
        logger.error("Registration failed.")
    return response


def handle_incoming_command(handler, payload):
    """Handle an incoming command and log the outcome."""
    logger.info("Handling incoming command...")
    response = handler.handle_incoming_message(payload)
    if response.get("status") == "Unknown message type":
        logger.warning("Received unknown message type.")
    else:
        logger.info(f"Processed command successfully: {response}")
    return response


def send_message_via_hub(handler, endpoint, payload):
    """Send a message via the hub and log the outcome."""
    logger.info(f"Sending message to endpoint '{endpoint}'...")
    response = handler.route_message(endpoint, payload)
    if response:
        logger.info(f"Message sent successfully: {response}")
    else:
        logger.error("Failed to send message.")
    return response
