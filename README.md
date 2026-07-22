# Lumen App Service Azure OpenAI chat sample

This repository contains a Python Quart chat app used by Lumen's Web App create
template experience. The app calls Azure OpenAI with managed identity and streams
chat responses to a simple browser UI.

Lumen provisions Azure resources with its own ARM template and configures App
Service source control to deploy the application code from this repository.

## What's included

- `app.py` - App Service entry point for the Quart application.
- `quartapp/` - Chat backend, frontend templates, and static assets.
- `requirements.txt` and `gunicorn.conf.py` - Python dependencies and startup
  configuration for App Service source-control deployment.
- `.env.sample` - Local development environment variables.
- `docs/`, `infra/`, and `readme_diagram.png` - Upstream Azure Container Apps
  reference materials copied for learning and local experimentation.

## Lumen deployment behavior

When this sample is selected in Lumen:

1. Lumen collects the Web App values needed for the template.
2. Lumen deploys Azure resources through the portal create ARM template.
3. The ARM deployment configures `Microsoft.Web/sites/sourcecontrols` so App
   Service pulls this repository and deploys the Quart app code.

The upstream infrastructure files in this repository are not used by Lumen
create. They are included only as reference material. Editing `infra/` will not
change resources that Lumen already created.

## Required app settings

The app requires Azure OpenAI configuration before it can answer chat requests:

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_CHAT_DEPLOYMENT`
- `AZURE_TENANT_ID` for local development
- `AZURE_CLIENT_ID` when using a user-assigned managed identity

Lumen's AI template provisioning still needs to model the Azure OpenAI resource,
model deployment, managed identity permissions, and app settings before this
sample is fully runnable from the portal create flow.

## Run locally

Provision or reuse an Azure OpenAI resource, then copy `.env.sample` to `.env`
and fill in the values.

```shell
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m quart --app app run --port 50505 --reload
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Attribution

This sample is adapted from
[`Azure-Samples/openai-chat-app-quickstart`](https://github.com/Azure-Samples/openai-chat-app-quickstart),
the Azure OpenAI chat quickstart sample originally designed for Azure Container
Apps.
