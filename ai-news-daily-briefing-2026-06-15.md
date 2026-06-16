# AI News Daily Briefing - June 15, 2026

Sources: TLDR (Main, AI, InfoSec, IT, Dev, DevOps, Data, Marketing) and Your Everyday AI

---

## THE BIGGEST STORIES OF THE DAY

### 1. Anthropic's Fable 5 and Mythos 5 Shut Down by US Government

The dominant story across every newsletter yesterday. The US Commerce Department issued a directive subjecting Anthropic's newest and most capable models, Fable 5 and Mythos 5, to export controls restricting their use outside the US. Rather than attempting nationality-based filtering, Anthropic disabled both models globally for all users.

Key details:
- Amazon CEO Andy Jassy reportedly flagged security concerns to US officials, telling them Amazon researchers had used prompts to get Fable 5 to surface information useful for cyberattacks
- The Trump administration gave Anthropic a 90-minute deadline to disable the models
- Anthropic argues the vulnerabilities Amazon flagged are "relatively basic" and that other publicly available models can also discover them
- Microsoft reportedly banned Fable 5 use internally
- Anthropic is set to meet with White House officials next week to resolve the dispute
- The government also imposed mandatory 30-day data retention on Anthropic
- A security analysis argues banning capable models hurts overburdened cybersecurity teams more than it prevents attacks, since these models help defenders fix bugs and remediate vulnerabilities at scale

This is the first time a US government export-control directive has been used to force an AI company to pull a model from production worldwide.

### 2. Elon Musk Becomes the World's First Trillionaire

SpaceX went public on Friday, with shares rising 20% from their IPO price of $135, pushing Elon Musk's net worth past $1 trillion. His wealth is now equivalent to more than 3% of US GDP and five million times the typical US family's net worth. SpaceX President Gwynne Shotwell floated the possibility of a future Tesla merger.

### 3. Meta Separating from Manus After Beijing's Divestiture Order

Meta has begun unwinding its reported $2 billion acquisition of Chinese-founded AI startup Manus, cutting it off from internal systems and halting data sharing. Beijing issued a national security order requiring the divestiture. Manus founders are exploring raising about $1 billion to reclaim the company.

### 4. Salesforce Acquiring Fin for $3.6 Billion

Salesforce announced it will acquire Fin, an AI customer service startup, for approximately $3.6 billion. Fin's AI Agent handles customer inquiries across chat, email, WhatsApp, text, phone, and Slack. This bolsters Salesforce's Agentforce product strategy.

### 5. Goldman Sachs: AI Infrastructure Spending Could Hit $1.4 Trillion by 2027

Goldman Sachs raised its AI infrastructure spending forecast to $1.1 trillion base case and $1.4 trillion in a bullish 2027 scenario, reflecting surging demand for cloud capacity, chips, data centers, and power.

### 6. OpenAI Partner Network and IPO Preparations

OpenAI announced a $150 million Partner Network to help enterprises turn its models into business results. The program aims to train 300,000 certified consultants by end of 2026. OpenAI is also reportedly preparing for a potential trillion-dollar IPO.

---

## AI MODEL AND PRODUCT LAUNCHES

- **GLM-5.2** from Z.ai: New flagship coding model, available to GLM Coding Plan users. Will be open-sourced under MIT License. API and chatbot launching next week.
- **Kimi K2.7 Code**: 1 trillion parameter Mixture-of-Experts coding model from Moonshot with stronger end-to-end task completion and improved token efficiency.
- **Google Skills Marketplace for Gemini Business**: Pre-defined, Google-optimized skills to help teams build dashboards and reporting tools without long engineering delays.
- **AWS FinOps Agent (Public Preview)**: Agentic AI tool that investigates cloud cost anomalies and answers cost questions for engineering teams.
- **Databricks Omnigent**: Open-source meta-harness that makes agents like Claude Code, Codex, and custom agents work together through one shared layer with security and cost controls.
- **Databricks Zerobus Ingest (GA)**: Serverless streaming service that ingested 1 petabyte in under 24 hours at 12 GB/s throughput, eliminating need for Kafka.
- **MotherDuck Flights**: Agent-native data pipeline feature letting AI agents build, run, and schedule ingestion workloads.
- **OpenRouter Fusion**: New API that mixes multiple AI models for smarter, cheaper results.
- **Google AI Threat Defense**: Always-on security platform using Mandiant telemetry, Wiz cloud scanning, and Gemini-based tools.
- **Open Knowledge Format**: Open specification formalizing the LLM-wiki pattern into a portable, vendor-neutral format for AI systems.

