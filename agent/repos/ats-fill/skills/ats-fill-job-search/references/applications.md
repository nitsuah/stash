---
up: "[[repos/ats-fill]]"
title: "ats-fill · applications"
source: https://github.com/nitsuah/auto-apply-plugin/blob/main/skills/ats-fill-job-search/references/applications.md
kind: repo-doc
repo: ats-fill
---

# Resumes, cover letters and application answers

## Resume

**Structure** (1 page early career, up to 2 pages experienced; US federal resumes differ, see USAJOBS):
1. Name, city/state, phone, email, LinkedIn/portfolio/GitHub as relevant. No photo, age, or marital status in US/UK/Canada applications.
2. Optional 2–3 line summary aimed at the target role family.
3. Experience, reverse-chronological: employer, title, location, dates, 3–6 bullets per recent role.
4. Skills, grouped (languages, platforms, tools, domains). Only what the candidate can discuss in an interview.
5. Education, certifications, selected projects/publications.

**Bullets: impact, not duties.** Pattern: *action verb + what you did + how + measurable result or scope*.

- Weak: "Responsible for CI/CD pipelines."
- Strong: "Rebuilt CI on ephemeral runners for 40 services, cutting median build time from 18 to 7 minutes and saving $9k/month."

No exact number? Use honest scope (team size, users, volume, frequency) or a qualitative outcome ("adopted by all four product teams"). Never invent metrics.

**Tailoring per application** (10–15 minutes, not a rewrite):
- Reorder bullets so the 2–3 most relevant achievements lead each role.
- Mirror the JD's terminology where it truthfully describes the candidate's work (e.g. "observability" vs "monitoring").
- Adjust the summary line to the role's mission.
- Keep a master resume with everything; tailor copies from it.

**About "ATS optimization."** Applicant tracking systems mostly store, search and route applications; humans make the decisions. What actually matters:
- Clean, single-column layout; standard headings (Experience, Education, Skills); real text, not text in images.
- PDF unless the employer asks for DOCX.
- Relevant terms present *in context*. Keyword stuffing, white-text tricks and copied JD paragraphs backfire with human reviewers.

Further reading: [CareerOneStop: Resumes](https://www.careeronestop.org/JobSearch/Resumes/resumes.aspx), [CareerOneStop: References](https://www.careeronestop.org/JobSearch/Resumes/references.aspx).

## Cover letters

Write one when it's requested, when the role is a stretch or a career change that needs explaining, or for small companies where a human reads everything. 200–350 words, three short parts:

1. **Why this role here.** One specific reason tied to the company's product, mission or a recent development. Not flattery.
2. **Why you.** Two concrete, relevant achievements mapped to the role's top needs.
3. **Close.** Enthusiasm and a clear next step.

Address gaps or pivots briefly and positively. Guide: [CareerOneStop: Cover letters](https://www.careeronestop.org/JobSearch/Resumes/cover-letters.aspx).

## Application questions

Free-text questions are where tailored answers matter most. ats-fill can draft them with the JD and profile as context; the candidate edits.

| Question type | Approach |
| --- | --- |
| "Why do you want to work here?" | Specific to the company + specific to the role + what you'd bring. 3–5 sentences. |
| "Describe your experience with X" | One concrete example: context, what you did, result. Mention depth honestly ("used in production for 2 years" vs "coursework"). |
| "Tell us about a challenge" | Short STAR (see [interviews.md](interviews.md)), emphasizing the action and what you learned. |
| Salary expectations | Prefer a researched range, or "open, based on the full package; my research suggests $X–$Y for this scope." Some US states and cities bar employers from asking salary *history*; expectations are fair game. See [offers.md](offers.md). |
| Work authorization / sponsorship | Answer accurately; the candidate's legal status is not something to optimize. |
| Demographic / EEO questions | Voluntary in the US; "decline to self-identify" is always acceptable. ats-fill leaves these off by default. |
| Knock-out yes/no questions | Answer truthfully; a false "yes" surfaces in interviews or background checks. |

**Review checklist before submit**: company and role names correct (no leftover names from another application); dates and titles match the resume; tone sounds like the candidate; no AI filler ("I am thrilled to leverage my synergies"); character limits respected; uploads are the right versions.

## Portfolio and public proof

For roles where work can be shown (engineering, design, writing, data, marketing): 2–4 strong, relevant samples beat 20 weak ones. Each needs a short write-up: the problem, the candidate's role, the decisions, and the outcome. Remove anything confidential from past employers.
