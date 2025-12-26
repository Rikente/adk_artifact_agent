import os

from dotenv import load_dotenv
load_dotenv(override = True)

from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.tools import ToolContext
from google.adk.tools.load_artifacts_tool import load_artifacts_tool

instruction = """
You are a helpful assistant.
When the user interacts with you, you will invoke your "save_artifact" tool to save an artifact for them.
"""

async def save_artifact(tool_context: ToolContext) -> str:
    """
    Save an artifact for the user.
    """
    string_to_save = 'This is the test string to save as a text artifact.'
    bytes_to_save = string_to_save.encode('utf-8')
    artifact_part = types.Part(
        inline_data = types.Blob(
            mime_type = 'text/plain',
            data = bytes_to_save,
        )
    )
    version_number = await tool_context.save_artifact('test_artifact', artifact_part)
    return f"Artifact saved with version number: {version_number}"

root_agent = LlmAgent(
    name = 'root_agent',
    model = 'gemini-2.5-flash',
    instruction = instruction,
    tools = [
        load_artifacts_tool, save_artifact
    ]
)