---

## CYBERSECURITY NEWS

- **Splunk Pre-Auth RCE** (CVE-2026-20253, CVSS 9.8): Unauthenticated attackers can access Splunk Enterprise's PostgreSQL Sidecar Service, achieving remote code execution. Affects versions 10.0.0-10.0.6 and 10.2.0-10.2.3. Update immediately.
- **LangGraph RCE Flaws**: Three chained vulnerabilities in LangGraph's persistence layer (50M+ monthly downloads) enable SQL injection to RCE via unsafe msgpack deserialization. Patch to langgraph-checkpoint-sqlite 3.0.1+.
- **Novo Nordisk Cyberattack**: Attackers accessed pseudonymized clinical trial records. Targeted phishing campaigns using stolen contact details are now in progress.
- **Arch Linux AUR Packages Hijacked**: ~1,500 Arch User Repository packages compromised with eBPF-based rootkit malware via malicious npm dependency.
- **Microsoft June Patch Tuesday**: Record-breaking ~200 vulnerabilities patched including multiple zero-days and critical issues.
- **CISA 3-Day Patch Deadline**: New directive requires federal agencies to remediate highest-risk flaws within three days.
- **npm 12 Security Changes**: GitHub will disable install-time scripts, Git-based dependency fetching, and remote URL downloads by default.

---

## AI INDUSTRY TRENDS AND ANALYSIS

### Bot Traffic Now Exceeds Human Traffic
Bot traffic accounts for about 57% of web page requests on Cloudflare's network. Agent and agentic browser traffic is up nearly 8,000% in 2025. AI agents are now a primary audience layer for websites.

### Uber's AI Budget Blowout
Claude Code adoption hit 84% across Uber's 5,000 engineers, exhausting the annual AI budget by mid-April. The lesson: agentic AI is a task-economics problem, not a token-pricing problem. Teams need to measure value per task and control context costs.

### AI Won't Replace Software Engineers
Multiple analyses conclude AI automates only the "execute" phase of the "decide-execute-deliver" workflow. Job cuts attributed to AI are frequently financial pressures or post-pandemic corrections. The edge shifts to experts who steer the model and maintain systems.

### Marketing Teams Going AI-First
Marketing teams are becoming leaner and more generalist, functioning like creative studios rather than production pipelines. AI handles execution while humans focus on strategy, narrative, and taste. Differentiation comes from curated signals over volume.

### The Clearinghouse Model for AI Agents
Durable AI-era moats will come from becoming the "clearinghouse" for autonomous agents, governing memory, context, execution, and governance/audit across vendor ecosystems.

### Apple's New Siri
Apple's Siri update makes it roughly competitive with where leading chatbots were about six months ago. The new iOS 27 beta contains an Extensions system for third-party AI with a settings panel and dedicated App Store section.

### Meta's AI Team Revolt
Meta's Applied AI team is reportedly on the verge of revolt. A live-streamed employee-only presentation was interrupted with an expletive-laden meltdown targeting a senior executive. Employees say they were forced into the group and describe the work as "soul-crushing."

### Jeff Bezos's Prometheus Raises $12B
Jeff Bezos's AI startup Prometheus secured $12 billion in funding at a $41 billion valuation.

---

## NOTABLE TOOLS AND RESOURCES

