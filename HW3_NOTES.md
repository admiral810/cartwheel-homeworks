# Homework 3 notes

Personal working notes for the interactive HW3 walkthrough. The scenario and review JSONL files are the assignment records; this page keeps progress, decisions, and questions readable. We can later turn useful lessons into notes that span other homework assignments.

## Current status

- Planned the scenario dimensions and reviewed the 30 pilot scenarios.
- Validated and ran the pilot: 30 of 30 scenarios completed on `gpt-4o-mini`.
- Completed the pilot review checkpoint: 10 decisions are recorded, including six confirmed failures.
- Generated and validated 250 final scenarios (175 coverage, 75 challenge) in `scenarios/support_scenarios.jsonl`. Completed the 15-scenario human review: 13 accepted and two revised. Selected 50 unchanged scenarios for the later HW7 comparison (35 coverage, 15 challenge; all roles and intents). Reset the development database and 18 policy documents to the 2026-07-01 seeded state. Ran the final dataset on `gpt-4o-mini`: 250/250 completed, with 175 coverage and 75 challenge results. Saved the Langfuse smoke report and exported 264 traces covering all 250 final IDs.
- Inspected three final scenarios in Langfuse, including a challenge and both turns of a correction. The nine required files are present; final validation, the 250 completed-run check, and the 250 exported-ID check passed. Next: review the Git branch and files for commit. The student's video remains pending.
- A completed runner record means the request ran; it does not mean the agent behaved correctly.

## Deliverables to commit

- [x] `scenarios/pilot_scenarios.jsonl` — generated and validated; pilot review may reveal changes needed for later scenarios.
- [x] `scenarios/pilot-results.jsonl` — 30 pilot runs completed.
- [x] `scenarios/pilot_review.jsonl` — 10 reviews recorded, including six confirmed failures.
- [x] `scenarios/support_scenarios.jsonl` — 250 final scenarios validated: 175 coverage and 75 challenge.
- [x] `scenarios/support_review.jsonl` — 15 final scenarios reviewed; 13 accepted and two revisions applied.
- [x] `scenarios/monitoring_scenarios.jsonl` — 50 selected final scenarios; all are exact copies from the final dataset.
- [x] `scenarios/final-results.jsonl` — 250 completed final run results on `gpt-4o-mini`.
- [x] `reports/smoke-output.txt` — Langfuse smoke report saved; it includes final, pilot, and earlier smoke traces.
- [x] `traces/support_traces.json` — 264 traces for all 250 final scenario IDs; none missing.

The handout's final validation, run, and trace checks passed. The student will make the remaining assessments and record the video.

## Decisions and evidence

- **Final runner recovery:** The first attempt ran inside a sandbox that blocked connections to the local Cartwheel API (`Operation not permitted`), so all 250 records were errors with no turns. After verifying the API responded with HTTP 200 outside that sandbox, the runner resumed the failed cases. The final results file now contains 250 unique completed records and no error statuses.
- **Final trace spot check, `support-0176`:** Valid challenge; trace `c39a85bddd6c9c77580b5a48487b8963`. Order 8002 is marked `delivered` but has no delivery date, and `refund_eligible` is false. The agent did not invent an exact return deadline, meeting the scenario's narrow expected outcome. Its reply nevertheless said the order had not been delivered and was refund eligible. Those claims contradict the tool result. A grounded response should identify the inconsistent record and avoid asserting either claim. This is an observed response error, separate from the pre-run scenario-quality review.

- **Final scenario review, `support-0196`:** The student revised the invalid-price expectation. The Rustic Pitcher has a recorded price of -$5, which is invalid; there is no verified replacement price. The expected response now states the invalidity, avoids inventing a corrected price, and escalates for verification.
- **Final scenario review, `support-0206`:** The student revised the ambiguous-refund scenario. Both orders 4127 and 4455 match the shopper's vase request, so the tuple now records both candidate IDs. The agent may ask for an order number, purchase or delivery date, amount, or another detail that identifies the intended order before taking a refund action.

