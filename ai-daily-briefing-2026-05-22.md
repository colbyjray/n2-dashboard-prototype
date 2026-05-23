# AI Daily Briefing: May 22, 2026

Compiled from TLDR (AI, Dev, DevOps, IT, InfoSec, Marketing, Main) and Your Everyday AI newsletters.

---

## Executive Summary

Yesterday was one of the biggest days in AI news this year. The aftershocks from Google I/O dominated the conversation, OpenAI's Codex continued its quiet march toward becoming the dominant AI agent platform, and major deals reshaped the competitive landscape between Anthropic, Microsoft, and the Pentagon. Here is everything that happened.

---

## Major Headlines

### 1. Microsoft and Anthropic in Talks for AI Chip Deal

Microsoft plans to supply its custom Maia AI chips to Anthropic, which currently faces compute challenges despite existing partnerships with Amazon and Google. Microsoft invested $5 billion in Anthropic in November, and Maia chips offer roughly 30% improved performance. This signals Anthropic is aggressively diversifying its compute supply chain to keep up with demand.

Source: TLDR AI
Link: https://www.itpro.com/technology/artificial-intelligence/google-adds-ai-to-the-search-box

### 2. Cursor Hits $3 Billion Annual Revenue Run Rate

Cursor's annualized revenue hit $3 billion in late April, with more than 3,000 enterprise customers paying at least $100,000 per year. SpaceX has the right to buy Cursor for $60 billion during a 30-day window starting around its June 12 IPO. Cursor is now one of the fastest-growing startups in history. The company also shared detailed lessons from building cloud agents, covering durable execution, isolated dev environments, self-healing infrastructure, and cleaner separation between agent state and conversation state.

Source: TLDR AI

### 3. Google Turns Search Into an AI Agent Hub

Google is adding deeper AI features into Search, including an expanded AI-powered search box, Gemini 3.5 Flash powering AI Mode, personal context pulled from Gmail and Photos, and agent-like workflows for tasks. Enterprise search, personal productivity, and agent interfaces are collapsing into one surface. Google also started testing AI-generated ads in both standard search and AI Mode, with ads appearing below AI responses.

Source: TLDR IT, TLDR Main
Link: https://www.itpro.com/technology/artificial-intelligence/google-adds-ai-to-the-search-box

### 4. Gemini 3.5 Flash Becomes Google's New Best Model

In a surprise, Google's fastest model tier (Flash) outperformed Gemini 3.1 Pro on coding and agentic benchmarks while running four times faster than comparable frontier models. AI Mode in Google Search has already been silently upgraded. Note: the cheap Flash pricing from older generations is gone. Gemini 3.5 Pro arrives next month.

Source: Your Everyday AI

### 5. OpenAI Codex Gets Locked-Mac Control and "Appshots"

OpenAI's latest Codex update lets users send tasks from their phone and have the app use a Mac even when it is locked and the screen is off. The feature works through a Computer Use plugin with permission controls and a safeguard that instantly relocks the Mac if someone touches the keyboard. Codex also shipped "appshots," a quick way to capture a window plus its full text content, even offscreen content. OpenAI reported $5.7 billion in Q1 revenue.

Source: Your Everyday AI, TLDR AI

### 6. Trump Delays AI Executive Order

President Trump delayed a planned executive order on AI, saying he was not satisfied with parts of it. The order would have allowed the government to review AI models ahead of time to spot security risks. He said he wants to protect the U.S. lead over China in AI and avoid any policy that might slow the industry down.

Source: Your Everyday AI

### 7. Pentagon Tests AI Rivals to Replace Claude

The Pentagon is actively testing AI models from other major vendors to replace Anthropic's Claude after the Defense Department cut ties over a supply-chain risk designation. 25 department power users began evaluating alternative tools in early March. OpenAI and Google are under review. The Pentagon is building a broader AI bench rather than relying on a single provider.

