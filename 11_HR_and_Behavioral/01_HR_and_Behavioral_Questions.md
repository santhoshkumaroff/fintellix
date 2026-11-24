# HR & Behavioural Questions (JD: Mindset – "Curious, eager to learn, keen to automate manual work"; Soft skills – "Analytical thinking, problem-solving, communication")

> Use the **STAR** method for experience questions: **S**ituation → **T**ask → **A**ction → **R**esult (with a number if possible). Keep answers 60–90 seconds.

### Q1. Tell me about yourself.
**Structure:** Present (education/current) → Relevant skills + project → Why this role → (one personal line).
- **Example 1, fresher:** "I'm a final-year B.E. Computer Science student at XYZ College. Over the last year I've focused on Python and GenAI. My main project is a RAG chatbot that answers questions over RBI circulars with citations, which I evaluated on a 40-question test set at 85% accuracy. I also automated my department's attendance consolidation with pandas, saving about 3 hours a week. I'm applying to Fintellix because the role combines exactly these skills with banking data, where accuracy really matters, and I'd learn the regulatory domain from experts."
- **Example 2, recent graduate with some experience:** "I graduated in 2025 in Data Science. I spent six months as a data intern at a logistics firm cleaning shipment data and building Python reports. Since then I've built two GenAI projects, a text-to-SQL assistant on a loan dataset and a PDF invoice extractor. I want to go deeper into GenAI for financial data, and Fintellix's regulatory reporting work is a strong fit."

### Q2. Why do you want this internship? Why Fintellix?
See `01_Company_and_Products/01_About_Fintellix_and_ICRA.md` Q3. Mention: live projects from the first weeks, Claude/RAG work, the banking domain, being part of Group ICRA, a 9-month structured training.

### Q3. Why banking / regulatory technology? Do you have any finance background?
**Answer:** Be honest and show curiosity. "I don't have formal finance training, but I've started learning. I now understand NPA, SMA buckets, LCR and ECL basics. What attracts me is that the data has to be exactly right and traceable, which makes the engineering challenge more interesting."
- **Example 1:** "I read about RBI moving reporting to its CIMS data warehouse. It showed me how central data quality is."
- **Example 2:** "My family uses digital banking daily. I'm curious how the bank's numbers reach the regulator."

### Q4. This is a 9-month, work-from-office internship in Bengaluru. Are you okay with that?
**Answer:** A clear yes, plus why it helps. "Yes. Being in the office helps me learn faster from the team, especially a domain as specialised as regulatory reporting." (Be truthful about exam dates or other commitments. Raise them now.)

### Q5. What are your strengths?
Pick 2–3 that match the JD, each with proof.
- **Example 1, "I automate repetitive work":** "In my internship I noticed we rebuilt the same weekly report by hand. I scripted it, and now it runs in 2 minutes."
- **Example 2, "I learn fast and test what I build":** "I learned RAG in 3 weeks and didn't stop at a demo. I built a test set to measure accuracy."

### Q6. What is your weakness?
**Answer:** A real but non-critical weakness, plus what you're doing about it.
- **Example 1:** "I used to go deep into perfecting code before sharing it. Now I share early drafts for feedback; my last project improved faster because of a mentor's early review."
- **Example 2:** "Public speaking made me nervous, so I volunteered to present at our college tech club twice this semester."

### Q7. Tell me about a challenging problem you solved. (problem-solving)
- **Example 1, STAR:** "S: My RAG bot gave wrong answers for questions about tables. T: Find the cause and fix it. A: I logged the retrieved chunks and saw the table text was scrambled by PDF extraction. I switched to pdfplumber for tables and stored them as markdown chunks. R: Accuracy on table questions rose from 50% to 80%."
- **Example 2:** "S: A pandas script crashed on a 3 GB file. A: I read it in chunks with only the needed columns and category dtypes. R: Memory fell from about 8 GB to under 1 GB, and it ran in 4 minutes."