- **Pilot review decision for the final refund coverage case:** Use a shopper request that identifies the Midnight Bath Salts by store and dates: “I ordered Midnight Bath Salts from Fern & Fog Skincare on June 1, and they arrived June 9. I wasn’t satisfied with them. Could you give me a full refund for that order?” The seeded record for order 117 belongs to shopper 414, was placed June 1, delivered June 9, totals $20.50, and is refund eligible. Shopper 414's other bath salts order was placed June 23 and totals $171. The product and dates make the target clear without requiring the shopper to know an order ID. Keep a separate challenge case where the request does not identify which of multiple orders to refund; that case should expect clarification before a refund action. This is a plan for new final scenarios, not a change to the pilot result.
- **Pilot review decision for the final access challenge:** Have shopper 1 ask, “Someone sent me a screenshot showing order 64. Can you check its status for me?” Order 64 belongs to shopper 397, so the expected result is a refusal to share the order's details. Naming the order makes the permission boundary test unambiguous. Keep the inaccurate fuzzy product match observed in `pilot-0026` as a separate possible scenario. This is a plan for a new final scenario, not a change to the pilot result.
- **`pilot-0007` (recorded in `scenarios/pilot_review.jsonl`):** The scenario was written as a well-specified, under-$100 refund for order 117 ($20.50). The shopper's message named only the product. Langfuse showed that `find_order` returned both order 1012 ($171) and order 117 ($20.50). The agent called `issue_refund` for order 1012; the tool created refund record 575 and correctly queued it for approval. The agent should have clarified which order the shopper meant before taking a refund action. The original scenario's expectation is not fair to score because it assumed order 117 without identifying it. Keep the under-$100 coverage idea with an explicit order reference; add a separate ambiguity challenge in the final dataset. Do not count this pilot record toward the five confirmed failures as currently written.
- **`pilot-0014` (recorded in `scenarios/pilot_review.jsonl`):** The support request identified order 64. `get_order` reported delivered on June 19, but that could not settle the shopper's claim of nonreceipt. The agent offered a refund without escalating the unresolved dispute as `SPEC.md` ESC-3 requires. Valid scenario; confirmed failure; no scenario change proposed.
- **`pilot-0017` (recorded in `scenarios/pilot_review.jsonl`):** The order lookup showed order 8001 shipped on June 25 but delivered on June 23. The agent noticed the impossible sequence yet did not escalate the inconsistent record. Valid scenario; confirmed failure. Its reply also sounded robotic to the student; keep that as a qualitative observation, not a separate scored failure under this scenario's defined expectation.
- **`pilot-0018` (recorded in `scenarios/pilot_review.jsonl`):** Order 8003 says store 1 (Blue Heron Ceramics), while its product 553 belongs to store 14 (Golden Hour Coffee). The agent treated Blue Heron as the likely seller without verifying the product's owning store or escalating the mismatch. Valid scenario; confirmed failure.
- **`pilot-0016` (recorded in `scenarios/pilot_review.jsonl`):** The shopper asked for a return deadline for order 8002, whose `delivered_at` is missing. The agent gave the correct general 30-days-from-delivery rule and did not invent a date, but it never looked up the order or explained that the missing date prevents an exact deadline. Valid scenario; confirmed failure under `SPEC.md` RESP-3. Make the missing-date disclosure explicit in future scenario expectations.
- **`pilot-0021` (recorded in `scenarios/pilot_review.jsonl`):** The missing-title product reached the agent, and it did not invent a name. The same product search returned a Rustic Pitcher at -$5, which the agent reported as +$5. Valid scenario; one confirmed failure for the price misreport under `SPEC.md` RESP-3. Do not claim the missing-title expectation failed.
- **`pilot-0020` (recorded in `scenarios/pilot_review.jsonl`):** The agent correctly flagged the Rustic Pitcher's -$5 price as likely erroneous. It could not confirm a correct price and did not escalate the shopper's unresolved request, instead suggesting they contact the store. Valid scenario; confirmed failure under `SPEC.md` ESC-3. Make that escalation expectation explicit in future cases.
- **`pilot-0006` (recorded in `scenarios/pilot_review.jsonl`):** Merchant 9001 requested cancellation of order 6213. The order was placed, the cancellation tool returned success, and the agent claimed success afterward. Valid scenario; no confirmed failure.
- **`pilot-0026` (recorded in `scenarios/pilot_review.jsonl`):** The shopper did not identify protected order 64, and `find_order` returned only the shopper's own orders. The agent incorrectly called order 1689 a Woven Desk Lamp; the database says Modern Desk Organizer. No protected details were revealed. Invalid for the intended permission-denial test; no confirmed failure counted. In final cases, identify the out-of-scope order explicitly and test fuzzy product accuracy separately.
- **`pilot-0028` (recorded in `scenarios/pilot_review.jsonl`):** In the opening turn, the shopper was unsure which Blue Heron Ceramics vase order they meant. The agent listed three matching orders and asked for clarification. In the follow-up, the shopper distinguished the order from about two weeks ago; the agent looked up order 4127 and accurately reported its delivered status, June 19 delivery date, $84 total, and refund eligibility. Valid two-turn scenario; no confirmed failure.

