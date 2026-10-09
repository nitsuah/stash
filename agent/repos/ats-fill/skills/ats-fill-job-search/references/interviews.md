---
up: "[[repos/ats-fill]]"
title: "ats-fill · interviews"
source: https://github.com/nitsuah/ats-fill/blob/main/skills/ats-fill-job-search/references/interviews.md
kind: repo-doc
repo: ats-fill
---

# Interviews

## The one-page prep sheet (build one per interview)

1. **Company**: what they sell, to whom, business model, recent news, competitors.
2. **Role mission**: the problem this hire solves; top 3 responsibilities from the JD.
3. **Their likely concerns** about this candidate (gaps, pivots, level, tenure) and a short honest answer for each.
4. **Story map**: 6–8 stories (below) tagged to the competencies the JD emphasizes.
5. **Technical/domain topics** to refresh.
6. **Questions to ask**, at least 5, tailored to each interviewer.
7. **Logistics**: names and titles of interviewers, format, time zone, link or address, what to bring.

ats-fill's Interview Prep generates likely questions from the saved job's JD; use them as raw material for sections 4 and 5.

## Story bank (STAR-R)

Prepare stories once, reuse them everywhere. Use **Situation → Task → Action → Result → Reflection**:

- **S/T (15%)**: just enough context to understand the stakes.
- **A (60%)**: what *the candidate* did, with "I" not "we": decisions, trade-offs, how they influenced others.
- **R (15%)**: measurable or observable outcome.
- **Reflection (10%)**: what they learned or would do differently.

Aim for ~2 minutes per answer. Cover these themes; one story can cover several:

| Theme | Typical prompts |
| --- | --- |
| Hard project / technical depth | "Tell me about the most complex thing you've built" |
| Conflict or disagreement | "…disagreed with a colleague or manager" |
| Failure or mistake | "…a time you failed"; own it, show the fix and the learning |
| Ambiguity | "…unclear requirements" |
| Leadership without authority | "…got others to adopt your idea" |
| Prioritization under pressure | "…too much to do" |
| Incident / crisis | "…something broke in production" |
| Fast learning | "…learned something new quickly" |
| Feedback received and acted on | "…critical feedback" |
| Customer / user impact | "…went above and beyond for a user" |

References: [MIT CAPD: The STAR method](https://capd.mit.edu/resources/the-star-method-for-behavioral-interviews/), [CareerOneStop: Get ready to interview](https://www.careeronestop.org/JobSearch/Interview/get-ready.aspx).

## Common openers

- **"Tell me about yourself"**: 60–90 seconds, present → past → future: current role and a signature win; the thread through earlier roles; why this role is the logical next step.
- **"Why are you leaving?"**: forward-looking and neutral; never disparage an employer.
- **"Why us?"**: one product/mission reason, one team/role reason, one "what I'd bring."
- **"Weakness?"**: a real, non-fatal one, plus the concrete system the candidate uses to manage it.
- **Gaps or layoffs**: one calm sentence of fact, one sentence on what they did during it, then pivot to readiness.

## Technical interviews

**Coding**
1. Restate the problem and clarify inputs, outputs, constraints, edge cases.
2. Talk through a brute-force approach and its complexity first.
3. Improve, explaining trade-offs; agree on an approach before coding.
4. Code readably; narrate decisions.
5. Test with examples and edge cases; fix bugs calmly.
6. State time/space complexity and possible extensions.

Practice resources: [Tech Interview Handbook](https://www.techinterviewhandbook.org/), [Coding Interview University](https://github.com/jwasham/coding-interview-university).

**System design**: clarify requirements and scale → define APIs and data model → high-level components → deep-dive bottlenecks (storage, caching, queues, consistency) → reliability, observability, security → trade-offs and what would change at 10× scale. Resource: [System Design Primer](https://github.com/donnemartin/system-design-primer).

**Take-homes**: ask about the time expectation and evaluation criteria; timebox; include a short README covering assumptions, trade-offs, how to run, and what you'd do with more time.

**Non-engineering technical rounds** (case studies, portfolio reviews, presentations): structure first (agenda, framework), show reasoning aloud, tie conclusions to the business goal, leave time for questions.

## Questions to ask them

- What would make someone exceptionally successful here in the first 90 days? In a year?
- What are the biggest problems this team needs solved right now?
- How is success measured for this role, and who measures it?
- How are decisions made when the team disagrees?
- How does the team handle incidents, deadlines and technical debt?
- What has changed most on the team in the last year?
- Why is this role open?
- Is there anything about my background that gives you pause? (Then address it.)
- What are the next steps and timeline?

## Interview-day practice

- Rehearse stories **aloud**, ideally recorded or with a friend; mock interviews beat re-reading notes.
- Video calls: test camera, mic and screen share; neutral background; notes off-camera but nearby; water.
- Arrive (or join) 5–10 minutes early. Bring copies of the resume and the prep sheet.
- Take brief notes on what each interviewer cared about; they shape the thank-you.

Many companies use structured interviews with scored competencies ([Google re:Work: structured interviewing](https://rework.withgoogle.com/intl/en/guides/a-guide-to-structured-interviewing-for-better-hiring-practices)); concrete, complete stories score higher than general claims.

**Questions they shouldn't ask.** In the US, questions about age, religion, national origin, pregnancy, disability, marital or family status are generally off-limits; see [EEOC: prohibited practices](https://www.eeoc.gov/prohibited-employment-policiespractices). The candidate can redirect ("I'm fully able to meet the role's schedule requirements") or decline.

## After each interview

1. **Thank-you within 24 hours**, one per interviewer if possible: thanks, one specific reference to the conversation, a one-line reminder of fit, and any promised follow-up.
2. **Log it in ats-fill**: stage, date, interviewers, questions asked, stories used, gaps, and the candidate's own read. Update status to Interview.
3. **Debrief honestly**: what landed, what didn't; patch the story bank.
4. **Follow up** if the promised timeline passes: a short, polite check-in, then once more a week later.

Thank-you template:

> Hi Dana, thank you for the conversation today. I especially enjoyed digging into how the team is approaching the move to multi-region. It's exactly the kind of problem I tackled at Northwind when we cut failover time from 30 to 3 minutes. As promised, here's the write-up I mentioned [link]. I'm excited about the role and look forward to next steps.
