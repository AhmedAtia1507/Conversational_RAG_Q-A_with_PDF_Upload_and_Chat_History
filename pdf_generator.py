"""
Generate synthetic PDFs for testing RAG systems.
Requires: pip install reportlab
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors

def generate_company_report(filename="test_company_report.pdf"):
    """Generate a fictional company annual report"""
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Company data (completely fictional)
    company_name = "NovaTech Industries"
    year = 2024
    ceo_name = "Sarah Chen"
    cfo_name = "Michael Rodriguez"
    employees = 2847
    revenue = "$342.7M"
    profit = "$67.4M"
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    story.append(Paragraph(f"{company_name}", title_style))
    story.append(Paragraph(f"Annual Report {year}", styles['Heading2']))
    story.append(Spacer(1, 0.5*inch))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", styles['Heading2']))
    exec_summary = f"""
    {company_name} completed another successful year in {year}, achieving record revenue of {revenue} 
    and net profit of {profit}. Under the leadership of CEO {ceo_name}, the company expanded its 
    workforce to {employees} employees and launched three new product lines: CloudSync Pro, 
    DataMesh Analytics, and SecureVault Enterprise.
    """
    story.append(Paragraph(exec_summary, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Financial Highlights Table
    story.append(Paragraph("Financial Highlights", styles['Heading2']))
    financial_data = [
        ['Metric', 'Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024'],
        ['Revenue', '$78.2M', '$84.5M', '$89.3M', '$90.7M'],
        ['Operating Income', '$15.1M', '$16.8M', '$17.2M', '$18.3M'],
        ['Net Income', '$14.2M', '$16.1M', '$17.8M', '$19.3M'],
    ]
    
    table = Table(financial_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table)
    story.append(Spacer(1, 0.3*inch))
    
    # Product Performance
    story.append(Paragraph("Product Performance", styles['Heading2']))
    products_text = f"""
    Our flagship product, CloudSync Pro, achieved 127% year-over-year growth with 45,000 active users. 
    The newly launched DataMesh Analytics platform secured partnerships with 12 Fortune 500 companies 
    in its first quarter. SecureVault Enterprise, targeting the financial services sector, reached 
    $23.4M in annual recurring revenue.
    """
    story.append(Paragraph(products_text, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Leadership Team
    story.append(Paragraph("Leadership Team", styles['Heading2']))
    leadership_text = f"""
    CEO: {ceo_name} - Leading the company since 2019, Sarah has 20 years of experience in enterprise software.
    <br/><br/>
    CFO: {cfo_name} - Michael joined {company_name} in 2022 from TechVentures Capital where he was a Managing Partner.
    <br/><br/>
    CTO: Dr. Amanda Foster - Amanda holds a PhD in Distributed Systems from MIT and previously led engineering at DataCore.
    <br/><br/>
    VP of Sales: James Wu - James expanded our sales team to 127 representatives across North America and Europe.
    """
    story.append(Paragraph(leadership_text, styles['BodyText']))
    
    # Build PDF
    doc.build(story)
    print(f"Generated: {filename}")

def generate_research_paper(filename="test_research_paper.pdf"):
    """Generate a fictional research paper"""
    
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Paper details (completely fictional)
    title = "Quantum-Resistant Lattice Structures in Post-Cryptographic Systems"
    authors = "Dr. Elena Vasquez, Prof. Raj Patel, Dr. Kim Nakamura"
    institution = "Institute for Advanced Computational Security"
    date = "September 2024"
    
    # Title and authors
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=18, spaceAfter=12, alignment=1)
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(authors, styles['Normal']))
    story.append(Paragraph(institution, styles['Normal']))
    story.append(Paragraph(date, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Abstract
    story.append(Paragraph("Abstract", styles['Heading2']))
    abstract = """
    We present a novel approach to constructing quantum-resistant cryptographic systems using
    modified Learning With Errors (LWE) lattice structures. Our algorithm, dubbed QLATTICE-47,
    demonstrates a 34% improvement in key generation speed while maintaining 256-bit security equivalence.
    Experimental results show that QLATTICE-47 resists known quantum attacks including Shor's algorithm
    variants and maintains computational complexity of O(n log n) for key operations. Performance benchmarks
    on standard hardware show encryption throughput of 2.3 GB/s and decryption at 1.8 GB/s.
    """
    story.append(Paragraph(abstract, styles['BodyText']))
    story.append(Spacer(1, 0.3*inch))
    
    # Introduction
    story.append(Paragraph("1. Introduction", styles['Heading2']))
    intro = """
    The emergence of quantum computing poses significant threats to current cryptographic infrastructure. 
    Traditional RSA and ECC systems are vulnerable to quantum attacks, necessitating the development of 
    post-quantum cryptographic (PQC) solutions. Our research builds upon the foundational work of 
    Regev (2005) and Peikert (2016) in lattice-based cryptography.
    """
    story.append(Paragraph(intro, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Methodology
    story.append(Paragraph("2. Methodology", styles['Heading2']))
    methodology = """
    We implemented QLATTICE-47 using a modified Ring-LWE structure with parameters n=1024, q=12289, 
    and error distribution σ=3.2. The system utilizes a hybrid approach combining lattice reduction 
    with polynomial sampling techniques. Our test environment consisted of Intel Xeon Platinum 8380 
    processors with 256GB RAM running Ubuntu 22.04 LTS.
    """
    story.append(Paragraph(methodology, styles['BodyText']))
    story.append(Spacer(1, 0.2*inch))
    
    # Results table
    story.append(Paragraph("3. Results", styles['Heading2']))
    results_data = [
        ['Algorithm', 'Key Gen (ms)', 'Encrypt (ms)', 'Decrypt (ms)', 'Security Level'],
        ['RSA-2048', '145', '0.8', '12', '112-bit'],
        ['CRYSTALS-Kyber', '32', '8.2', '9.1', '128-bit'],
        ['QLATTICE-47', '21', '5.4', '6.7', '256-bit'],
    ]
    
    table = Table(results_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(table)
    
    doc.build(story)
    print(f"Generated: {filename}")

def generate_test_suite():
    """Generate multiple test PDFs with ground truth Q&A"""

    # Create Test_Data directory if it doesn't exist
    test_data_dir = "Test_Data"
    os.makedirs(test_data_dir, exist_ok=True)
    print(f"Created directory: {test_data_dir}\n")

    print("Generating RAG Test PDFs...\n")

    # Generate PDFs in Test_Data directory
    generate_company_report(os.path.join(test_data_dir, "novatech_report.pdf"))
    generate_research_paper(os.path.join(test_data_dir, "quantum_lattice_paper.pdf"))
    
    # Create ground truth Q&A file
    qa_pairs = """
