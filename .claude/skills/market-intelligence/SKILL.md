---
name: market-intelligence
description: Run a structured market intelligence pass on a topic, segment, or trend. Trigger when the user asks for market sizing, demand signals, buyer behavior, adjacent trends, or to research a market or industry segment.
---

# Market intelligence

A structured procedure for assessing a market segment, demand pattern, or industry trend. The procedure is the same whether invoked directly or by the `research-analyst` agent — context (personas, strategy, etc.) is loaded by the caller before this skill runs, not by the skill itself.

## When this triggers

- The user asks to research a market segment or industry.
- The user asks about TAM/SAM/SOM, market sizing, or demand signals.
- The user asks about buyer behavior, purchase cycles, or decision criteria.
- A research agent delegates a market intelligence question.

## Steps

1. **Define the segment** — restate the segment or topic in one sentence. If the boundary is ambiguous (e.g., "the workstation market" — pro vs. consumer? mobile vs. desktop?), confirm with the user before sizing.
2. **Sizing** — gather TAM/SAM/SOM signals from public sources. Note the time window of each data point (e.g., "FY2025 estimate from Gartner, dated 2025-Q3").
3. **Demand signals** — recent reporting on growth/decline, hiring trends, RFPs, conference traffic, search-volume shifts. Date every signal.
4. **Buyer behavior** — typical decision criteria, purchase cycles, evaluation length, key personas if known. If shared persona context was loaded by the caller, reference it here.
5. **Adjacent trends** — technologies, regulations, or substitutes that materially shift the segment. Flag direction (tailwind vs. headwind).
6. **Risks and assumptions** — every claim that depends on a single source, an interpolation, or a forward-looking estimate. Be explicit about what's solid vs. inferred.

## Output format

A markdown report with these sections, in order:

- **Segment definition** — one sentence
- **Sizing** — TAM/SAM/SOM with date stamps and source links
- **Demand signals** — bulleted, each dated
- **Buyer behavior** — short paragraph or bulleted
- **Adjacent trends** — bulleted, with direction (tailwind / headwind / neutral)
- **Risks and assumptions** — bulleted
- **Sources** — every external citation, listed at the end

Cite every external source inline as a markdown link. Don't fabricate numbers — if a figure isn't sourced, omit it or say "not found in available sources."
