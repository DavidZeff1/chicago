## 1. Elementary School Quality Score (`map_elementary_quality.py`)

**What it shows:** A comprehensive quality rating for elementary schools (ES) in each Chicago community, scored 0-100.

**How it's calculated:**

| Category                       | Component                      | Max Points |
| ------------------------------ | ------------------------------ | ---------- |
| **Environment (25 pts)**       | Safety Score                   | 10         |
|                                | Environment Score              | 8          |
|                                | Low Misconduct Rate (inverted) | 7          |
| **Teaching (25 pts)**          | Instruction Score              | 10         |
|                                | Teachers Score                 | 8          |
|                                | Leaders Score                  | 7          |
| **Family/Attendance (20 pts)** | Family Involvement             | 7          |
|                                | Parent Engagement              | 6          |
|                                | Student Attendance             | 7          |
| **Academics (30 pts)**         | PK-2 Literacy %                | 8          |
|                                | PK-2 Math %                    | 8          |
|                                | Gr3-5 Math %                   | 7          |
|                                | Gr3-5 Reading %                | 7          |

**Why it's useful:** Parents choosing elementary schools can see which neighborhoods have the best overall elementary education. The score balances safety, teaching quality, family engagement, and age-appropriate academic outcomes (PK-5 metrics).

---

## 2. Middle School Quality Score (`map_middle_quality.py`)

**What it shows:** A comprehensive quality rating for middle schools (MS) in each Chicago community, scored 0-100.

**How it's calculated:**

| Category                       | Component                      | Max Points |
| ------------------------------ | ------------------------------ | ---------- |
| **Environment (25 pts)**       | Safety Score                   | 10         |
|                                | Environment Score              | 8          |
|                                | Low Misconduct Rate (inverted) | 7          |
| **Teaching (25 pts)**          | Instruction Score              | 10         |
|                                | Teachers Score                 | 8          |
|                                | Leaders Score                  | 7          |
| **Family/Attendance (20 pts)** | Family Involvement             | 7          |
|                                | Parent Engagement              | 6          |
|                                | Student Attendance             | 7          |
| **Academics (30 pts)**         | Gr6-8 Math %                   | 8          |
|                                | Gr6-8 Reading %                | 8          |
|                                | Gr8 Explore Math %             | 7          |
|                                | Gr8 Explore Reading %          | 7          |

**Why it's useful:** Middle school is a critical transition period. This map uses grade 6-8 specific metrics and the 8th grade EXPLORE test (a pre-ACT assessment) to show which communities have strong middle schools preparing students for high school.

---

## 3. High School Quality Score (`map_highschool_quality.py`)

**What it shows:** A comprehensive quality rating for high schools (HS) in each Chicago community, scored 0-100.

**How it's calculated:**

| Category                       | Component                      | Max Points |
| ------------------------------ | ------------------------------ | ---------- |
| **Environment (20 pts)**       | Safety Score                   | 8          |
|                                | Environment Score              | 6          |
|                                | Low Misconduct Rate (inverted) | 6          |
| **Teaching (20 pts)**          | Instruction Score              | 8          |
|                                | Teachers Score                 | 6          |
|                                | Leaders Score                  | 6          |
| **Family/Attendance (15 pts)** | Family Involvement             | 5          |
|                                | Parent Engagement              | 5          |
|                                | Student Attendance             | 5          |
| **Academics/College (45 pts)** | Graduation Rate                | 10         |
|                                | College Eligibility %          | 8          |
|                                | College Enrollment Rate %      | 8          |
|                                | ACT Score (normalized to 36)   | 8          |
|                                | Algebra Pass Rate              | 6          |
|                                | Freshman on Track Rate         | 5          |

**Why it's useful:** High school quality heavily determines college and career outcomes. This score weights academics and college readiness at 45% — the highest of any category — because that's what matters most at this level. It answers: "Which neighborhoods prepare students best for life after high school?"

---

## 4. College Readiness Score (`map_college_readiness.py`)

**What it shows:** A focused score measuring only how well high schools prepare students for college, scored 0-100.

**How it's calculated:**

