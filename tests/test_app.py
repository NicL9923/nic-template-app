import json
import os
import unittest
from unittest.mock import patch

import httpx2
from openai import AsyncOpenAI
from quartapp import create_app
from quart.testing.app import LifespanError


class AppTest(unittest.IsolatedAsyncioTestCase):
    async def test_startup_routes_stream_and_token(self):
        requests = []
        tokens = []
        async def token():
            tokens.append(True)
            return "fake-token"
        async def respond(request):
            requests.append(request)
            return httpx2.Response(200, headers={"content-type": "text/event-stream"}, content=(
                b'event: response.created\ndata: {"type":"response.created","sequence_number":0,"response":{"id":"resp_1","object":"response","created_at":1,"model":"test-deployment","output":[],"parallel_tool_calls":true,"tool_choice":"auto","tools":[]}}\n\n'
                b'data: [DONE]\n\n'))
        def client(**kwargs):
            return AsyncOpenAI(**kwargs, http_client=httpx2.AsyncClient(transport=httpx2.MockTransport(respond)))
        env = {"AZURE_OPENAI_ENDPOINT": "https://example.invalid/", "AZURE_OPENAI_CHAT_DEPLOYMENT": "test-deployment"}
        with patch.dict(os.environ, env), patch("quartapp.chat.get_bearer_token_provider", return_value=token) as provider, patch("quartapp.chat.AsyncOpenAI", side_effect=client):
            app = create_app(testing=True)
            async with app.test_app():
                web = app.test_client()
                self.assertEqual((await web.get('/')).status_code, 200)
                response = await web.post('/chat/stream', json={"input": "hello"})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.mimetype, 'application/x-ndjson')
                self.assertEqual(json.loads(await response.get_data())['type'], 'response.created')
                self.assertEqual(requests[0].headers['authorization'], 'Bearer fake-token')
                self.assertEqual(requests[0].url.path, '/openai/v1/responses')
                body = json.loads(requests[0].content)
                self.assertEqual((body['model'], body['input'], body['store']), ('test-deployment', 'hello', False))
                self.assertTrue(tokens)
                self.assertEqual(provider.call_args.args[1], 'https://cognitiveservices.azure.com/.default')

    async def test_missing_endpoint_fails_startup(self):
        with patch.dict(os.environ, {"AZURE_OPENAI_ENDPOINT": "", "AZURE_OPENAI_CHAT_DEPLOYMENT": "test"}):
            app = create_app(testing=True)
            with self.assertRaisesRegex(LifespanError, 'AZURE_OPENAI_ENDPOINT'):
                async with app.test_app():
                    pass
