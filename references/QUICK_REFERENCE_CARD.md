# Decomposer — Quick Reference Card

One page. The full spec is `../PROTOCOL.md`; this is the reminder, not the definition.

## The five steps

| # | Step | Output |
|---|---|---|
| 1 | Honesty Fuse | What I can engage with · where I am blind · how this most likely dies |
| 2 | Uncertainty Mapping | Every element → GREEN / YELLOW / RED |
| 3 | Hierarchical Decomposition | Epistemic dependency tree (not a module tree) |
| 4 | Node Attributes | Alive if / Dead if · confidence · detection latency · lethality |
| 5 | Anti-Shell Self-Check | 5 checks + 2 sub-checks. Fail → back to the named step |

## Zones

| Zone | Means | What to do |
|---|---|---|
| GREEN | The next concrete action is unambiguous right now | Do it. Keep it minimal. |
| YELLOW | The question is clear, the answer is not | This is where the work is. Write a probe. |
| RED | You cannot formulate the question at all | Do not work it directly. Contact with reality makes it visible. |

**The 70% rule:** if GREEN exceeds 70% of elements, the map is dishonest. Return to step 1.

**Zone sanity:** say each RED node out loud. If a well-formed question comes out, it is YELLOW. Red is not a badge of rigour.

## Survival condition

```
Alive if: [observable, measurable state]
Dead if:  [observable, measurable state]
```

Both falsifiable. No condition → delete the node. "Alive if the team works hard" is not a condition.

## Node attributes — all four, no substitutions

| Attribute | Question it answers | Scale |
|---|---|---|
| Confidence | How likely does this hold? | High / Medium / Low / Zero |
| Detection latency | If wrong, how long until I know? | hours / days / weeks / months / quarters |
| Survival condition | What makes it alive or dead? | a pair of observable statements |
| Lethality | What dies with it? | names of specific downstream nodes |

Confidence and detection latency are **not** the same field. High confidence + months of latency is a good bet with a long downside. Zero confidence + hours of latency is a cheap experiment.

## Anti-Shell Self-Check

| Check | Question | Pass |
|---|---|---|
| 1 | Does every node have its own observable survival condition? (Inheriting from a parent does not count.) | / |
| 1b | Does every node carry confidence **and** detection latency, neither standing in for the other? | / |
| 2 | Any jargon that cannot be translated to an action or a measurement? | / |
| 3 | Is YELLOW + RED at least 30% — and does the stated count match the listed elements? | / |
| 3b | For every RED node, can you state the question? If yes → relabel YELLOW. | / |
| 4 | Is there at least one plain, unhedged "I don't know"? | / |
| 5 | Is the first concrete action one sentence, specific, and the LAST line of the output? | / |

Failure → return to the step named in `../references/ANTI_SHELL_CHECKLIST.md`, correct, re-run all checks.

## Output shape

```
CONFESSION OF LIMITS
  What I don't know / Assumptions / What would invalidate this

UNCERTAINTY MAP        <element> — [GREEN|YELLOW|RED]
DEPENDENCY TREE        <root> ← <dependent> …

NODES
  <node> — Alive if: … / Dead if: …
           confidence: …  detection latency: …  lethality: …

FIRST ACTION           one sentence, specific, startable today
```

## Node schema — uniform, Red included

```
confidence:        High | Medium | Low | Zero
detection latency: hours | days | weeks | months | quarters | unknown
lethality:         <named nodes> | unknown
```

`unknown` is the only sanctioned "I can't fill this in". Prose in a value slot
(`"you have this number, I don't"`, `无法定价`) breaks the field. `Zero` and `Low`
differ: Low has a story, Zero has nothing.

## Hard gates — reject if

- modules or features appear before step 1 is done;
- any node lacks its own survival condition;
- confidence is present without detection latency, or vice versa;
- a formulable question is labelled RED;
- jargon survives Check 2;
- the output ends without a one-sentence first action;
- anything at all follows the first action — including a sentence certifying the
  output's own honesty ("Honest.", "not bravado", "no jargon found in scan");
- the stated element count disagrees with the elements listed;
- prose sits in a confidence or latency value slot;
- the output switches language partway through.

## Skip it when

The task is small and already understood. You asked for a module list and meant it. You need speed, not analysis. The protocol is for stress-testing plans before commitment, not for running them.