Source: Your Everyday AI

### 8. DeepSeek Nears $10 Billion Funding Round

DeepSeek is in the final stretch of a roughly $10 billion funding round, with interest from Tencent, IDG Capital, NetEase, JD.com, and a state-backed AI fund. The deal could value DeepSeek at about $45 billion. The startup says it will prioritize advanced AI research and AGI over quick commercialization.

Source: Your Everyday AI

### 9. Manus Must Unwind Meta Takeover

Chinese regulators have told Manus to unwind its acquisition by Meta. The founders now need to raise funds to buy back the operation and are in discussions for roughly $1 billion in funding. A reversal of a deal this large months after completion is virtually unheard of.

Source: TLDR AI

### 10. Marc Andreessen Says AI Has Already Hit AGI

Marc Andreessen claims frontier AI models have already crossed into AGI territory, saying the latest systems now outperform most human experts on most questions. He argued that AI companies are underselling their own progress and that coding agents are radically boosting productivity.

Source: Your Everyday AI

---

## AI Product and Platform Updates

### Google I/O Aftermath: Chrome's "Agentic Web" Vision
Chrome unveiled 15 updates at Google I/O focused on three areas: giving AI agents more capabilities, improving web performance, and integrating Gemini to make the browser a proactive assistant. Key announcements include the WebMCP standard, dedicated DevTools for agents, on-device AI with Gemma 197M, and upcoming consumer features like image editing and Gemini integration on Android.

Source: TLDR Dev
Link: https://developer.chrome.com

### Google Unifies AI Coding Tools Under "Antigravity"
Google is consolidating its AI coding tools (IDE, CLI, SDK, and agent tooling) into a single platform called Antigravity for developers building AI-assisted software workflows.

Source: TLDR IT
Link: https://www.infoworld.com/article/4175416/google-to-unify-ai-coding-tools-under-antigravity.html

### ChatGPT Now Lives Inside Microsoft PowerPoint
ChatGPT is now a native add-in inside PowerPoint, pulling directly from Gmail, Outlook, and SharePoint to build slides from your actual work. Outputs stay fully editable. This mostly flew under the radar because Codex dominated the news cycle.

Source: Your Everyday AI

### Claude Compliance API
Anthropic's Claude now pushes chat, file, and activity data into 28 popular security and compliance platforms via a new Compliance API.

Source: Your Everyday AI

### Anthropic's New Consulting Venture
Anthropic's unnamed consulting venture made its first acquisition, picking up Fractional AI as its operational centerpiece.

Source: TLDR AI

### Qwen3.7-Max Released
Alibaba's Qwen team released Qwen3.7-Max, a proprietary agent-foundation model posting top scores on Terminal-Bench 2.0, SWE-Pro, SciCode, MCP-Mark, GPQA Diamond, and multiple math benchmarks.

Source: TLDR AI

### Hitachi Partners with Anthropic for "Lumada 3.0"
Hitachi announced a strategic partnership with Anthropic to strengthen its Lumada 3.0 initiative, combining Hitachi's domain expertise with Anthropic's AI for safe, real-world deployment of physical AI.

Source: TLDR IT

### Salesforce Makes Informatica Tools API-Callable
Salesforce is making Informatica's data integration, governance, and quality tools callable through APIs, letting developers and AI systems access governed enterprise data directly in workflows.

Source: TLDR IT

### Spotify AI Podcasts
Spotify is making podcasts more interactive and personal with in-episode Q&A, creator Memberships, and AI-generated Personal Podcasts.

Source: Your Everyday AI

### Amazon Alexa+ Going After NotebookLM
Amazon is hoping to replicate NotebookLM's success to get Alexa+ off the ground.

Source: Your Everyday AI

---

## AI Security and Threats