# Ground Truth Q&A for RAG Testing

## NovaTech Industries Report (novatech_report.pdf)

### Simple Fact Retrieval
Q: What was NovaTech's total revenue in 2024?
A: $342.7M

Q: Who is the CEO of NovaTech Industries?
A: Sarah Chen

Q: How many employees does NovaTech have?
A: 2,847 employees

Q: What was Q3 2024 revenue?
A: $89.3M

Q: Who is the CFO?
A: Michael Rodriguez

Q: What was NovaTech's net profit in 2024?
A: $67.4M

### Multi-hop Reasoning
Q: What is the difference between Q4 and Q1 revenue?
A: $12.5M ($90.7M - $78.2M)

Q: Which product line targets financial services?
A: SecureVault Enterprise

Q: What was the total operating income across all quarters in 2024?
A: $67.4M ($15.1M + $16.8M + $17.2M + $18.3M)

### Product-Specific
Q: How many active users does CloudSync Pro have?
A: 45,000 active users

Q: What is the annual recurring revenue of SecureVault Enterprise?
A: $23.4M

Q: How many Fortune 500 partnerships did DataMesh Analytics secure?
A: 12 partnerships

Q: What was the year-over-year growth rate for CloudSync Pro?
A: 127%

### Leadership Information
Q: Who is the CTO of NovaTech Industries?
A: Dr. Amanda Foster

Q: Who is the VP of Sales?
A: James Wu

Q: How many sales representatives does NovaTech have?
A: 127 representatives

