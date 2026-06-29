# -*- coding: utf-8 -*-
"""
Generate a 100-question MCQ question paper on "Design Thinking: A Primer".
Outputs a formatted PDF with questions, four options each, and an answer key.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)

# Each entry: (question, [opt A, opt B, opt C, opt D], correct_index 0-3)
QUESTIONS = [
    ("Design Thinking is best described as a:",
     ["Random trial-and-error method",
      "Human-centred approach to innovation and problem solving",
      "Purely technical engineering discipline",
      "Financial accounting technique"], 1),
    ("Which organisation is most closely associated with popularising Design Thinking?",
     ["NASA", "IDEO", "WHO", "OPEC"], 1),
    ("Who is the author often credited with bringing Design Thinking to business through IDEO?",
     ["Steve Jobs", "Tim Brown", "Bill Gates", "Peter Drucker"], 1),
    ("The d.school that teaches Design Thinking is part of which university?",
     ["MIT", "Harvard", "Stanford", "Oxford"], 2),
    ("At the core of Design Thinking is empathy for the:",
     ["Competitor", "Investor", "End user / customer", "Government"], 2),
    ("The classic five-stage Design Thinking model begins with which stage?",
     ["Ideate", "Empathize", "Prototype", "Test"], 1),
    ("Which is the correct order of the five stages of Design Thinking?",
     ["Define, Empathize, Ideate, Test, Prototype",
      "Empathize, Define, Ideate, Prototype, Test",
      "Ideate, Empathize, Define, Test, Prototype",
      "Prototype, Test, Ideate, Define, Empathize"], 1),
    ("The three overlapping lenses of Design Thinking are desirability, feasibility, and:",
     ["Visibility", "Viability", "Volatility", "Variability"], 1),
    ("'Desirability' in Design Thinking primarily refers to what is:",
     ["Technically possible", "Financially sustainable",
      "Meaningful and useful to people", "Legally permitted"], 2),
    ("'Feasibility' refers to what is:",
     ["Desirable to users", "Technically and organisationally possible",
      "Profitable", "Aesthetically pleasing"], 1),
    ("'Viability' refers to what is:",
     ["Technically possible", "Emotionally appealing",
      "Financially and strategically sustainable", "Easy to prototype"], 2),
    ("The main goal of the Empathize stage is to:",
     ["Build the final product", "Understand users' needs, emotions and motivations",
      "Calculate the budget", "Write marketing copy"], 1),
    ("Which is a primary method used during the Empathize stage?",
     ["Mass production", "User observation and interviews",
      "Stock analysis", "Patent filing"], 1),
    ("An 'empathy map' typically captures what the user says, thinks, does and:",
     ["Buys", "Feels", "Sells", "Owns"], 1),
    ("A fictional character representing a user segment is called a:",
     ["Avatar bot", "Persona", "Stakeholder", "Prototype"], 1),
    ("A customer journey map is used to visualise the user's:",
     ["Bank balance", "Experience and touchpoints over time",
      "Genetic profile", "Tax records"], 1),
    ("The Define stage is mainly about:",
     ["Generating many ideas", "Framing a clear, actionable problem statement",
      "Mass manufacturing", "Selling the product"], 1),
    ("A well-framed problem statement in Design Thinking is also known as a:",
     ["Mission statement", "Point of View (POV) statement",
      "Profit statement", "Press release"], 1),
    ("Which phrase is commonly used to reframe problems as opportunities for ideation?",
     ["What If Only", "How Might We", "Why Not Now", "When Could They"], 1),
    ("A good problem statement should be:",
     ["Broad and vague", "Human-centred and not prescribe a solution",
      "Focused only on technology", "About the company's revenue"], 1),
    ("The Ideate stage focuses on:",
     ["Narrowing to one idea immediately", "Generating a large quantity of diverse ideas",
      "Testing prototypes", "Conducting interviews"], 1),
    ("Brainstorming works best when participants initially aim for:",
     ["Quality over quantity", "Quantity of ideas and deferred judgment",
      "Silence", "Criticism of every idea"], 1),
    ("A key rule of brainstorming is to:",
     ["Judge ideas immediately", "Defer judgment and build on others' ideas",
      "Allow only the manager to speak", "Stop at one idea"], 1),
    ("'Going for quantity' during ideation helps because:",
     ["More ideas guarantee lower cost", "A larger pool increases chances of novel solutions",
      "It impresses investors", "It reduces the need for testing"], 1),
    ("SCAMPER is a technique used for:",
     ["Budgeting", "Stimulating creative ideas", "User testing", "Market sizing"], 1),
    ("In SCAMPER, the 'S' commonly stands for:",
     ["Sell", "Substitute", "Simplify", "Standardise"], 1),
    ("The 'C' in SCAMPER stands for:",
     ["Copy", "Combine", "Compete", "Calculate"], 1),
    ("Mind mapping is primarily a tool for:",
     ["Financial forecasting", "Organising and generating ideas visually",
      "Code compilation", "Inventory control"], 1),
    ("Divergent thinking is about:",
     ["Selecting the single best option", "Expanding and generating many possibilities",
      "Cutting costs", "Following strict rules"], 1),
    ("Convergent thinking is about:",
     ["Generating endless options", "Narrowing down and selecting the best ideas",
      "Avoiding decisions", "Ignoring constraints"], 1),
    ("The Prototype stage aims to:",
     ["Finalise mass production", "Build quick, inexpensive representations of ideas to learn",
      "Conduct payroll", "Replace the testing stage"], 1),
    ("A 'low-fidelity' prototype is typically:",
     ["A fully functional product", "Rough and inexpensive, like a paper sketch",
      "A finished mobile app", "A legal contract"], 1),
    ("The main purpose of prototyping is to:",
     ["Impress shareholders", "Learn quickly and fail cheaply",
      "Avoid talking to users", "Skip the testing phase"], 1),
    ("The Test stage is used to:",
     ["Launch the final product to the entire market",
      "Gather user feedback and refine the solution",
      "Fire underperforming staff", "Stop the project"], 1),
    ("Design Thinking is generally considered a process that is:",
     ["Strictly linear and one-directional", "Iterative and non-linear",
      "Done only once", "Independent of users"], 1),
    ("'Iteration' in Design Thinking means:",
     ["Doing the project once perfectly", "Repeating and refining steps based on learning",
      "Avoiding feedback", "Copying competitors"], 1),
    ("The Double Diamond model was popularised by the:",
     ["British Design Council", "United Nations", "World Bank", "Stanford d.school"], 0),
    ("The Double Diamond model alternates between divergent and ____ thinking.",
     ["random", "convergent", "negative", "linear"], 1),
    ("The first diamond of the Double Diamond focuses on:",
     ["Building the solution", "Finding the right problem",
      "Marketing", "Manufacturing"], 1),
    ("The second diamond of the Double Diamond focuses on:",
     ["Defining the problem", "Developing and delivering the right solution",
      "Hiring staff", "Filing patents"], 1),
    ("'Human-centred design' places which group at the centre of the process?",
     ["Shareholders", "People who will use the solution",
      "Suppliers", "Regulators"], 1),
    ("Which mindset is essential to Design Thinking?",
     ["Fear of failure", "Bias towards action and experimentation",
      "Avoiding users", "Working in isolation"], 1),
    ("A 'bias towards action' encourages designers to:",
     ["Plan endlessly without acting", "Make and test ideas rather than only discuss them",
      "Avoid prototypes", "Delay decisions indefinitely"], 1),
    ("Storytelling in Design Thinking is used to:",
     ["Confuse stakeholders", "Communicate insights and ideas persuasively",
      "Replace research", "Hide failures"], 1),
    ("Reframing a problem helps a team to:",
     ["Lock into the first solution", "See the challenge from new perspectives",
      "Avoid creativity", "Reduce empathy"], 1),
    ("'Beginner's mind' (or beginner's mindset) encourages designers to:",
     ["Assume they know everything", "Approach problems with curiosity and without assumptions",
      "Ignore the user", "Rely only on experts"], 1),
    ("Observing users in their natural environment is sometimes called:",
     ["Contextual inquiry / ethnographic observation", "Cold calling",
      "Mass surveying only", "Auditing"], 0),
    ("Open-ended interview questions are preferred because they:",
     ["Yield yes/no answers", "Encourage rich, detailed responses",
      "Save the most money", "Avoid talking to users"], 1),
    ("A 'leading question' in user research should generally be:",
     ["Encouraged", "Avoided because it biases answers",
      "Used to confuse users", "Used to sell products"], 1),
    ("Latent needs are needs that users:",
     ["State clearly and loudly", "Have but may not be able to articulate",
      "Never actually have", "Only mention in surveys"], 1),
    ("Synthesis in Design Thinking refers to:",
     ["Building the product", "Making sense of research to find patterns and insights",
      "Selling the product", "Ignoring data"], 1),
    ("An 'insight' is best described as a:",
     ["Raw data point", "Non-obvious realisation that guides design",
      "Sales figure", "Random guess"], 1),
    ("Affinity mapping (clustering sticky notes) is used to:",
     ["Calculate profit", "Group related observations to reveal themes",
      "Test prototypes", "Recruit staff"], 1),
    ("'Fail fast, fail cheap' encourages teams to:",
     ["Avoid all risk", "Learn early from inexpensive experiments",
      "Never prototype", "Hide mistakes"], 1),
    ("Which of the following is NOT one of the five classic stages?",
     ["Empathize", "Define", "Monetize", "Test"], 2),
    ("A storyboard in Design Thinking is used to:",
     ["Record finances", "Visualise a user's experience as a sequence of frames",
      "Replace prototyping entirely", "List employees"], 1),
    ("Role-playing and bodystorming are techniques used to:",
     ["Audit accounts", "Physically act out and empathise with experiences",
      "Write code", "Calculate taxes"], 1),
    ("'Wizard of Oz' prototyping involves:",
     ["A fully automated system", "Humans simulating system functions behind the scenes",
      "No users at all", "Final production"], 1),
    ("The primary benefit of testing with real users is to:",
     ["Confirm the team is always right", "Uncover flaws and gather actionable feedback",
      "Increase development cost", "Avoid iteration"], 1),
    ("In Design Thinking, failure is viewed as:",
     ["A reason to quit", "A valuable source of learning",
      "Always unacceptable", "Irrelevant"], 1),
    ("Multidisciplinary teams are valued in Design Thinking because they:",
     ["Reduce diversity of thought", "Bring varied perspectives and richer solutions",
      "Slow everything down needlessly", "Avoid collaboration"], 1),
    ("Co-creation means involving ____ in the design process.",
     ["only executives", "users and stakeholders", "only designers", "only engineers"], 1),
    ("'How Might We' statements are deliberately phrased to be:",
     ["Narrow and prescriptive", "Optimistic and open to many solutions",
      "Negative", "Purely technical"], 1),
    ("A prototype that looks and works close to the final product is called:",
     ["Low-fidelity", "High-fidelity", "Paper-only", "Verbal"], 1),
    ("Rapid prototyping emphasises:",
     ["Perfection before showing anyone", "Speed and quick feedback cycles",
      "Avoiding users", "High upfront cost"], 1),
    ("In ideation, 'building on the ideas of others' is captured by the phrase:",
     ["'No, but'", "'Yes, and'", "'Maybe later'", "'Not now'"], 1),
    ("The phrase 'Yes, and' encourages participants to:",
     ["Reject ideas", "Accept and expand on contributions", "Stay silent", "Compete"], 1),
    ("A key reason to defer judgment during ideation is to:",
     ["Reduce the number of ideas", "Create psychological safety for wild ideas",
      "Speed up firing", "Avoid prototyping"], 1),
    ("Visualisation (sketching) in Design Thinking helps to:",
     ["Hide ideas", "Make abstract ideas tangible and shareable",
      "Replace user research", "Increase confusion"], 1),
    ("Which factor does Design Thinking balance alongside human needs?",
     ["Only profit", "Technology and business viability",
      "Only aesthetics", "Only regulations"], 1),
    ("The Empathize and Define stages together are often called the ____ space.",
     ["solution", "problem", "delivery", "production"], 1),
    ("The Ideate, Prototype and Test stages are often called the ____ space.",
     ["problem", "solution", "research", "audit"], 1),
    ("'Point of View' (POV) typically combines a user, a need, and an:",
     ["Invoice", "Insight", "Advertisement", "Algorithm"], 1),
    ("Which is a common pitfall in problem definition?",
     ["Framing it around the user", "Embedding a solution inside the problem statement",
      "Keeping it human-centred", "Being specific"], 1),
    ("Prototyping helps reduce:",
     ["User involvement", "Risk and uncertainty before full investment",
      "Creativity", "Empathy"], 1),
    ("The concept of 'wicked problems' refers to problems that are:",
     ["Simple and well-defined", "Complex, ill-defined and interconnected",
      "Already solved", "Purely mathematical"], 1),
    ("Design Thinking is especially useful for tackling problems that are:",
     ["Routine and obvious", "Ambiguous and human-centred",
      "Already fully understood", "Purely numerical"], 1),
    ("A 'value proposition' describes:",
     ["The company's tax rate", "The benefit a solution offers to users",
      "The office location", "The number of employees"], 1),
    ("Empathy interviews should ideally make the interviewee feel:",
     ["Judged", "Comfortable and free to share", "Pressured to buy", "Confused"], 1),
    ("The 'Five Whys' technique is used to:",
     ["Increase sales", "Dig down to the root cause of a problem",
      "Avoid analysis", "Generate prototypes"], 1),
    ("Asking 'why' repeatedly during research helps uncover:",
     ["Surface-level facts only", "Underlying motivations and root causes",
      "Financial reports", "Competitor pricing"], 1),
    ("A 'minimum viable product' (MVP) is built to:",
     ["Include every possible feature", "Test core assumptions with minimal effort",
      "Avoid user feedback", "Maximise initial cost"], 1),
    ("In Design Thinking, constraints are viewed as:",
     ["Only obstacles", "Drivers that can spark creativity",
      "Irrelevant", "Reasons to stop"], 1),
    ("The term 'ideation' is most closely linked to which stage?",
     ["Empathize", "Define", "Ideate", "Test"], 2),
    ("Which is a divergent activity?",
     ["Selecting the final concept", "Brainstorming many ideas",
      "Cutting the idea list", "Final voting"], 1),
    ("Which is a convergent activity?",
     ["Brainstorming wildly", "Dot-voting to prioritise ideas",
      "Free association", "Generating variations"], 1),
    ("'Dot voting' is a technique to:",
     ["Generate ideas", "Quickly prioritise options as a group",
      "Interview users", "Build prototypes"], 1),
    ("Tim Brown describes Design Thinking as drawing on the designer's:",
     ["Accounting skills", "Sensibility and methods to match needs with feasibility",
      "Legal training", "Sales quotas"], 1),
    ("Which of these best reflects a Design Thinking mindset?",
     ["Assume the solution first", "Embrace ambiguity and stay curious",
      "Avoid feedback", "Work alone in secret"], 1),
    ("Prototyping 'to think' means using prototypes to:",
     ["Avoid decisions", "Explore and refine ideas, not just demonstrate them",
      "Replace strategy", "Skip empathy"], 1),
    ("Which tool helps capture the emotional highs and lows of a user experience?",
     ["Balance sheet", "Journey map with an emotional curve",
      "Org chart", "Gantt chart only"], 1),
    ("Reframing 'people don't use the stairs' as 'how might we make stairs fun' is an example of:",
     ["Ignoring the user", "Opportunity-focused problem reframing",
      "Cost cutting", "Convergent thinking"], 1),
    ("Brainstorming sessions benefit from a clear:",
     ["Ban on speaking", "Focus question or 'How Might We' prompt",
      "List of criticisms", "Single approved idea"], 1),
    ("In Design Thinking, the user's needs are discovered mainly through:",
     ["Assumptions", "Empathy and research", "Random guessing", "Sales targets"], 1),
    ("Which is the best example of a high-fidelity prototype?",
     ["A napkin sketch", "An interactive clickable app mock-up",
      "A verbal description", "A single sticky note"], 1),
    ("The overall spirit of Design Thinking can be summarised as:",
     ["Solution-first and rigid", "Human-centred, collaborative and experimental",
      "Isolated and theoretical", "Profit-only and fixed"], 1),
    ("Prototyping and testing together help teams to:",
     ["Avoid learning", "Validate or invalidate assumptions before scaling",
      "Eliminate users", "Skip empathy"], 1),
    ("A core question the Empathize stage tries to answer is:",
     ["How much profit will we make", "What do users truly need and feel",
      "Who should we fire", "Which competitor to copy"], 1),
    ("Design Thinking is sometimes described as a balance of analytical thinking and:",
     ["Random guessing", "Intuitive (creative) thinking",
      "Financial auditing", "Strict bureaucracy"], 1),
    ("Which deliverable best summarises the Define stage?",
     ["A finished product", "A clear, actionable problem statement",
      "A marketing budget", "A staffing plan"], 1),
]


def build_pdf(output_path):
    import random
    rng = random.Random(42)  # deterministic shuffle for reproducibility

    # Shuffle option order per question so the correct answer is
    # distributed across A/B/C/D instead of always being one letter.
    shuffled = []
    for q, opts, ans in QUESTIONS:
        idxs = list(range(4))
        rng.shuffle(idxs)
        new_opts = [opts[i] for i in idxs]
        new_ans = idxs.index(ans)
        shuffled.append((q, new_opts, new_ans))

    doc = SimpleDocTemplate(
        output_path, pagesize=A4,
        topMargin=18 * mm, bottomMargin=16 * mm,
        leftMargin=18 * mm, rightMargin=18 * mm,
        title="Design Thinking: A Primer - MCQ Question Paper",
    )
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleX", parent=styles["Title"], fontSize=18, leading=22,
        alignment=TA_CENTER, textColor=colors.HexColor("#1a3c6e"))
    sub_style = ParagraphStyle(
        "SubX", parent=styles["Normal"], fontSize=11, leading=15,
        alignment=TA_CENTER, textColor=colors.HexColor("#444444"))
    instr_style = ParagraphStyle(
        "Instr", parent=styles["Normal"], fontSize=9.5, leading=13,
        alignment=TA_LEFT, textColor=colors.HexColor("#333333"))
    q_style = ParagraphStyle(
        "Q", parent=styles["Normal"], fontSize=10.5, leading=14,
        spaceBefore=6, spaceAfter=2)
    opt_style = ParagraphStyle(
        "Opt", parent=styles["Normal"], fontSize=10, leading=13.5,
        leftIndent=14)
    section_style = ParagraphStyle(
        "Sec", parent=styles["Heading2"], fontSize=13,
        textColor=colors.HexColor("#1a3c6e"), spaceBefore=8, spaceAfter=4)

    story = []
    story.append(Paragraph("DESIGN THINKING: A PRIMER", title_style))
    story.append(Paragraph("Multiple Choice Question Paper", sub_style))
    story.append(Spacer(1, 6))

    meta_data = [
        ["Total Questions: 100", "Total Marks: 100"],
        ["Time Allowed: 2 Hours", "Each Question: 1 Mark"],
    ]
    meta_tbl = Table(meta_data, colWidths=[85 * mm, 85 * mm])
    meta_tbl.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#222222")),
        ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#1a3c6e")),
        ("INNERGRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9bb4d4")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_tbl)
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        "<b>Instructions:</b> Each question carries one mark. "
        "Choose the single best answer (A, B, C or D) for each question. "
        "There is no negative marking. An answer key is provided at the end of the paper.",
        instr_style))
    story.append(Spacer(1, 8))

    letters = ["A", "B", "C", "D"]
    for i, (q, opts, _) in enumerate(shuffled, start=1):
        story.append(Paragraph(f"<b>{i}.</b> {q}", q_style))
        for j, opt in enumerate(opts):
            story.append(Paragraph(f"({letters[j]}) {opt}", opt_style))

    # Answer key
    story.append(PageBreak())
    story.append(Paragraph("ANSWER KEY", section_style))
    story.append(Spacer(1, 4))

    key_rows = []
    row = []
    for i, (_, _, ans) in enumerate(shuffled, start=1):
        row.append(f"{i}. {letters[ans]}")
        if len(row) == 5:
            key_rows.append(row)
            row = []
    if row:
        while len(row) < 5:
            row.append("")
        key_rows.append(row)

    key_tbl = Table(key_rows, colWidths=[34 * mm] * 5)
    key_tbl.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 9.5),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9bb4d4")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f3f6fb")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1a3c6e")),
    ]))
    story.append(key_tbl)

    doc.build(story)


if __name__ == "__main__":
    assert len(QUESTIONS) == 100, f"Expected 100 questions, got {len(QUESTIONS)}"
    for idx, (q, opts, ans) in enumerate(QUESTIONS, start=1):
        assert len(opts) == 4, f"Q{idx} does not have 4 options"
        assert 0 <= ans <= 3, f"Q{idx} has invalid answer index"
    out = "Design_Thinking_A_Primer_MCQ.pdf"
    build_pdf(out)
    print(f"PDF generated: {out} with {len(QUESTIONS)} questions.")
