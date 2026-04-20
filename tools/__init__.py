from tools.file_ops import create_file
from tools.code_gen import generate_and_write_code
from tools.summarizer import summarize_text
from tools.chat import general_chat
from tools.web_search import web_search

TOOL_MAP = {
    "create_file": create_file,
    "write_code": generate_and_write_code,
    "summarize": summarize_text,
    "general_chat": general_chat,
    "web_search": web_search,
}