### Negative Tests (Should say "not found" or similar)
Q: What is NovaTech's investment in blockchain technology?
A: This information is not mentioned in the document

Q: Who is the VP of Marketing?
A: This information is not mentioned in the document

---

## Quantum Lattice Paper (quantum_lattice_paper.pdf)

### Simple Fact Retrieval
Q: What is the name of the proposed algorithm?
A: QLATTICE-47

Q: What is the encryption throughput of QLATTICE-47?
A: 2.3 GB/s

Q: What is the decryption throughput of QLATTICE-47?
A: 1.8 GB/s

Q: What security level does QLATTICE-47 provide?
A: 256-bit security equivalence

Q: What is the value of parameter n in QLATTICE-47?
A: n=1024

Q: What is the value of parameter q in QLATTICE-47?
A: q=12289

Q: What is the error distribution parameter sigma?
A: σ=3.2

### Numerical/Performance
Q: What is the key generation time for QLATTICE-47?
A: 21 ms

Q: How much faster is QLATTICE-47 key generation compared to RSA-2048?
A: About 7x faster (145ms vs 21ms)

Q: What is the computational complexity of QLATTICE-47 key operations?
A: O(n log n)

Q: What is the encryption time for QLATTICE-47?
A: 5.4 ms

Q: What improvement in key generation speed does QLATTICE-47 demonstrate?
A: 34% improvement

### Technical Details
Q: What lattice structure does QLATTICE-47 use?
A: Modified Ring-LWE structure

Q: What hardware was used for testing QLATTICE-47?
A: Intel Xeon Platinum 8380 processors with 256GB RAM

Q: What operating system was used in the test environment?
A: Ubuntu 22.04 LTS

### Author Information
Q: Who are the authors of this paper?
A: Dr. Elena Vasquez, Prof. Raj Patel, Dr. Kim Nakamura

Q: What institution are the authors from?
A: Institute for Advanced Computational Security

Q: When was the paper published?
A: September 2024

### Negative Tests
Q: What quantum attacks can break QLATTICE-47?
A: The paper states it resists known quantum attacks; specific attacks that can break it are not mentioned

Q: What is the decryption time for RSA-2048?
A: This information is provided in the table (12ms) but not for comparison purposes in the text

---

## Advanced RAG Testing (Cross-Document, Paraphrasing, Edge Cases)

### Cross-Document Questions
Q: Compare the number of employees at NovaTech with the number of authors on the QLATTICE-47 paper
A: NovaTech has 2,847 employees while the QLATTICE-47 paper has 3 authors

Q: Which document was published more recently, the NovaTech annual report or the quantum lattice paper?
A: Both are from 2024. The quantum lattice paper specifies September 2024, while the annual report covers the full year 2024

Q: Is there any connection between NovaTech's products and the QLATTICE-47 algorithm?
A: NovaTech has a product called SecureVault Enterprise targeting financial services, while QLATTICE-47 is a quantum-resistant cryptographic system. Both relate to security, but no direct connection is mentioned

Q: Which document contains more numerical performance metrics?
A: The quantum lattice paper contains more performance metrics (encryption/decryption times, throughput, complexity) compared to the NovaTech report

### Paraphrased Questions (Semantic Understanding)
Q: How much money did NovaTech make in total during 2024?
A: $342.7M (paraphrase of "What was NovaTech's total revenue in 2024?")

Q: What's the name of the person running NovaTech as CEO?
A: Sarah Chen (paraphrase of "Who is the CEO of NovaTech Industries?")

Q: How fast can QLATTICE-47 encrypt data?
A: 2.3 GB/s (paraphrase of "What is the encryption throughput of QLATTICE-47?")

Q: What's the title of the algorithm presented in the research paper?
A: QLATTICE-47 (paraphrase of "What is the name of the proposed algorithm?")

Q: How long does it take QLATTICE-47 to generate keys?
A: 21 ms (paraphrase of "What is the key generation time for QLATTICE-47?")

### List/Aggregation Questions
Q: List all three product lines launched by NovaTech in 2024
A: CloudSync Pro, DataMesh Analytics, and SecureVault Enterprise