### Megalodon: Mass GitHub Repo Backdooring
An automated campaign pushed 5,718 malicious commits to 5,561 GitHub repositories in a six-hour window, injecting GitHub Actions workflows with payloads that exfiltrate CI secrets, cloud credentials, SSH keys, and OIDC tokens. The compromise cascaded to npm via poisoned publishes.

Source: TLDR InfoSec

### GitHub Actions Cache Poisoning Spreading
GitHub Actions cache poisoning lets attackers write poisoned dependency caches that later run inside high-privilege publish workflows. Seen in Angular, tj-actions, Cline, and TanStack incidents.

Source: TLDR InfoSec

### Zscaler Acquires Symmetry Systems
Zscaler acquired Symmetry Systems to track how AI agents interact with sensitive enterprise data, strengthening AI security with data-layer visibility on their Zero Trust platform.

Source: TLDR IT

### Prempti: Policy for AI Coding Agents
Prempti is a new experimental security tool that monitors and controls AI coding agents like Claude Code by intercepting their file reads, shell commands, and other actions before execution using policy-based rules.

Source: TLDR DevOps

### AI Reshapes Cybersecurity Workforce
Two new workforce research reports say enterprises are accelerating AI security training. Key concerns include prompt injection, model exploitation, agentic AI hijacking, and AI-powered social engineering.

Source: TLDR IT

---

## AI and Marketing

### Google AI-Generated Ads in Search
Google started testing AI-generated ads for brands and products below AI Mode responses and direct discount offers in standard search results. The ads will not appear in Gemini for now.

Source: TLDR Main

### Chrome Lighthouse Will Audit for AI Readiness
Chrome's Lighthouse will check for a machine-readable summary at the domain root (interpreted as llms.txt) as part of evaluating AI readiness. This has direct implications for SEO and AI search optimization.

Source: TLDR Marketing

### AI Search Readiness and LLM Citation Behavior
Free ChatGPT over-indexes on Reddit while paid ChatGPT leans toward editorial publishers. Brand visibility shifts across ChatGPT and API environments. Logged-in experiences favor earned media while the API skews toward retail and product pages.

Source: TLDR Marketing

### AI-Generated Ads Outperform When Disguised as Human
AI-generated ads match human performance overall, but ads that look human-made drive the highest click-through rates. When ads are recognized as AI, performance drops. Perception matters more than origin.

Source: TLDR Marketing

### B2B Buyers Trust AI Less Than Marketers Think
Nearly half of B2B buyers use generative AI to research vendors, but more than half have encountered misleading information and 69% still rely on sales reps to validate findings.

Source: TLDR Marketing

### Chrome's Prompt API for On-Device AI
Chrome's Prompt API allows webpages to run Gemini Nano locally with one line of JavaScript, without API costs. Best use cases: rewriting, scoring, and short passage summarization.

Source: TLDR Marketing

---

## Industry and Workforce Trends

### The Rise of Forward Deployed Engineers
Demand for Forward Deployed Engineers (FDEs) is growing at Google, OpenAI, and Anthropic, but the role now acts more like a solutions architect focused on integration and client management. OpenAI and Anthropic are creating separate deployment entities.

Source: TLDR Dev

### Coding Agents Causing Decision Fatigue
AI coding agents have shifted engineering from manual writing to intensive decision-making and review, resulting in increased work density and decision fatigue. This requires redesigning the development lifecycle.

Source: TLDR Dev

### AI's Plummeting Prices Are a Software Story
Open-weight models running on older commodity hardware are becoming competitive with frontier models. Many applications do not need the best models, which has big implications for what frontier labs can charge.

Source: TLDR AI

### Cisco Updates Certifications for AI Era
Cisco is updating core certification tracks to require AI, automation, and infrastructure skills alongside traditional networking fundamentals.

Source: TLDR IT

### ClickUp Cuts 22% of Staff, Plans AI-Driven Million-Dollar Salary Bands
ClickUp cut 22% of its staff and plans to introduce million-dollar salary bands for employees who create outsized impact using AI.

