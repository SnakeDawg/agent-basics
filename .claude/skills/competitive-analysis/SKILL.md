---
name: competitive-analysis
description: Run a structured competitive analysis on a competitor, set of competitors, or product category. Trigger when the user asks to analyze a competitor, compare positioning, identify gaps, build a feature/price comparison, or map a competitive landscape.
---

# Competitive analysis

A structured procedure for analyzing one or more competitors, or a competitive landscape across a product category. The procedure is the same whether invoked directly or by the `research-analyst` agent — context (company strategy, target personas, etc.) is loaded by the caller before this skill runs, not by the skill itself.

## When this triggers

- The user asks to analyze a specific competitor.
- The user asks for a competitive landscape, feature comparison, or positioning map.
- The user asks where competitors converge, diverge, or have gaps.
- A research agent delegates a competitor-related question.

## Steps

1. **Identify the set** — confirm which competitors are in scope. If the user said "our competitors" without naming them, ask. If they named a category, propose a candidate set (3–7 competitors) and confirm before profiling.
2. **Profile each competitor** — for every competitor in scope: positioning statement, target buyer, primary product line, pricing approach (list / negotiated / freemium / etc.), recent strategic moves (last 12 months). Cite sources per fact.
3. **Comparison matrix** — a markdown table comparing the set across the dimensions that matter for the user's question. Choose dimensions that produce real differences, not boilerplate.
4. **Gaps and openings** — where the set converges (commoditized), where it diverges (differentiation territory), where any single competitor is overextended or under-defended.
5. **Strategic implications** — only if the caller loaded shared context (company strategy, personas, archetypes), tie findings back to it. If no context was loaded, omit this section.

## Output format

A markdown report with these sections, in order:

- **Competitor set** — bulleted, each with a one-line positioning
- **Profiles** — one short subsection per competitor
- **Comparison matrix** — markdown table
- **Gaps and openings** — bulleted; lead with the most actionable
- **Strategic implications** — only if shared context was loaded
- **Sources** — every external citation, at the end

Cite every external source inline as a markdown link. Be precise about what's reported vs. inferred — don't blur the line between "competitor X said this on their pricing page" and "competitor X probably charges this based on signals."
