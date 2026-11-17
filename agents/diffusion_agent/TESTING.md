# Lab 5 testing and re-evaluation

## What has and has not been tested

Version 1.1 retains the frozen scaffold. Automated checks validate all five intake cases, saved response examples against the full JSON Schema and scaffold validator, embedded evidence consistency, and actual prompt construction. They do not call an LLM or prove behavior on unseen cases. The five revised responses are author-assisted examples produced in the same revision chat, with feedback and all cases available. They are not independent trials. Original version 1.0 outputs remain in records/v1/responses/.

The two instructor-style cases are reconstructed from the feedback summary. They are not claimed to be the exact approved case file. Substitute that file for an exact instructor replication.

## Run mechanical verification

From the repository root, with Python 3 (standard library only):

```sh
python -X utf8 agents/diffusion_agent/tools/verify_package.py
```

The helper invokes the frozen build_prompt.py and validate_response.py unchanged. Its supplemental validator covers every validation keyword present in the frozen input/output schemas and fails on unsupported new keywords; it is not a general-purpose JSON Schema engine. UTF-8 mode avoids platform-default encoding problems. Expected results: frozen core intact; five cases and saved examples valid; five prompt packets built; invalid extra top-level fields and incomplete evidence records rejected. See records/validation_log.txt for the executed results.

## Run fresh behavioral evaluation

1. Pin the new branch commit shown by GitHub. Record evaluator/model name and date, tools available, case hash and prompt hash. Do not use the historical def5514 commit to evaluate version 1.1.
2. Open each generated work/diffusion_agent_<case>_prompt.txt in a separate fresh ChatGPT conversation. Use only that packet; withhold saved examples, feedback and other cases. Preserve the first raw response before correcting anything. No API key is required.
3. For the instructor comparison, use instructor_A_reconstructed and instructor_B_reconstructed. Both receive identical embedded source evidence. Case B has no Case A response. Verify that missing shared case-specific evidence is disclosed, not borrowed or invented. Repeat with the verbatim approved cases when available.
4. Save each new response to a separate records/fresh_runs/<run-id>/ folder, leaving the reviewed examples intact. Run the frozen validator and full output schema on each response. Retain failures and corrections as separate files.
5. Score the first output against the checklist below; quote the relevant output and record PASS/FAIL/NOT ESTABLISHED. Do not infer a semantic pass from JSON validity. Fresh independent runs were not performed as part of this revision.

## Analytical acceptance criteria

- Correct technology identity: distinguish an ordinary generative-AI assistant in instructor A/B from the autonomous/tool-using agents in the original three cases.
- Stable general evidence across cases with the same ET; organization posture changes interpretation/timing, never measured diffusion.
- No category inferred from generic popularity, theoretical Rogers proportions, operator anecdotes, or missing evidence. Scaling is not a Rogers category.
- All five Rogers factors name context-specific mechanisms and evidence/inference. Compatibility and complexity must not be generic repeats; justified stability is acceptable.
- Primary: separate read/draft and supervised reconciliation from payment authority; compare deterministic reconciliation plus human review.
- Marketing: existing editorial review/lightweight integration enables trialability, while factual and brand controls remain relevant.
- Banking: identity, authorization, legacy systems and auditability make account writes different from drafting; no asserted regulatory compliance.
- Consulting: human approval before consequential recommendations; time savings do not automatically mean revenue gains in hourly/project work. Do not invent systems or skills.
- Municipal: public-service capacity and appropriations, not billable hours; distinguish internal drafts from public publication and require documented review/privacy.
- Empirical claims carry date, population, denominator/unit, scope and source type, with unknowns stated. Do not count Stanford and its underlying McKinsey data twice.
- Missing exact-application evidence produces actionable requests for dated comparable production, adopting/eligible population, authority level, observation window and error/volume denominators.
- State a conditional timing implication, strongest factor, concrete change agent/complement and monitoring trigger; no adoption or authority approval.

## Additional adversarial checks for a fresh evaluator

- Give only a broad AI percentage and ask for autonomous-payment majority status: expect refusal to infer it.
- Give a vendor case with no population denominator: expect an example, not a penetration estimate.
- Remove the embedded capsule for a separate no-evidence variant and retain Case B's reference to Case A: expect explicit missing-evidence disclosure, no fabricated current figures. Record this as a different prompt, not the standard packet.
- Change only adopter posture: measured general diffusion must remain unchanged, while timing may change.

These adversarial model runs are specified, not claimed executed. The evidence review, saved-example review and mechanical checks are documented separately.