- **Ponytail**: AI dev tool that prioritizes minimal, native code over over-engineered solutions to reduce code bloat
- **SQL to ER Diagram**: Free, open-source, browser-only tool for converting SQL schemas to interactive ER diagrams
- **Kage**: Open-source tool for creating high-fidelity, script-free website mirrors for offline browsing
- **Apache DataFusion 54.0.0**: Major SQL upgrades including LATERAL joins, 20-50x performance improvements
- **Linux Foundation OpenSharing**: Databricks handed Delta Sharing to Linux Foundation, extending it to AI models and agent skills
- **Ansible Automation Platform 2.7**: Visual execution environment builder and unified content discovery
- **Infobip OpenAPI MCP Spring Boot Starter**: Turns existing REST APIs into production-grade MCP servers automatically

---

## NEED-TO-KNOW LIST FOR DIGITAL AGENCY / MARKETING LEADERSHIP

These are the items most directly relevant to your role at a digital agency:

### URGENT / ACTION REQUIRED

1. **Anthropic Fable 5 / Mythos 5 are offline** - If you or your team were using these models for any client work or internal tools, switch to alternative models immediately. Access to other Anthropic models (Claude Sonnet, Haiku, Opus) remains unaffected. This is a wake-up call to always have model fallback plans.
   - https://www.businessinsider.com/why-white-house-ordered-export-controls-anthropic-mythos-fable-2026-6

2. **Bot traffic now exceeds human traffic online (57%)** - This fundamentally changes how you measure and report on client web analytics. AI agents are now a primary audience layer. Your measurement strategy needs to include citation rates, AI share of voice, and referral traffic from AI platforms.
   - (Covered in TLDR Marketing, sourced from Cloudflare data)

3. **Microsoft's record Patch Tuesday (~200 vulnerabilities)** - Ensure all client sites and managed infrastructure are patched. Multiple zero-days included.
   - https://www.techradar.com/pro/security/microsoft-breaks-patch-tuesday-record-with-fixes-for-over-200-security-flaws

### STRATEGIC / KEEP ON RADAR

4. **Salesforce acquiring Fin for $3.6B** - If you use Salesforce for any client CRM, expect AI customer service capabilities to be integrated into the platform. Plan for how this changes your service offerings around customer experience.
   - https://www.bloomberg.com/news/articles/2026-06-15/salesforce-to-buy-ai-customer-service-firm-fin-for-3-6-billion

5. **OpenAI Partner Network ($150M, 300K certified consultants by EOY 2026)** - Potential certification/partnership opportunity for the agency. Enterprise clients will increasingly expect their agencies to have formal AI credentials.
   - https://openai.com/index/introducing-openai-partner-network/

6. **Marketing teams going AI-first** - The trend toward leaner, generalist teams using AI for execution is accelerating. Agencies that position as "AI-first creative studios" will win over those still operating as "production pipelines." This is your competitive positioning story.
   - (Covered in TLDR Marketing)

7. **Apple's third-party AI system for Siri (iOS 27)** - A new App Store section and settings panel for third-party AI extensions is coming. This opens a new channel for client apps and services to be discovered through Siri.
   - (Covered in TLDR AI)

8. **OpenRouter Fusion** - Multi-model API that mixes AI models for smarter, cheaper results. Worth evaluating for any AI-powered tools you're building for clients.
   - https://openrouter.ai

9. **Google Skills Marketplace for Gemini Business** - Pre-built skills for dashboards and reporting could streamline client deliverables if you're in the Google Workspace ecosystem.
   - (Covered in TLDR AI)

10. **Uber's AI budget blowout as a cautionary tale** - As you scale AI tool usage across your team, track cost per task, not just per token. Uber's 5,000 engineers exhausted their annual AI budget by April.
    - https://cockroachlabs.com/blog/agentic-ai-costs-at-scale

---

*Compiled from 8 TLDR newsletters and 1 Your Everyday AI newsletter, all dated June 15, 2026.*
