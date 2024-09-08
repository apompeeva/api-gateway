import os

from dotenv import load_dotenv

load_dotenv()

JAEGER_AGENT_HOST = os.environ.get('JAEGER_AGENT_HOST', 'localhost')
JAEGER_AGENT_PORT = int(os.environ.get('JAEGER_AGENT_PORT', '6831'))
