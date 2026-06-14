# Prompt: Generate Document from Template (Universal)

> This prompt is used when the agent needs to generate any InnoTech document type from raw
> user-supplied content. It handles routing, input extraction, and calls the type-specific prompt.

---

## Step 1 — Detect Document Type

Read `references/document-routing.md` and identify the target document code (BRD/PRD/SRS/FRD/TRD/API/DD/UAT/IRL).

## Step 2 — Extract Available Information

From the user's raw content, extract:
- Project name / title
- Prepared by / version / date
- Any existing sections or requirements
- Stakeholder names and roles
- Any tables, lists, or narrative content

Map extracted content to the relevant fields in the type-specific generation standard.

## Step 3 — Fill Gaps

For any required field not found in the user content, insert a clearly marked placeholder:
```
[TBD – insert PROJECT_NAME]
[TBD – insert PREPARED_BY]
```
Do NOT invent or fabricate project-specific information.

## Step 4 — Load Type-Specific Prompt

Load and execute `prompts/generate-[type].md` with the extracted inputs.

## Step 5 — Apply Style

Ensure all InnoTech style rules from `references/document-style-guide.md` and
`references/docx-generation-rules.md` are applied regardless of input format.

## Step 6 — Validate and Deliver

Run `checklists/final-review-checklist.md` before delivering the output file.
