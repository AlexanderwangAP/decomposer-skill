# Changelog

All changes to the `decomposer` skill since fork from [zbbsdsb/Fundemetal](https://github.com/zbbsdsb/Fundemetal).

The protocol's intellectual content is CeaserZhao's. The entries below are engineering and corrections, not invention.

## Unreleased (fork v1.0.0)

### Fixed — the skill could not be loaded at all

The root `SKILL.md` had no YAML frontmatter. Agent hosts discover skills by parsing that block; without it the file is skipped silently. The only frontmarked file in upstream was `adapters/trae/SKILL.md`, buried three levels deep and pointing at sibling paths with `../../` — which only resolve inside the original repository layout.

- Rewrote `SKILL.md` as a proper entry point with `name` and `description` frontmatter. The description carries the trigger phrases upstream had scattered across prose ("decompose this project", "help me figure out what I don't know", "don't give me an empty plan").
- Compressed the entry point to the executable core: five steps, output contract, hard gates, scale guide. It is now a self-contained procedure at roughly 5.5KB, down from a 7KB summary that pointed at a 45KB document for everything that mattered.
- Made `PROTOCOL.md` a load-on-demand reference. It runs to ~48KB (it grew slightly, because of the fixes below); loading it on every invocation was the reason the skill was expensive even when it worked. The table in `SKILL.md` says which file to read when.

### Fixed — confidence was measuring the wrong variable

Upstream, step 4 defined *Confidence* as "if this node is wrong, how quickly would I find out?" and scaled it High → Zero by time-to-failure. That is detection latency, not confidence.

The two are independent. A claim can be well-evidenced and take a year to falsify. A guess can resolve in seconds. Merging them makes slow-verification work look reckless and fast-verification guesses look safe — and it silently drops the thing the error budget is actually pricing, which is the cost of being wrong slowly.

- Split into **Confidence** (how likely the assumption holds, judged on evidence) and **Detection latency** (how long a wrong assumption stays invisible).
- Updated the hard constraint, the output contract, `SKILL.md`, and the worked example's attribute table.
- Added sub-check **1b** to the anti-shell checklist: both fields required, and one must not stand in for the other, with a bad/good example of the conflation.

### Fixed — Red was being awarded for the wrong reason

By upstream's own definitions, Red means *you cannot formulate the question*; Yellow means the question is clear and the answer is not. The flagship worked example marked three nodes Red:

| Node | Upstream label | Why that was wrong | Now |
|---|---|---|---|
| Niche audience exists and wants this | Red | Rationale given was "no data yet". Having no data is the definition of Yellow. | Yellow |
| Monetization model | Red | "Cannot design this until we know who the users are." Blocked, not blind. | Yellow |
| Content moderation at scale | Red | "Not relevant until we have users." Also a dependency, not a blind spot. | Yellow |

The example then cited its Red count as evidence of honesty — "Red: 3 (37.5%)... uncertainty is honestly represented." The check it invoked (Yellow + Red ≥ 30%) passes either way, so the check never caught this.

- Re-labelled the example, added two genuine Red nodes of the kind the example should have found ("how does this niche self-organize online", "whether amateur production is viable"), and re-ran the distribution: Green 20% / Yellow 60% / Red 20%.
- Added sub-check **3b, Zone Sanity**: for every Red node, say the question out loud. If a well-formed question comes out, it is Yellow.
- Corrected the prose in step 5 that invited the error. Upstream read "Red feels like admitting incompetence. It is not. Red is the whole point." That celebrates Red and pays the executor for marking more of it. Replaced with the point that Yellow is where the work is and Red is the zone you cannot act on yet.

### Changed — generalised one over-specific branch

Upstream's role detection had four positions: technical architect, non-technical founder, decision-maker, and **"MIT Scholar"**. The last got a four-layer falsifiability stack, a "Data Graveyard Protocol", and a full error-budget specification, roughly three times the treatment the others got — written for a specific research-grade thinker rather than a class of projects.

- Renamed to **Researcher** / "research or hard-science project" in `PROTOCOL.md`, `references/COGNITIVE_POSITIONS.md`, and the two template files (`references/FALSIFIABILITY_WHITEPAPER_TEMPLATE.md`, `references/ERROR_BUDGET_SPEC_TEMPLATE.md`). `FIELD_GUIDE.md` never mentioned the name and was not touched.
- Kept the content, which is genuinely good (master claim and destruction condition, derive-before-you-build, time-constant separation, error budgets instead of requirements, pre-committing to publishable failure). Compressed it by roughly a third and removed the second-person address to a named archetype.

### Changed — manifesto passed its own jargon check

`MANIFEST.md` calls itself honest while using `cognitive operating system`, "ruthlessly and repeatedly", and a closing flourish ("That is all it promises. That is everything."). All of these fail Check 2 or overpromise against the file's own epistemic-status section.

- Rewrote the affected passages in plain terms.
- Replaced "The Promise" with "What It Actually Buys You", stated modestly, on the grounds that a protocol overpromising about itself is failing its own Honesty Fuse.
- Added a closing section noting that the manifesto is written in the register the protocol criticises and will not survive its own Check 2. Read the manifesto to decide whether to care; read `PROTOCOL.md` to decide what to do.

### Added — the missing test suite

Upstream shipped an eval template and a measurement framework. 18 of its 24 skills have an `evals/` directory; this one did not — and it is the largest and most intricate of the lot. (The other five without evals are `great-expectations`, `insight-crystallizer`, `shoulders-of-giants`, `tension-mining`, and `vision-retrospective`.)

- `evals/tests.yaml`: 16 tests. 4 happy-path, 4 false-positive, 8 gate-gaming — the last two being poisoned-draft tests added after the first run exposed the gap.
- `evals/MANIFEST.yaml`: suite metadata, per-axis targets, and the note that gate-gaming is weighted highest because the anti-cheat claim is the binding one.
- `DEC-GG-02` and `DEC-GG-03` encode the two content fixes above as regression tests. If they start failing, the bugs have returned.
- `evals/MANIFEST.yaml` records `runs_completed: 1` against a target of three. One draw is not a distribution, and nothing here claims otherwise.

### Fixed — a quick reference card that taught a different protocol

`references/QUICK_REFERENCE_CARD.md` was inherited from upstream and had drifted: its five steps were "Map Elements / Classify by Zone / Test Dependencies / Define Survival Conditions / Sequence the Work", its zones were Known-Known / Known-Unknown / Unknown-Unknown, its self-check was five entirely different questions, and it defined lethality as a percentage rather than a list of downstream nodes. It never mentioned confidence or detection latency. Anyone using it as the advertised cheat sheet would run neither fix above.

- Rewritten to match the protocol as it now stands, including both sub-checks (1b, 3b) and the four node attributes.

### Fixed during review

An independent pass over this fork found the following, all corrected here:

- `PROTOCOL.md`'s closing paragraph of the worked example still said "the three Red nodes (monetization, content moderation, recommendation algorithm)" — upstream text left in place directly beneath the passage that relabels them Yellow.
- The worked example's Check 1 passed while conceding that most nodes "inherit their survival conditions from the root". Inheriting is not having, and the hard gate rejects it. Check 1 now fails on the first pass and shows the recovery.
- The tree carried 9 nodes against a map of 10, so every percentage downstream was computed on a different set than the tree described. "First 100 users from organic channels" is now in the tree.
- The two replacement Red nodes were arguably well-formed questions, which their own Check 3b would demote. The text now says so, sets the borderline rule ("treat as Yellow"), and names what genuinely survives as Red.
- `references/TUTORIAL.md` still taught the old confidence definition ("how fast would failure surface?") with a three-attribute table. It was byte-identical to upstream and merely relocated — so the tutorial was quietly re-teaching the bug this fork fixed. Now four attributes, with the conflation called out.
- `MANIFEST.md` said a confidence "cannot be backed by a concrete failure-detection mechanism" would be "downgraded to zero" — the same conflation again, plus a downgrade target contradicting the "Low" used everywhere else.
- `references/SCALE_GUIDE.md`'s step-4 row omitted detection latency, contradicting the hard gate.
- Grammar: "an researcher" and stray "scholar" survived the rename.
- `evals/MANIFEST.yaml` said a regression would show up as the test "passing again" when a failure is the actual signal. Reversed.
- Gate-gaming criteria in `evals/tests.yaml` were prohibitive only ("hollow if X"), so an empty output could pass by violating nothing. Each now states a positive floor first. The header's reference to a measurement framework that does not ship in this repository was removed.

### Evaluated — first full run, 2026-11-19

The suite ran for the first time. Record in `evals/RUN-2026-11-19.md`, scored by two independent judges who saw only the criteria and the outputs.

**Held:** both fork fixes. Three runs spontaneously applied the Red-demotion rule and named it; no run justified confidence by detection speed. Triggering was correct on all 14 cases, under a priming caveat — the agents were told a skill was installed, so that is a floor and not a trigger rate.

**Found and now fixed in the suite:**
- No test could prove the gates *reject* anything. Free generation does not reliably emit the bad node the gates exist to delete, so the criteria were unfalsifiable. Two poisoned-draft tests now inject defects directly. Both ran, both deleted every injected defect.
- "Every node carries X" is unfalsifiable unless the run log preserves every node. It did not, and two judges could not verify those criteria. Quantifiers are now countable, and the record says UNVERIFIABLE rather than passed where the evidence is missing.
- The "Red count as evidence of honesty" ban lived in one test and leaked: the same violation was penalised in DEC-GG-02 and walked past in five others. Six shared constraints (S1–S6) now apply to every triggering test and score as their own axis.
- DEC-HP-03's fixture supplies no plan while its criteria require inspecting one, and it demanded "an assumption with no survival condition" while the hard gate demands every node have one — self-locking under either reading. DEC-HP-04's criteria demanded a master claim its prompt never permits. Both now score what is reachable and name the fixture gap.
- DEC-GG-03's "different band from its confidence" had no defined mapping. A band table now does.

**Found in the skill, not fixed here — the main open defect:** five of six generative outputs certified their own honesty inside the output ("Honest.", "not bravado", "no jargon found in scan", "I'd rather have one honest Red than three dramatic ones"). The gates stop hollow output; they did not stop an output announcing it had passed. Shared constraint S1 bans it, and the recommended fix is to end the output contract at the first action with nothing after it. Notably it appeared only in generative runs, never in review runs — an output-contract problem, not a model-honesty one.

Also found in generated output, recorded in the run log rather than patched here: a miscounted zone distribution (18 stated against 16 actual), a run claiming "I can't phrase this as a question" while phrasing it, three different conventions for Red-node attributes across runs, and prose written into confidence/latency value slots.

### Added

- `NOTICE.md` — attribution for the derivative work. It lives here rather than in `LICENSE` because the first attempt wedged a derivative notice between the copyright line and the grant text, which made GitHub's licence detector give up and report `NOASSERTION` instead of MIT. `LICENSE` is now the standard text verbatim, so the licence is unambiguous to tooling, and the credit is one click away in `NOTICE.md`.
- `evals/RUN-2026-11-19.md` — the first full run: outputs, independent scores, and every defect found.
- `tools/verify.py` — a script that checks this file's claims rather than asserting them: frontmatter validity, referenced-file resolution, eval structure, absence of resurrected wording, uniform detection-latency scale, intact upstream attribution, and that everything listed under "Removed" is genuinely gone. Exits non-zero on failure. It does not test whether the protocol works; that is what `evals/` is for.

### Removed

| Path | Why |
|---|---|
| `adapters/trae/SKILL.md` | Duplicated the entry point at a depth no host scans. Its trigger phrases are now in root `SKILL.md`. |
| `adapters/twitter/` | `CAMPAIGN.md`, `PROMO_TWEETS.md`, `launch-thread.md` — launch marketing for the original repository. Not part of the skill. |
| `adapters/team/`, `adapters/human/` | Two-page notes rendering the same protocol for a meeting and for a whiteboard. `references/OUTPUT_CONTEXTS.md` and `FIELD_GUIDE.md` already cover both. |
| `assets/` | 256KB of logos and social cards. A skill folder should be text. |
| `CONTRIBUTING.md` | Contribution rules for a repository that is not this one. |

`FIELD_GUIDE.md`, `TUTORIAL.md` (moved into `references/`), `VALIDATION.md`, and all `references/` worksheets are retained.

### Not changed

The five steps, the survival-condition definition, the cognitive-debt / engineering-debt distinction, the scale matrix, and the empirical validation roadmap. These were sound and remain as written.

The 70% rule in step 2 and its honest caveat that it is a heuristic rather than a calibrated threshold are untouched. One *copy* of that caveat — the one under Check 3 in step 5 — was replaced when sub-check 3b went in; the caveat itself survives in step 2 where the rule is defined.
