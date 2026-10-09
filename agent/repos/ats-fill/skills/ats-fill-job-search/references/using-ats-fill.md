---
up: "[[repos/ats-fill]]"
title: "ats-fill · using-ats-fill"
source: https://github.com/nitsuah/ats-fill/blob/main/skills/ats-fill-job-search/references/using-ats-fill.md
kind: repo-doc
repo: ats-fill
---

# Using ats-fill effectively

ats-fill is a local-first Chrome extension (Manifest V3). Everything it stores lives in `chrome.storage.local` on the candidate's device. There is no server, account or telemetry. Outside requests happen only when the candidate triggers them: job-board searches, optional LinkedIn/Google profile import, and Google's Gemini API when they add their own key.

- Install: [Chrome Web Store](https://chromewebstore.google.com/detail/ats-fill/amofaeopfmaicbiijgjaojenedkkadmn), or load unpacked from [the repo](https://github.com/nitsuah/ats-fill)
- Feature list: [docs/FEATURES.md](https://github.com/nitsuah/ats-fill/blob/main/docs/FEATURES.md) · Privacy: [docs/PRIVACY.md](https://github.com/nitsuah/ats-fill/blob/main/docs/PRIVACY.md)

## First-run setup (10 minutes)

1. **Accept the privacy consent** in Profile. Nothing is stored before it.
2. **Upload the resume** (PDF, DOCX or pasted text). With a Gemini key it is parsed into structured fields; without one, fill in Core profile by hand.
3. **Check every parsed fact** against the real resume: names, dates, titles, employers, degrees, certifications. Parsing is a draft.
4. **Fill Preferences and defaults**: work authorization, sponsorship, start date, availability, salary range, remote preference, and short reusable "Why this company / Why this role / Additional info" answers.
5. **Leave sensitive fields off** (gender, race, veteran, disability) unless the candidate deliberately wants them filled. They are never sent to AI models.
6. **Optional: add a free Gemini key** in Settings ([get one](https://aistudio.google.com/app/apikey)) and leave the model on **Auto**. Fill, tracking, search and analytics work without it.

## Filling an application

| Platform | Detection | Fill |
| --- | --- | --- |
| Greenhouse, Lever, Ashby, LinkedIn Easy Apply | yes | full |
| Workday, iCIMS, Jobvite, Phenom/Circle, generic forms | yes | partial; expect more manual review |

1. Open the application page, then open ats-fill. **Detected ATS** in Readiness should name the platform.
2. Press **Preview** to see every answer it will use. Search the list, fix anything wrong, and note questions it flags.
3. Press **Fill this form** (or fill from Preview). Fields are filled in place on the page.
4. Read the **Last fill** card: *filled* / *kept* (existing values left alone) / *to review* (no saved answer, or file fields). Handle every "to review" item yourself.
5. Upload files, answer attestations and legal/demographic questions, read the whole form, and **submit it yourself**. ats-fill never submits.
6. Press **Mark submitted** so the pipeline records it.

Tips:
- If nothing fills on a supported page, reload the tab once; ats-fill retries content-script injection automatically, but a stale tab can still need a reload.
- Multi-page applications (Workday especially): fill each page, then review before pressing Next.
- Corrections you make on forms become **Memory**. Review it in Profile → Memory: edit, ignore (restore later) or delete each remembered answer. Prune stale ones monthly.

## Job search

- **16 sources**: nine keyless boards on by default (Remotive, Arbeitnow, The Muse, Remote OK, Jobicy, Working Nomads, HN Who's Hiring, We Work Remotely, remote.co); Indeed and Hackajob; keyed sources (Adzuna, USAJOBS, Reed, Jooble) after adding keys in Settings; LinkedIn when the candidate is already signed in to LinkedIn in the browser (uses that session; say so before suggesting it).
- **Custom RSS sources** (Settings): add state workforce boards, niche communities or a target company's careers feed. Each one asks for permission to read only that site.
- Search a specific role family ("platform engineer", "clinical research coordinator") rather than a broad title, then use the source chips, **Filters** (remote, type, region) and the pay range. Tick **hide unknown pay** when transparency matters.
- Read the source-confidence hint on each card; verify promising listings on the employer's own careers site before investing time.
- **Save job** puts it in the pipeline as a draft with title, company, pay and description.

## Pipeline (tracker)

- Stages: Drafted → Filled → Submitted → Pending → Interview → Offer, plus Rejected and Retired. Drag cards between stages or change status on the card.
- Per job: pay band, location, employment type, remote, notes, **verdict** (Strong yes, Lean yes, Neutral / maybe, Lean no, No, Need more research, Interview prep) and a **scorecard**. Fill the verdict *before* applying, so the reasoning is captured before the outcome is known.
- **Add job** captures the current tab or a pasted description; with a Gemini key, **Clean up** strips boilerplate and **Summarize** produces a short brief.
- **Import CSV** brings in history from a spreadsheet (flexible headers: Company, Role Title, Status, Date, Location, Pay Min/Max, Scorecard, Verdict, URL, Notes). **Export CSV** anytime; it is also the GDPR/CCPA data export.
- Use the **Active / All** toggle to hide closed jobs while working.

## Analytics

Computed locally from the pipeline: response rate by source, response rate by salary band, and time to first response. Read them after 15–20 applications, not 3. Use them to shift effort toward sources and pay bands that actually reply. Response times for entries logged before the first-response timestamp existed are approximate.

## Interview Prep

Pick a saved job; with a Gemini key, ats-fill generates likely questions from that job's description and the profile, each with a suggested answer structure. Draft answers inline; they save locally per job. Treat the list as a starting point and add company-, interviewer- and role-specific questions (see [interviews.md](interviews.md)).

## Privacy and data controls

- Help & Privacy → **Clear temp cache** removes working state only; **Delete all local data** wipes everything, including consent.
- Profile import via LinkedIn or Google uses the candidate's own OAuth client and only pre-fills name and email.
- Keys (Gemini, board APIs, OAuth) are the candidate's own and stay local.

## Recommended weekly rhythm with the app

| When | Do |
| --- | --- |
| Mon | Search 2–3 role families; save 10–15 promising roles with verdicts |
| Tue–Thu | Tailor and apply to the best 5–8; Preview → Fill → review → submit → Mark submitted |
| Daily, 10 min | Update stages, log responses, prune Memory |
| Interview booked | Run Interview Prep on that job; build the prep sheet |
| Fri | Read Analytics; adjust sources, targets or materials; export CSV as a backup |