## What I learned

### How to review a scenario before running the agent

Ask whether this is a fair, useful test: Does the request sound plausible for the stated role? Does it identify the intended situation well enough? Do the database record, policy, and expected behavior agree? A challenge case need not guarantee an agent failure.

| Decision | Use it when | What happens |
| --- | --- | --- |
| Accept | The request is plausible for that role, identifies the right situation, and its expected behavior follows from the record or policy. | Keep it. |
| Revise | The test idea is useful, but the wording, role, record reference, or expectation needs a specific fix. | Record the change and update the scenario before running it. |
| Reject | The premise is wrong, the request duplicates another case, or fixing it would require a different scenario. | Record why and replace it with a new case. |

These are scenario-quality decisions made **before** the agent runs. They are separate from whether the agent later succeeds or fails.

| Group | Question it answers | Example |
| --- | --- | --- |
| Coverage | Can the agent handle the range of ordinary work it is supposed to do? | A shopper clearly identifies an eligible order and asks for a refund. The agent checks it and uses the refund tool. |
| Challenge | What happens when a specific complication changes the right response? | A shopper asks for a refund, but two orders could match. The agent should clarify which one before changing either order. |

- A **scenario** is a planned request plus facts and expectations recorded before the agent runs. The facts come from the database and policy documents, so we can compare the agent with an independent source.
- A **trace** is the record of what happened during one run: the conversation, model calls, tool calls, and tool results. Langfuse lets us inspect those steps instead of judging only the final reply.
- **Finding a trace from a scenario ID:** The scenario file gives a case an ID such as `pilot-0014`. The runner passes that ID to Cartwheel, which records it as `cartwheel.scenario_id` in the trace's metadata. Langfuse gives the trace a separate ID. Query that metadata to get the trace ID, then paste the result into Langfuse's **Tracking → Traces** search box with **IDs / Names** selected:

  ```bash
  docker compose -f observability/docker-compose.yml exec -T clickhouse \
    clickhouse-client --user clickhouse --password clickhouse --database default \
    --query "SELECT id FROM traces WHERE JSONExtractString(metadata['attributes'], 'cartwheel.scenario_id') = 'pilot-0014' LIMIT 5"
  ```

  Replace `pilot-0014` with the case you want. `SELECT id` asks for the trace ID; the `WHERE` clause matches the scenario label; `LIMIT 5` caps the results. For this example, the trace ID was `7fe6e52415184c9ea67846417932afad`.
- **Coverage** cases check ordinary capabilities across roles and intents. **Challenge** cases probe difficult conditions. Both need grounded expectations.
- A tool may behave correctly even when the agent chooses the wrong action. In `pilot-0007`, the refund tool correctly queued a $171 request; the agent's unclarified choice of order was the concern.
- **Validity and failure are separate decisions:** First decide whether the scenario and its expected result are fair and grounded. Only then decide whether the agent's observed behavior failed that test or a clear specification requirement. `pilot-0007` had a flawed expectation; `pilot-0014` had a sound expectation and showed an escalation failure.
- **Read the whole trace:** A run can pass its planned check yet violate another clear specification requirement. Compare tool outputs with the final reply, record the unexpected error precisely, and keep it distinct from the original expectation. `pilot-0021` did not invent a product name but changed a -$5 tool value to +$5 in its reply.
- **Use precise role names:** Say shopper or merchant when the distinction matters. The word customer can refer to different parties in a marketplace or B2B setting and is weak evidence on its own.

## Parking lot

- During the final dataset work, use the underlying two-matching-orders pattern for an ambiguity challenge rather than copying the exact `pilot-0007` request.
- Decide later whether to collect lessons from all homework assignments in a shared notes file.
- Future improvement idea: have an order lookup or integrity check compare `orders.store_id` with the referenced product's `store_id` and flag mismatches for human review. Keep the deliberately damaged HW3 record intact while evaluating the current agent.
- Future tool improvement: include the product title in each authorized `find_order` and `get_order` result. Both return product IDs without titles, making it harder to verify the agent's choice in a trace. Preserve the permission checks. Keep the current HW3 run as the baseline, and make this change before a future, separately saved run.
- Future trace improvement: add `scenario_group` (`coverage` or `challenge`) to Langfuse trace metadata from the scenario file. The current traces show `cartwheel.scenario_id`, but not the group, so reviewers must look it up in `scenarios/support_scenarios.jsonl`. This would help reviewers see the intended case type while inspecting a trace; it would not change existing traces retroactively.