Source: TLDR Main

### Nvidia Vera CPUs for Agentic AI
Nvidia's ARM-based Vera CPUs are purpose-built for Agentic AI and inference, and are projected to hit $20 billion revenue this year.

Source: TLDR Main

---

## Need-to-Know Items for Your Role

These are prioritized for a digital marketing agency leader who needs to stay ahead of AI developments affecting clients, strategy, and operations.

### Tier 1: Act on This Week

1. **Google AI Ads Are Live in AI Mode** - Google is testing AI-generated ads below AI Mode responses. If you manage Google Ads for clients, monitor how these new ad formats appear and whether they affect existing campaign performance. Start thinking about how AI Mode ad creative differs from traditional search ads.
   - Link: https://www.itpro.com/technology/artificial-intelligence/google-adds-ai-to-the-search-box

2. **Chrome Lighthouse Now Checks for llms.txt** - Chrome's Lighthouse will audit domains for a machine-readable summary (llms.txt) as part of AI readiness. Start implementing llms.txt for client websites to ensure visibility in AI-powered search and agent browsing.
   - Link: https://developer.chrome.com

3. **Google Search Is Becoming an AI Agent Hub** - Google Search now uses Gemini 3.5 Flash in AI Mode with personal context from Gmail and Photos. This fundamentally changes how users discover brands. Review client SEO strategies for AI-first search behavior.
   - Link: https://www.itpro.com/technology/artificial-intelligence/google-adds-ai-to-the-search-box

4. **AI-Generated Ads Perform Best When They Look Human** - Research shows AI ads that appear human-made drive the highest CTR, but performance drops when recognized as AI. This should inform how you use AI in creative production for clients.

### Tier 2: Brief Your Team This Month

5. **ChatGPT Is Now Native in PowerPoint** - This directly speeds up client presentation and pitch deck creation. Ensure your team knows it pulls from Gmail, Outlook, and SharePoint.

6. **LLM Citation Behavior Differs by Access Point** - Free ChatGPT over-indexes Reddit; paid ChatGPT favors editorial publishers. This affects GEO (Generative Engine Optimization) strategy for clients.

7. **B2B Buyers Use AI to Research But Don't Fully Trust It** - 69% still rely on sales reps to validate AI-found information. Factor this into client B2B marketing strategies.

8. **Cursor at $3B ARR; Codex Running Autonomously** - The AI coding tools landscape is moving fast. If your agency builds web properties, evaluate whether Cursor or Codex can accelerate development workflows.

9. **Chrome's Prompt API Enables On-Device AI** - Webpages can now run Gemini Nano locally with one line of JavaScript. Explore lightweight AI features (rewriting, scoring, summarization) that could differentiate client websites.
   - Link: https://developer.chrome.com

### Tier 3: Stay Aware

10. **Trump Delayed the AI Executive Order** - Regulatory uncertainty continues. No immediate action needed but watch for the order's final form, especially any provisions around AI-generated content labeling that could affect marketing.

11. **DeepSeek Raising $10B; Manus Forced to Unwind Meta Deal** - Geopolitical dynamics in AI are intensifying. This affects long-term model selection and client data sovereignty considerations.

12. **Megalodon GitHub Attack Hit 5,700+ Repos** - If your agency uses GitHub Actions or open-source dependencies, audit workflows and rotate secrets exposed to CI runners.

13. **Spotify Launching AI Podcasts** - New content format opportunity for clients. Interactive Q&A and AI-generated personal podcasts could become a marketing channel.

14. **ClickUp Cuts Staff, Plans AI-Driven Compensation** - Signal of broader trend: companies restructuring around AI productivity. Watch for similar moves across marketing tech vendors.

---

Sources: TLDR AI, TLDR Dev, TLDR DevOps, TLDR IT, TLDR InfoSec, TLDR Marketing, TLDR Main, Your Everyday AI - all from May 22, 2026.
