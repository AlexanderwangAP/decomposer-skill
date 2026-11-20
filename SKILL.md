---
name: decomposer
description: >
  Converts unknown unknowns into known unknowns before anything is built.
  Use when a request is a large, ambiguous, or aspirational goal and the user
  wants an honest breakdown rather than a polished plan — e.g. "help me figure
  out what I don't know", "decompose this project", "this is too big, where do
  I start", "don't give me an empty plan", "honest breakdown", "sanity-check
  this plan", "what could kill this", or a roadmap request where the problem is
  under-specified. Also use to red-team a plan that already exists. Skip when
  the task is already well understood and executable, when the user wants a fast
  answer rather than analysis, or when they ask for a functional module list
  explicitly.
---

# Decomposer

A five-step protocol for turning "I don't know what I don't know" into named,
testable questions. It produces an **actionable uncertainty map**, not a report.

Two metrics only: **honesty** and **actionability**. If output is dishonest it is
worthless; honest but unactionable is incomplete. Everything else is noise.

Full specification and worked examples: `PROTOCOL.md` (read before a first run).
Checklist for the final gate: `references/ANTI_SHELL_CHECKLIST.md`.

## The five steps

**1 — Honesty Fuse.** Before any analysis, output three things, in this order:
what I can actually engage with, where I am blind (specific missing facts, not
moods), and the single most likely way this dies. No module lists, no feature
breakdowns, no "this is ambitious but achievable."

**2 — Uncertainty Mapping.** Classify every *element* into a zone. An element is
the smallest unit of uncertainty that can carry a survival condition — it is a
claim that needs testing, not a module.
- **Green** = the next concrete action is unambiguous right now.
- **Yellow** = the question is clear, the answer is not.
- **Red** = you cannot formulate the question at all. Not "hard". Blind.

If Green exceeds 70% of elements, the map is dishonest — return to step 1.

**3 — Hierarchical Decomposition.** Build an *epistemic* dependency tree:
which unknowns must be resolved before others can be addressed. This is not
functional decomposition ("what are the parts"). Prune to root unknowns and
independent leaves. Three node states: Executable / Pending Validation / Blind Zone.

**4 — Node Attributes.** Attach to each node:
- **Survival condition** — `Alive if: [observable] / Dead if: [observable]`.
  Not a risk, not work to do. A binary test anyone can apply. No condition →
  delete the node.
- **Confidence** — High / Medium / Low / Zero: how much you would bet the
  assumption holds, given current evidence.
- **Detection latency** — hours / days / weeks / months / quarters: how long a wrong
  assumption would surface. Separate field; slow detection does not lower
  confidence, it raises the cost of being wrong.
- **Lethality** — which specific downstream nodes die if this one dies.

Hard constraint: a node marked High confidence with no written survival
condition is downgraded to Low. Your confidence is in sounding authoritative,
not in the node.

**5 — Anti-Shell Self-Check.** Five checks, two of them with a sub-check. Fail → return to the named step.

1. Every node has its own observable survival condition. Inheriting from a parent node does not count — a node that borrows its condition has not been understood.
   **1b.** Every node records both confidence and detection latency, and neither stands in for the other. "High confidence because failure would show up fast" is a latency claim wearing confidence's name.
2. No untranslatable jargon ("best practices", "robust", "scalable", "synergy").
3. Yellow + Red ≥ 30% of nodes. **And the count must reconcile**: stated element
   total equals the number of elements actually listed, and the zone percentages
   are computed against that same total. Recount out loud before writing the
   percentages — a map that says "18 elements" and lists 16 has failed.
   **3b.** For each Red node, say the question out loud. If a well-formed question comes out, it is Yellow and must be relabelled. Red is not a badge of rigour. "What the first N conversations reveal that I have not thought to ask" is Red — the residual, not the topic. "Which definition conflicts exist in this org, and how deep they run" is Yellow — plain question, unknown answer. If you can conjugate it into a question someone could answer, it is Yellow.
4. At least one explicit, unhidden "I don't know".
5. The first concrete step is one sentence — a specific action, not "research".
   It is also the last line: nothing follows it.

## Output contract

```
CONFESSION OF LIMITS
  What I don't know: … / Assumptions I'm making: … / What would invalidate this: …

UNCERTAINTY MAP
  <element> — [GREEN|YELLOW|RED]

DEPENDENCY TREE
  <root> ← <dependent> …

NODES
  <node> — Alive if: … / Dead if: …
          confidence: …  detection latency: …  lethality: …

FIRST ACTION
  <one sentence, specific, can start today>
```