Q: What are the names of all the leadership positions mentioned in the NovaTech report?
A: CEO (Sarah Chen), CFO (Michael Rodriguez), CTO (Dr. Amanda Foster), and VP of Sales (James Wu)

Q: List all the algorithms compared in the quantum lattice paper's results table
A: RSA-2048, CRYSTALS-Kyber, and QLATTICE-47

Q: What are all the parameters specified for QLATTICE-47?
A: n=1024, q=12289, and σ=3.2

### Ambiguous Questions (Tests Clarification Handling)
Q: What was the revenue?
A: This question is ambiguous. NovaTech had total revenue of $342.7M in 2024, with quarterly revenues ranging from $78.2M (Q1) to $90.7M (Q4). Please specify which quarter or if you want the total

Q: Who is the doctor?
A: There are two doctors mentioned: Dr. Amanda Foster (CTO of NovaTech) and Dr. Elena Vasquez (author of the quantum lattice paper). Please specify which one

Q: What is the encryption time?
A: QLATTICE-47 has an encryption time of 5.4 ms. If you're asking about other algorithms, RSA-2048 is 0.8 ms and CRYSTALS-Kyber is 8.2 ms

### Hallucination Trap Questions
Q: What was NovaTech's Q5 2024 revenue?
A: There is no Q5 (fifth quarter). The report only covers Q1 through Q4 of 2024

Q: What is QLATTICE-48?
A: QLATTICE-48 is not mentioned in the documents. The algorithm discussed is QLATTICE-47

Q: How many employees does the quantum research institute have?
A: The number of employees at the Institute for Advanced Computational Security is not mentioned in the paper

Q: What was the revenue of QLATTICE-47?
A: QLATTICE-47 is a cryptographic algorithm, not a company or product with revenue. You may be confusing it with NovaTech's products

Q: Who is the CEO of the Institute for Advanced Computational Security?
A: The CEO or leadership of the Institute for Advanced Computational Security is not mentioned in the paper

Q: What programming language was QLATTICE-47 implemented in?
A: The programming language used for QLATTICE-47 implementation is not mentioned in the paper

### Conversational Follow-up Questions (Multi-turn Context)
Q: Who is the CEO of NovaTech?
A: Sarah Chen

Q: How long has she been in that role?
A: Since 2019 (requires understanding "she" refers to Sarah Chen from previous question)

Q: What about the CFO?
A: Michael Rodriguez is the CFO. He joined NovaTech in 2022 from TechVentures Capital (requires understanding we're still talking about NovaTech)

### Temporal/Comparative Questions
Q: Which quarter had the highest revenue for NovaTech?
A: Q4 2024 with $90.7M

Q: How did NovaTech's revenue trend throughout 2024?
A: Revenue showed consistent growth each quarter: Q1 ($78.2M), Q2 ($84.5M), Q3 ($89.3M), Q4 ($90.7M)

Q: Which algorithm has the fastest key generation time?
A: QLATTICE-47 with 21 ms, followed by CRYSTALS-Kyber (32 ms) and RSA-2048 (145 ms)

### Edge Cases
Q: What was the revenue in Q1, Q2, Q3, and Q4 of 2024 for NovaTech Industries?
A: Q1: $78.2M, Q2: $84.5M, Q3: $89.3M, Q4: $90.7M (tests handling of long, multi-part questions)

Q: QLATTICE-47 key gen time?
A: 21 ms (tests handling of abbreviated/informal questions)

Q: What is the total sum of all quarterly revenues for NovaTech in 2024?
A: $342.7M (Q1 $78.2M + Q2 $84.5M + Q3 $89.3M + Q4 $90.7M = $342.7M)
"""
    
    with open(os.path.join(test_data_dir, "ground_truth_qa.txt"), "w", encoding="utf-8") as f:
        f.write(qa_pairs)

    print(f"\nGenerated {os.path.join(test_data_dir, 'ground_truth_qa.txt')} with test questions and answers")
    print(f"\n[SUCCESS] Test suite ready in '{test_data_dir}' directory! Use these PDFs to verify your RAG system retrieves correctly.")

if __name__ == "__main__":
    generate_test_suite()