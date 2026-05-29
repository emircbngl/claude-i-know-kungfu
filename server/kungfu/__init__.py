"""I Know KungFu — MCP server package.

The server is the *librarian*, not the brain: it stores, retrieves, structures,
dedupes, verifies, and benchmarks. It never calls an LLM. All judgment (deciding
what to fetch, distilling docs into cards, writing code) stays with Claude.
"""

__version__ = "0.1.0"
