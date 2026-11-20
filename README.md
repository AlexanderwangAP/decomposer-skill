# Decomposer

An agent skill that turns "I don't know what I don't know" into questions you can actually answer.

It produces an **uncertainty map**, not a plan. Every node gets a survival condition you can test, a confidence level, and a time-to-detection. Then it tells you the one thing to do first.

```
"I want to build a niche TikTok. I can't code and my budget is small."
   │
   ├─ Honesty Fuse      → what I can't tell you, and how this probably dies
   ├─ Uncertainty Map   → 2 green, 6 yellow, 2 red
   ├─ Dependency Tree   → one root unknown; everything else waits
   ├─ Node Attributes   → Alive if / Dead if, confidence, detection latency
   └─ First Action      → "Ask 20 people in the niche to submit one video by hand."
```

---

## Where this came from

**This is a fork and a repair job. It is not original work.**

The protocol was written by **CeaserZhao** as `decomposer`, one of 24 skills in [zbbsdsb/Fundemetal](https://github.com/zbbsdsb/Fundemetal) (MIT, 2026). The intellectual content — the five steps, the survival condition, the anti-shell check, the worked example — is his. If you use this and it helps you, the credit is his.

What this repository adds is engineering and corrections. The upstream skill could not be loaded by an agent host at all: its root `SKILL.md` had no YAML frontmatter, so discovery skipped it entirely. Two more things were wrong in the content and are fixed here. Details in [CHANGELOG.md](CHANGELOG.md).

The upstream repository is licensed CC0 overall with each skill carrying its own MIT license. This fork stays MIT, and the original copyright notice is retained in [LICENSE](LICENSE) as the license requires.

## Install

Copy the `decomposer/` folder into your agent's skills directory. For Claude, that is `~/.claude/skills/decomposer/`. No build step.

The skill loads by progressive disclosure: `SKILL.md` is small and holds the executable core. `PROTOCOL.md` (the full 45KB specification) is read only when needed. You do not pay for the long document on every run.

## Use it

Ask for it, or say things like:

- "help me figure out what I don't know about X"
- "decompose this project"
- "this is too big, where do I start"
- "don't give me an empty plan"
- "sanity-check this plan before we commit budget"

It also works on a plan that already exists — treat it as a red-team pass.

It declines politely when the task is small and well-specified, when you asked for a module list, or when you want speed over analysis. A skill that fires on everything is useless.

## The five steps

| | Step | Produces |
|---|---|---|
| 1 | Honesty Fuse | What I can't address, where I'm blind, how this most likely dies |
| 2 | Uncertainty Mapping | Every element as Green / Yellow / Red |
| 3 | Hierarchical Decomposition | An epistemic dependency tree — not a module tree |
| 4 | Node Attributes | Alive if / Dead if, confidence, detection latency, lethality |
| 5 | Anti-Shell Self-Check | 5 checks + 2 sub-checks; fail any and go back |

**The distinction that matters:** a functional decomposition asks *what are the parts*. This asks *what do I need to know first*. A five-module roadmap for a social platform looks like progress and means nothing if you don't know whether anyone wants the thing.

## The two fixes

**Confidence was measuring the wrong thing.** Upstream defined confidence as "if this is wrong, how fast would I find out?" That is detection latency. A well-evidenced claim can take a year to falsify; a coin flip resolves in seconds. Merging them makes slow work look reckless and quick guesses look safe. They are now separate fields.

**Red was being awarded for the wrong reason.** Red means *you cannot formulate the question*. Upstream's flagship example marked three nodes Red for having no data or being blocked — both of which are Yellow, because the question is perfectly clear. It then cited the resulting Red count as evidence of honesty. The example is re-laboured, and there is now a zone-sanity sub-check that catches this.

Neither fix changes the protocol's shape. Both change what it outputs.

## Status

The protocol is a heuristic, not a validated method. Upstream said so in its own manifesto, and it is still true here.

The `evals/` directory holds **16 tests** across happy-path, false-positive, and gate-gaming categories. Two of them are poisoned-draft tests that inject a deliberately bad node and watch the gates delete it. The gate-gaming cases are the binding ones — an anti-cheat claim is only worth as much as its hardest test.

**They have been run three times each** (2026-11-19 and 19-20) — 48 runs, meeting the suite's own 3-per-test target. Full record in [`evals/RUN-2026-11-19.md`](evals/RUN-2026-11-19.md), scored by two independent judges.

What the runs showed: triggering was correct on 48 of 48, though the agents knew a skill was installed, so that is a floor rather than a real trigger rate. Both fork fixes held across all three rounds, in generation *and* in rejection. The gates deleted every injected defect in the poisoned-draft tests, on every round.

What it also showed, and is worth knowing before you rely on this: **five of six generative outputs certified their own honesty inside the output** — "Honest.", "not bravado", "no jargon found in scan". The gates stop hollow output; they did not stop an output announcing it had passed. That is now banned by shared constraint S1, but it is the clearest thing this skill gets wrong.

What these runs cannot show: the trigger rate against unprimed users, and behaviour on prompts outside these sixteen. Both need a rig this harness does not have.

The useful framing, inherited from upstream and correct: this is a red-teaming tool for plans. Its value is in catching bad plans, not producing good ones.

## Layout

```
decomposer/
├── .gitignore                    repo plumbing
├── SKILL.md                      entry point, YAML frontmatter, executable core
├── PROTOCOL.md                   full specification and worked example
├── LICENSE                       standard MIT, reproduced verbatim from upstream
├── NOTICE.md                     attribution: this is a derivative work
├── MANIFEST.md                   why it exists (a sales pitch; the protocol is in PROTOCOL.md)
├── MANIFEST.yaml                 machine-readable metadata
├── CHANGELOG.md                  what this fork changed and why
├── VALIDATION.md                 upstream's research plan for testing the claims
├── FIELD_GUIDE.md                how the protocol renders in specific contexts
├── tools/
│   └── verify.py                 checks that the claims below actually hold
├── evals/
│   ├── MANIFEST.yaml             suite metadata
│   ├── tests.yaml                16 tests, incl. 2 poisoned-draft
│   └── RUN-2026-11-19.md         the first full run: outputs, scores, defects
└── references/
    ├── ANTI_SHELL_CHECKLIST.md   the checks, with recovery steps
    ├── PROBE_TOOLKIT.md          how to find unknown unknowns
    ├── COGNITIVE_POSITIONS.md    adapting output to the reader's role
    ├── SCALE_GUIDE.md            how deep to go
    ├── COMMON_PITFALLS.md        where runs go wrong
    ├── OUTPUT_CONTEXTS.md        rendering the map outside a conversation
    ├── QUICK_REFERENCE_CARD.md   one-page cheat sheet
    ├── TUTORIAL.md               walking a beginner through it
    ├── DECISION_CARDS_WORKSHEET.md        worksheet for the decision-maker branch
    ├── FALSIFIABILITY_WHITEPAPER_TEMPLATE.md   worksheet for the research branch
    ├── ERROR_BUDGET_SPEC_TEMPLATE.md            worksheet for the research branch
    ├── ZERO_CODE_VALIDATION_TEMPLATE.md         worksheet for the founder branch
    └── SEVEN_DAY_TEST_CHAIN_TEMPLATE.md         worksheet for the founder branch
```

Removed from upstream: `adapters/` (a TRAE wrapper that duplicated the entry point, plus Twitter launch material), `assets/` (branding images), and `CONTRIBUTING.md`. See CHANGELOG.md.

## Verifying the claims

This fork makes a number of specific claims — a bug was fixed, a file was removed, attribution is intact. Those are checkable rather than asserted:

```bash
python3 tools/verify.py
```

It exits non-zero if any claim fails: frontmatter parses, every referenced file resolves, the evals are well-formed with positive floors on the gate-gaming cases, none of the corrected wording has crept back in, the detection-latency scale is uniform across files, the upstream copyright and MIT grant survive, and everything CHANGELOG lists as removed is actually gone. Wire it into CI if you like.

It does not test whether the protocol works. That is what `evals/` is for.

## License

MIT. See [LICENSE](LICENSE) — the standard text, reproduced verbatim from upstream with CeaserZhao's original copyright notice intact, as the licence requires.

Attribution for the derivative work lives in [NOTICE.md](NOTICE.md), kept separate from the licence so that GitHub and other tooling can still recognise the licence unambiguously.

If you publish something built on this, link upstream. That is all the original asked for.