**The output ends at FIRST ACTION.** Nothing follows it — no summary, no
closing thought, and above all no sentence certifying that the output is honest
or compliant. "Honest.", "not bravado", "no jargon found in scan", "this is the
first thing produced", "I'd rather have one honest Red than three dramatic ones"
are all rejected. Compliance should leave traces, not declarations; a receipt of
compliance is not compliance. If you are tempted to add one, that is the signal
to stop.

**One language throughout.** Pick the user's language and stay in it. Do not
switch mid-output.

### The node schema is uniform

Every node — Green, Yellow, and Red alike — carries the same five fields. Red is
not exempt. The treatment of Red nodes has drifted in practice (some runs give
them no attributes at all, some give probe conditions, some refuse a field
outright); this is the rule: **a Red node gets the same schema, and where a field
is genuinely unknowable it is marked, not left blank and not filled with prose.**

```
confidence:           High | Medium | Low | Zero
detection latency:    hours | days | weeks | months | quarters | unknown
lethality:            <named nodes> | unknown
```

`unknown` is the only sanctioned value for "I cannot fill this in", and it is
available for detection latency and lethality **but not for confidence**. There
is no `unknown` confidence. If you have no basis for a confidence judgement, the
answer is `Zero` — that is exactly what Zero means, and using `unknown` there
just renames it and breaks the band.

Writing `confidence: "you have this number, I don't"` or
`detection latency: 无法定价` is prose in a value slot and breaks the field. Nor
may you append a justification to a value — `confidence: unknown — this is a
number on your books, not a guess I can make` is prose wearing a value's
clothes. Put the reason in a sentence outside the schema.

**Confidence has exactly four bands and they are not interchangeable.**
- `High` — direct evidence, or a strong prior from close analogues.
- `Medium` — indirect evidence; plausible, with a named way it fails.
- `Low` — a guess with a story attached; you would not be surprised either way.
- `Zero` — no basis at all. You are filling in a blank.

`Zero` and `Low` differ: Low has a story, Zero has nothing. If you find yourself
using both for nodes with the same evidence base, pick one and use it.

## Hard gates — reject output that

- lists modules or features before step 1 is complete;
- contains any node without a survival condition, Red included;
- states a confidence without a detection latency (or vice versa);
- classifies a node as Red when the question is actually formulable — that is
  Yellow, and calling it Red inflates the honesty signal;
- puts prose in a confidence or latency value slot instead of a value or `unknown`;
- cites the number of Red nodes as evidence about the map's honesty — whether
  as a boast ("only one honest Red, not three dramatic ones") or as a defence
  against an imagined accusation ("labelling more of this Red would be
  theatre"). Both argue from the count. The count is not an argument; the zone
  rules are, and they are already stated;
- contains jargon that cannot be translated to an action or measurement;
- switches language partway through;
- has anything at all after the first action;
- ends without a one-sentence first action.

## Scale

Simple task (1 person, 1 week) → step 5 only, 3–5 nodes. Moderate → all five,
10–20 nodes. Complex → all five plus full decomposition, 20–50 nodes.

Do not run this on a problem already understood and executable, during an
active execution sprint with no new information, or when the user wants speed.
It is a red-teaming tool for plans, not a production process.

## Reference files

| File | Read when |
|---|---|
| `PROTOCOL.md` | Before a first run. Full spec, worked example, probe toolkit, validation framework |
| `references/ANTI_SHELL_CHECKLIST.md` | Running step 5. Per-position adaptations and recovery |
| `references/PROBE_TOOLKIT.md` | Cannot find the unknown unknowns in step 2 |
| `references/COGNITIVE_POSITIONS.md` | Adapting output to the user's role |
| `references/SCALE_GUIDE.md` | Deciding how deep to go |
| `references/COMMON_PITFALLS.md` | Output feels hollow or the user resists |
| `references/OUTPUT_CONTEXTS.md` | Rendering the map for a non-conversation context |
| `references/QUICK_REFERENCE_CARD.md` | One-page cheat sheet. Matches the protocol above, including both sub-checks |
| `references/TUTORIAL.md` | Walking a beginner through it, with a second worked example |
| `FIELD_GUIDE.md` | Rendering the map in a non-conversation context (essay, meeting brief, whiteboard) |
| `VALIDATION.md` | The research plan for testing whether any of this works |
| `MANIFEST.md` | Why the protocol exists. Read for motivation; the procedure is in `PROTOCOL.md` |
| `references/*_TEMPLATE.md`, `references/DECISION_CARDS_WORKSHEET.md` | Fill-in-the-blank worksheets for the research, founder, and decision-maker branches |
