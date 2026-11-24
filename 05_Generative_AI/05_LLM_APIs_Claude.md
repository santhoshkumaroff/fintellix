# LLM APIs – Claude (JD: "LLM APIs (such as Claude)")

> Check the latest model names at docs.anthropic.com before the interview. Model IDs change. The examples use `claude-sonnet-5-5`.

### Q1. How do you call Claude from Python?
```python
# pip install anthropic
import os
from anthropic import Anthropic

client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])   # or just Anthropic() – reads env var

msg = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=400,
    temperature=0,
    system="You are a banking regulatory assistant. Be concise.",
    messages=[{"role": "user", "content": "Explain SMA-0, SMA-1, SMA-2 in a table."}],
)
print(msg.content[0].text)
print(msg.usage.input_tokens, msg.usage.output_tokens)   # for cost tracking
```
- **Example 2:** Wrap this in a function `ask(prompt, system)` with retry and logging, and reuse it everywhere.

### Q2. What is the structure of the Messages API?
**Answer:**
- `model`, `max_tokens` (required)
- `system`: system prompt (a separate parameter, not a message)
- `messages`: a list of alternating `{"role": "user" | "assistant", "content": ...}`
- Optional: `temperature`, `top_p`, `stop_sequences`, `tools`, `stream`, `metadata`
- The response has `content` (a list of blocks: text, tool_use), `stop_reason` (`end_turn`, `max_tokens`, `tool_use`, `stop_sequence`) and `usage`.
- **Example 1:** If `stop_reason == "max_tokens"`, the answer was cut off. Increase `max_tokens` or ask for a shorter answer.
- **Example 2:** A multi-turn chat: append the assistant reply and the next user message to `messages` and call again (the API is **stateless**, so you send the history every time).

### Q3. How do you keep a conversation (multi-turn)?
```python
history = []
def chat(user_text):
    history.append({"role": "user", "content": user_text})
    resp = client.messages.create(model="claude-sonnet-5-5", max_tokens=500, messages=history)
    reply = resp.content[0].text
    history.append({"role": "assistant", "content": reply})
    return reply
chat("What is LCR?"); chat("Give an example with numbers.")
```
- **Example 2:** For long chats, summarise the old turns into one message to save tokens.

### Q4. What is streaming and why use it?
**Answer:** You receive tokens as they're generated instead of waiting for the full answer, which gives better UX in chatbots.
```python
with client.messages.stream(model="claude-sonnet-5-5", max_tokens=500,
        messages=[{"role": "user", "content": "Summarise Basel III"}]) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```
- **Example 2:** A Streamlit chat UI that shows the answer typing out live.

### Q5. What is tool use (function calling) with Claude?
**Answer:** You describe tools with a name, a description and a JSON input schema. Claude may respond with a `tool_use` block. Your code executes the tool and sends back a `tool_result`. Claude then writes the final answer.
```python
tools = [{
    "name": "get_npa_amount",
    "description": "Get total NPA outstanding for a branch and month",
    "input_schema": {
        "type": "object",
        "properties": {"branch": {"type": "string"}, "month": {"type": "string", "description": "YYYY-MM"}},
        "required": ["branch", "month"],
    },
}]
resp = client.messages.create(model="claude-sonnet-5-5", max_tokens=500, tools=tools,
        messages=[{"role": "user", "content": "NPA amount for MUM in Oct 2026?"}])
if resp.stop_reason == "tool_use":
    call = next(b for b in resp.content if b.type == "tool_use")
    result = get_npa_amount(**call.input)            # your Python function (SQL inside)
    final = client.messages.create(model="claude-sonnet-5-5", max_tokens=500, tools=tools,
        messages=[
            {"role": "user", "content": "NPA amount for MUM in Oct 2026?"},
            {"role": "assistant", "content": resp.content},
            {"role": "user", "content": [{"type": "tool_result", "tool_use_id": call.id, "content": str(result)}]},
        ])
    print(final.content[0].text)
```
- **Example 2:** A `create_jira_ticket` tool lets the assistant log a data-quality issue it found (with human approval before execution).

### Q6. How do you handle errors, rate limits and retries?
**Answer:** Catch API errors (rate limit 429, overloaded 529, timeouts, 5xx) and retry with **exponential backoff + jitter**. Don't retry 4xx validation errors. The SDK has built-in retries (`max_retries`). Set timeouts.
```python
import anthropic, time, random
def safe_call(**kwargs):
    for attempt in range(5):
        try:
            return client.messages.create(**kwargs)
        except (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.InternalServerError):
            time.sleep((2 ** attempt) + random.random())
    raise RuntimeError("LLM call failed after retries")
```
- **Example 2:** A batch job over 5,000 documents uses a limited worker pool to stay under the rate limits.

### Q7. How do you control cost?
**Answer:** Choose the smallest model that meets the accuracy bar (Haiku for simple classification, Sonnet for most work, Opus for the hardest reasoning). Trim context with RAG. Use **prompt caching** for repeated prefixes. Use the **Batch API** for non-urgent bulk jobs (cheaper, asynchronous). Cap `max_tokens`. Cache identical answers. Track `usage` per call.
- **Example 1:** Classifying 50,000 complaints overnight → a small model via the Batch API.
- **Example 2:** A 15k-token schema prompt for text-to-SQL → prompt caching cuts repeated input cost.

### Q8. Claude model family – which one when?
**Answer:** The tiers trade capability against speed and cost: **Haiku** (fast, cheap), **Sonnet** (balanced, the default for most apps), **Opus** (most capable for complex reasoning). Check current versions and pricing in the docs.
- **Example 1:** Real-time FAQ bot → Sonnet or Haiku.
- **Example 2:** Analysing a complex new regulation and mapping its impact → Opus or a reasoning mode.

### Q9. How can banks access Claude securely?
**Answer:** Directly through the Anthropic API (with enterprise data terms), or through cloud platforms such as **Amazon Bedrock**, **Google Cloud Vertex AI** or **Microsoft Foundry**, inside the bank's existing cloud agreements and region controls. Plus internal controls: PII masking, logging, approval workflows.
- **Example 1:** A bank already on AWS uses Claude via Bedrock in its approved region.
- **Example 2:** A gateway service strips account numbers before any prompt leaves the network.

### Q10. How do you make outputs deterministic and testable?
**Answer:** Temperature 0, fixed prompts in version control, structured output with validation, seeded test sets, and comparing against expected answers with tolerance (exact match for fields, semantic match or LLM-as-judge for prose).
- **Example 1:** An extraction test: `assert result.circular_no == "RBI/2024-25/16"`.
- **Example 2:** A summary test: the judge checks it mentions the effective date and the applicable entities.

### Q11. What are Claude's notable capabilities to mention?
- Long context windows; strong at reading long documents
- Vision: images, charts, PDFs
- Tool use, structured outputs, extended thinking
- Prompt caching, Batch API, streaming
- Agent tooling (Claude Agent SDK, MCP) and Claude Code for coding
- **Example 1:** Upload a scanned PDF return → Claude extracts the table to JSON.
- **Example 2:** Use Claude Code to write unit tests for a reconciliation script.

### Q12. How would you use AI-assisted tools in daily work? (JD: "AI-assisted tools")
**Answer:** Use coding assistants (Claude Code, Copilot) to write boilerplate, tests, regex and SQL faster, and to explain unfamiliar code. **Always review and test the generated code**, and never paste confidential client data into unapproved tools.
- **Example 1:** "Write a pandas function that reconciles two files on account_id and outputs breaks". Review it, add tests, then use it.
- **Example 2:** Ask the assistant to explain a 500-line legacy stored procedure before modifying it.
