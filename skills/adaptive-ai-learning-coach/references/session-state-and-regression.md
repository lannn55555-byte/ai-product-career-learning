# Session state and regression checks

## Durable learning state

Maintain the following in the learner's workspace log when it is writable.
Otherwise return it as a clearly named Markdown block for the learner to copy.

```text
Selected duration, current phase, and learning mode
Foundation profile: product [emerging / working / unassessed];
  AI [emerging / working / unassessed]; evidence and last calibration date
AI mainline: Day N / duration; named units, current unit, and status
Product foundation: PF-DN / selected sequence; named units, current unit, and status
Bridge: product decision and AI-specific delta connecting the active units
Anchor scenario: familiar context and latest system-map choices
Required content delivered: terms, mechanism, boundary, and application
Anchor evidence: prompt, learner decision, feedback, and result
Independent transfer check: different domain/task context, decision rule,
  learner response, feedback, and pass / needs_review / not_started
Mastery: node, level 0–5, demonstrated evidence, uncertainty, and review point
Branch: active / closed / parked, with question and return module
Learner preferences: explicit durable preferences only
System-map change and one concrete next action
```

Use stable anchors such as `AI-D4-C1`, `PF-D4-C1`, `AI-D4-A1`, and
`AI-D4-T1`; reserve `T` for an independent transfer check. Do not call an
anchor variation an independent transfer check.

## Completion states

Use one state for every active unit:

- `in_progress`: explanation or anchor practice has started.
- `concept_complete_transfer_pending`: the learner demonstrated the rule in
  the anchor context, but has not passed an independent transfer check.
- `needs_review`: a transfer check revealed a material gap; record the
  focused repair and retry point.
- `completed`: the named outcome and independent transfer check passed.

Only a completed unit advances its own track. In Dual foundation mode, the
calendar-day checkpoint is complete only when both scheduled units are
completed. Do not record Level 3 or above without linked transfer evidence.

## Regression checks

Before replying, test the intended response against these cases:

1. The learner says, “Do not make me build something first.” Start with the
   concept; do not require project narration.
2. Foundation evidence is missing. Begin provisionally in Dual foundation mode;
   do not force a separate diagnostic interview.
3. A learner has an emerging foundation. Deliver the required terms, mechanism,
   boundary, and example before application; do not skip them after one
   plausible answer.
4. A status card shows only `PF-DN` while Dual foundation mode is active.
   Name the actual product unit, its outcome, and its progress.
5. A status card shows `1 / 2`, but only one independently named unit exists.
   Correct it to `1 / 1`. Explanation, application, feedback, and transfer
   validation do not create extra sections.
6. Two independently named units were announced. Do not skip one because the
   learner answered the other well; explicitly revise scope and denominator
   first if the plan changes.
7. A familiar-project question or one-condition variation is being treated as
   transfer. Record it as anchor practice, then use a different-domain or
   different-task-context scenario before Level 3 or above.
8. A learner is asked for a numerical evaluation threshold without baseline,
   eligible population, risk level, and business objective. Do not require an
   invented number; assess the missing inputs and calibration/pilot method.
9. The learner asks a relevant technical question. Treat it as a branch, record
   the return point, and do not advance either track automatically.
10. The learner asks whether today is complete. Report both-track unit status,
    evidence state, active branch, and one next action; do not estimate from
    message count.
11. The learner completes several lessons. Do not call the learning connected
    until they defend system choices in an unseen integration scenario.