### Q8. Describe a time you worked in a team / had a conflict.
- **Example 1:** "In our final-year project, two of us disagreed about FAISS vs Chroma. Instead of arguing, we ran both on our data for a day and compared speed and setup. Chroma's metadata filtering won, and we documented why."
- **Example 2:** "A teammate kept missing deadlines. I talked to him privately and learned he was stuck on the frontend. We paired for two evenings and the module shipped on time."

### Q9. Tell me about a time you made a mistake.
**Answer:** Own it, describe the fix, and the lesson (ideally a process change).
- **Example 1:** "I pushed a config with my API key to GitHub. I revoked the key within minutes, rotated it, added `.env` to `.gitignore`, and set up a pre-commit secret scanner."
- **Example 2:** "My report double-counted customers because I summed per loan instead of per customer. I caught it while reconciling with totals, and now I always reconcile outputs against an independent total."

### Q10. How do you learn a new technology quickly? (curiosity / eagerness)
**Answer:** Official docs and a quick-start → build a tiny working example → apply it to a real problem → read others' code → teach or write about it.
- **Example 1:** "I learned LangChain by building a 50-line RAG first, then reading how its retriever works internally."
- **Example 2:** "For banking terms, I keep a glossary and connect each term to a data column, e.g. DPD → days_past_due → NPA flag."

### Q11. Where do you see yourself in 3–5 years?
**Answer:** Growth aligned with the company. "I'd like to grow into a GenAI engineer who understands both the technology and the banking domain deeply, someone who can design accurate, auditable AI features for regulatory products. I'd love to do that at Fintellix if there's a path after the internship."

### Q12. How do you handle pressure and deadlines?
- **Example 1:** "During exams plus a hackathon, I broke the hackathon work into a must-have demo and nice-to-haves, finished the core first, and we placed in the top 5."
- **Example 2:** "When priorities clash, I ask my lead which matters most rather than guessing."

### Q13. What would you do if your manager asked you to do something you didn't know how to do?
**Answer:** Say so honestly, propose how you'll learn it, give a realistic time estimate, and check in early with a draft.

### Q14. What would you do if the GenAI tool you built gave a wrong number that went into a client report?
**Answer:** Inform my lead immediately, help correct it before submission (or issue a correction), find the root cause, add a test that catches it, and add a control so numbers come from code or SQL, not from the LLM.
- **Example:** "I'd add a validation step that cross-checks every number in the generated text against the database."

### Q15. Do you have any other offers / higher studies plans?
**Answer:** Be honest but committed. "I'm focused on this role. I don't plan higher studies during the next 9 months."

### Q16. What are your stipend expectations?
**Answer:** "I'm flexible and focused on learning. I'm happy with the company's standard intern stipend." (Research typical Bengaluru tech intern stipends beforehand so you're not surprised.)

### Q17. Do you have any questions for us?
Always ask 2. See `01_Company_and_Products/01_About_Fintellix_and_ICRA.md` Q9.

### Q18. Ethics: Would you paste client data into ChatGPT or another public AI tool to finish faster?
**Answer:** "No. Client data is confidential. I'd use only company-approved tools and environments, mask or synthesise data for testing, and ask my lead if unsure."
- **Example:** "For prompt testing I'd generate synthetic loan records with fake names."

### Q19. Why should we hire you?
**Answer:** Match three JD requirements to proof. "You need strong Python, hands-on GenAI with evaluation, and a learner's mindset. I've built a RAG project with a measured 85% accuracy, I've automated real manual work with pandas, and I've already started learning your domain: NPA, LCR, ECL and RBI's CIMS. I'll be productive early and keep improving."

### Q20. Describe a time you showed initiative.
- **Example 1:** "Nobody asked, but I added an evaluation script to our team project. It caught a regression before our demo."
- **Example 2:** "I noticed our college library list was manually typed every term, so I built a small script to auto-generate it from the database."