| Component                    | Max Points | Why this weight                          |
| ---------------------------- | ---------- | ---------------------------------------- |
| College Eligibility %        | 25         | Meeting college admission requirements   |
| College Enrollment Rate %    | 25         | Actually going to college                |
| Graduation Rate %            | 20         | Can't go to college without graduating   |
| ACT Score (normalized to 36) | 20         | Standardized measure of readiness        |
| Freshman on Track Rate %     | 10         | Early indicator of graduation likelihood |

**Why it's useful:** Unlike the full high school quality score, this strips away everything except college outcomes. It's the purest measure of "if my kid goes to high school here, will they end up in college?" Useful for families where college is the primary goal.

---

## 5. Overall School Quality Score (`map_overall_quality.py`)

**What it shows:** A universal quality score applied to ALL schools (elementary, middle, and high) using only metrics that exist across all school types, scored 0-100.

**How it's calculated:**

| Component                      | Max Points |
| ------------------------------ | ---------- |
| Safety Score                   | 15         |
| Instruction Score              | 15         |
| Environment Score              | 10         |
| Low Misconduct Rate (inverted) | 10         |
| Teachers Score                 | 10         |
| Leaders Score                  | 10         |
| Family Involvement             | 10         |
| Parent Engagement              | 10         |
| Student Attendance             | 10         |

**Why it's useful:** This gives a single "overall education quality" view of each neighborhood by averaging all schools together. It answers: "Generally speaking, how good are the schools in this area?" Good for getting a quick snapshot without diving into elementary vs. middle vs. high school separately.

---

## 6. Academic Performance Score (`map_academic_performance.py`)

**What it shows:** Pure academic achievement based on standardized test scores, scored 0-100.

**How it's calculated:**

| Component                | Max Points |
| ------------------------ | ---------- |
| ISAT Exceeding Math %    | 50         |
| ISAT Exceeding Reading % | 50         |

**Why it's useful:** This is the most objective measure — standardized test performance only. No subjective scores, no surveys. It shows which neighborhoods have students performing at the highest levels academically. Useful for comparing raw academic output across communities.

---

## 7. Safety & Environment Score (`map_safety_environment.py`)

**What it shows:** How safe and conducive to learning each community's schools are, scored 0-100.

**How it's calculated:**

| Component                      | Max Points | What it measures                   |
| ------------------------------ | ---------- | ---------------------------------- |
| Safety Score                   | 35         | Physical safety, security          |
| Environment Score              | 35         | Learning environment quality       |
| Low Misconduct Rate (inverted) | 30         | Behavioral issues (fewer = better) |

**Why it's useful:** Some parents prioritize safety above academics. This map isolates just the safety and environment factors. It answers: "Where will my child be physically safe and in a good learning environment?" — especially relevant for families moving from areas with school safety concerns.

---

## 8. Parent & Community Engagement Score (`map_engagement.py`)

**What it shows:** How involved families and the community are in schools, scored 0-100.

**How it's calculated:**

| Component                | Max Points | What it measures                        |
| ------------------------ | ---------- | --------------------------------------- |
| Family Involvement Score | 35         | How much families participate in school |
| Parent Engagement Score  | 35         | How engaged parents are with education  |
| Parent Environment Score | 30         | How welcoming schools are to parents    |

**Why it's useful:** Research shows parent involvement is one of the strongest predictors of student success. This map shows which communities have strong school-family connections. High engagement often indicates: active PTAs, good communication, parents who show up to events, and schools that welcome family participation.

---

## Summary Table

| Map                  | Focus                          | Best for answering                      |
| -------------------- | ------------------------------ | --------------------------------------- |
| Elementary Quality   | ES schools, full picture       | "Best neighborhoods for young kids?"    |
| Middle Quality       | MS schools, full picture       | "Best neighborhoods for pre-teens?"     |
| High School Quality  | HS schools, full picture       | "Best neighborhoods for teenagers?"     |
| College Readiness    | HS only, college outcomes      | "Where do kids actually go to college?" |
| Overall Quality      | All schools, universal metrics | "Generally good schools here?"          |
| Academic Performance | Test scores only               | "Where are kids scoring highest?"       |
| Safety & Environment | Safety metrics only            | "Where are schools safest?"             |
| Engagement           | Parent involvement only        | "Where are families most involved?"     |
