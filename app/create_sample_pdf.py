from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Create a PDF file in the data folder
c = canvas.Canvas("data/sample_notes.pdf", pagesize=letter)

# Page 1 - Operating Systems
c.setFont("Helvetica-Bold", 16)
c.drawString(100, 750, "Operating Systems - B.Tech Notes")

c.setFont("Helvetica", 12)
c.drawString(100, 700, "CPU Scheduling:")
c.drawString(100, 680, "CPU scheduling decides which process runs next on the processor.")
c.drawString(100, 660, "Common algorithms: Round Robin, FCFS, SJF, Priority Scheduling.")
c.drawString(100, 640, "Round Robin gives equal time slots called quantum to each process.")

c.drawString(100, 600, "Deadlock:")
c.drawString(100, 580, "Deadlock is a situation where two or more processes wait forever.")
c.drawString(100, 560, "Each process holds a resource and waits for another held by others.")
c.drawString(100, 540, "Four conditions for deadlock: Mutual Exclusion, Hold and Wait,")
c.drawString(100, 520, "No Preemption, Circular Wait.")

# Page 2 - DBMS
c.showPage()
c.setFont("Helvetica-Bold", 16)
c.drawString(100, 750, "Database Management Systems - B.Tech Notes")

c.setFont("Helvetica", 12)
c.drawString(100, 700, "Normalization:")
c.drawString(100, 680, "Normalization organizes database to reduce redundancy.")
c.drawString(100, 660, "1NF: Each column has atomic values, no repeating groups.")
c.drawString(100, 640, "2NF: No partial dependency on primary key.")
c.drawString(100, 620, "3NF: No transitive dependency.")

c.drawString(100, 580, "Transactions:")
c.drawString(100, 560, "A transaction is a unit of work that must complete fully or not at all.")
c.drawString(100, 540, "ACID properties: Atomicity, Consistency, Isolation, Durability.")

c.save()
print("PDF created at data/sample_notes.pdf")
