"""All 20 AI agent profiles for Code Council Bot."""

from agents.base import AgentProfile

AGENT_PROFILES: list[AgentProfile] = [
    # === OPENAI AGENTS ===
    AgentProfile(
        name="GPT-4o",
        emoji="\U0001f9e0",
        provider="openai",
        model_override="gpt-4o",
        specialization="Universal full-stack development",
        coding_style="Clean, well-documented, follows official conventions",
        strengths=["full-stack", "API design", "system architecture", "debugging"],
    ),
    AgentProfile(
        name="Codex",
        emoji="\U0001f4bb",
        provider="openai",
        model_override="gpt-4o-mini",
        specialization="Rapid code generation and completion",
        coding_style="Fast, minimal, efficient code",
        strengths=["code completion", "boilerplate generation", "quick prototyping"],
    ),
    AgentProfile(
        name="GitHub Copilot",
        emoji="\U0001f916",
        provider="openai",
        model_override="gpt-4o",
        specialization="Context-aware code suggestions",
        coding_style="Matches surrounding code patterns, IDE-friendly",
        strengths=["autocomplete", "pattern matching", "test generation"],
    ),

    # === ANTHROPIC AGENTS ===
    AgentProfile(
        name="Claude",
        emoji="\U0001f3af",
        provider="anthropic",
        model_override="claude-sonnet-4-20250514",
        specialization="Deep reasoning and complex architecture",
        coding_style="Thorough, well-reasoned, safety-conscious",
        strengths=["complex logic", "security", "code review", "architecture"],
    ),
    AgentProfile(
        name="Devin",
        emoji="\U0001f477",
        provider="anthropic",
        model_override="claude-sonnet-4-20250514",
        specialization="Autonomous software engineering",
        coding_style="Full project awareness, systematic approach",
        strengths=["project setup", "debugging", "end-to-end development"],
    ),

    # === GOOGLE AGENTS ===
    AgentProfile(
        name="Gemini Pro",
        emoji="\U0001f48e",
        provider="google",
        model_override="gemini-2.5-pro",
        specialization="Large context code understanding",
        coding_style="Google-style, comprehensive, well-tested",
        strengths=["large codebases", "multimodal", "documentation"],
    ),

    # === DEEPSEEK AGENTS ===
    AgentProfile(
        name="DeepSeek Coder",
        emoji="\U0001f50d",
        provider="deepseek",
        model_override="deepseek-coder",
        specialization="Code generation and understanding",
        coding_style="Clean, functional, algorithmic",
        strengths=["algorithms", "data structures", "competitive programming"],
    ),

    # === MISTRAL AGENTS ===
    AgentProfile(
        name="Codestral",
        emoji="\u2b50",
        provider="mistral",
        model_override="codestral-latest",
        specialization="Fast code generation",
        coding_style="European engineering precision, fast and efficient",
        strengths=["speed", "multilingual code", "efficient algorithms"],
    ),

    # === TOGETHER/OPEN-SOURCE AGENTS ===
    AgentProfile(
        name="CodeLlama",
        emoji="\U0001f999",
        provider="together",
        model_override="meta-llama/CodeLlama-70b-Instruct-hf",
        specialization="Code infilling and generation",
        coding_style="Meta-style, practical, production-ready",
        strengths=["code infilling", "large files", "Python/C++"],
    ),
    AgentProfile(
        name="StarCoder",
        emoji="\u2728",
        provider="together",
        model_override="bigcode/starcoder2-15b-instruct-v0.1",
        specialization="Multi-language code generation",
        coding_style="Open-source community style, diverse languages",
        strengths=["multi-language", "code search", "documentation"],
    ),

    # === GROQ AGENTS (FAST INFERENCE) ===
    AgentProfile(
        name="Llama 3.3",
        emoji="\u26a1",
        provider="groq",
        model_override="llama-3.3-70b-versatile",
        specialization="Fast general-purpose coding",
        coding_style="Practical, modern, well-structured",
        strengths=["speed", "general coding", "scripting"],
    ),

    # === OPENROUTER AGENTS ===
    AgentProfile(
        name="Qwen Coder",
        emoji="\U0001f3ef",
        provider="openrouter",
        model_override="qwen/qwen-2.5-coder-32b-instruct",
        specialization="Code generation and editing",
        coding_style="Alibaba engineering, robust, scalable",
        strengths=["Chinese/English code", "web development", "scalability"],
    ),
    AgentProfile(
        name="Cursor AI",
        emoji="\U0001f5b1\ufe0f",
        provider="openrouter",
        model_override="anthropic/claude-sonnet-4-20250514",
        specialization="IDE-integrated code editing",
        coding_style="Edit-focused, diff-aware, refactoring expert",
        strengths=["refactoring", "code editing", "codebase navigation"],
    ),
    AgentProfile(
        name="Replit AI",
        emoji="\U0001f4e6",
        provider="openrouter",
        model_override="google/gemini-2.5-pro-preview",
        specialization="Online development and deployment",
        coding_style="Full-stack, deployment-ready, cloud-native",
        strengths=["full-stack", "deployment", "rapid prototyping"],
    ),
    AgentProfile(
        name="Codeium",
        emoji="\U0001f680",
        provider="openrouter",
        model_override="deepseek/deepseek-coder",
        specialization="Free code completion and search",
        coding_style="Fast, context-aware, lightweight",
        strengths=["code search", "autocomplete", "fast suggestions"],
    ),
    AgentProfile(
        name="Phind",
        emoji="\U0001f50e",
        provider="openrouter",
        model_override="qwen/qwen-2.5-coder-32b-instruct",
        specialization="Developer search and code generation",
        coding_style="Research-backed, documentation-heavy, thorough",
        strengths=["research", "documentation", "API integration"],
    ),
    AgentProfile(
        name="Tabnine",
        emoji="\U0001f4d1",
        provider="openrouter",
        model_override="meta-llama/llama-3.3-70b-instruct",
        specialization="Local and cloud code completion",
        coding_style="Privacy-focused, team-aware, consistent",
        strengths=["team patterns", "privacy", "code consistency"],
    ),
    AgentProfile(
        name="JetBrains AI",
        emoji="\U0001f3d7\ufe0f",
        provider="openrouter",
        model_override="google/gemini-2.5-pro-preview",
        specialization="IDE-native code assistance",
        coding_style="IntelliJ-style, strongly typed, refactoring-friendly",
        strengths=["Java/Kotlin", "refactoring", "type safety"],
    ),
    AgentProfile(
        name="Sourcegraph Cody",
        emoji="\U0001f4da",
        provider="openrouter",
        model_override="anthropic/claude-sonnet-4-20250514",
        specialization="Large codebase understanding",
        coding_style="Context-rich, cross-repo aware, precise",
        strengths=["large codebases", "code search", "cross-repo context"],
    ),
    AgentProfile(
        name="Aider",
        emoji="\U0001f6e0\ufe0f",
        provider="openrouter",
        model_override="anthropic/claude-sonnet-4-20250514",
        specialization="Git-integrated terminal coding",
        coding_style="Terminal-native, git-aware, diff-based",
        strengths=["git integration", "terminal workflow", "incremental edits"],
    ),
]


def get_agents_by_provider(provider: str) -> list[AgentProfile]:
    return [a for a in AGENT_PROFILES if a.provider == provider]


def get_agent_by_name(name: str) -> AgentProfile | None:
    for agent in AGENT_PROFILES:
        if agent.name == name:
            return agent
    return None
