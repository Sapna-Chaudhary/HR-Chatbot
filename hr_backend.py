#imports
import pandas as pd
from docx import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama

print("Setup successful")

#llm
def get_llm():
    return ChatOllama(
        model="qwen2.5:1.5b"
    )

#Excel_file
excel_file = "data/HR_Data.xlsx"

employee_df = pd.read_excel(
    excel_file,
    sheet_name="Employee_Master_Data"
)

attendance_df = pd.read_excel(
    excel_file,
    sheet_name="Attendance"
)

timesheet_df = pd.read_excel(
    excel_file,
    sheet_name="Timesheet"
)

leave_df = pd.read_excel(
    excel_file,
    sheet_name="Leave_Tracker"
)
# Memory
last_employee = None

#Docx
from docx import Document
doc = Document("data/Employee_Handbook.docx")
text = ""
for para in doc.paragraphs:
    text += para.text + "\n"
    
from langchain_core.documents import Document as LangDocument

documents = [
    LangDocument(page_content=text)
]

#chunking
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(documents)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

#vectorstore
vectorstore = FAISS.load_local(
    "faiss_index",
    embeddings,
    allow_dangerous_deserialization=True
)

#handbook_query
def handbook_query(question):

    docs = vectorstore.similarity_search(
        question,
        k=3
    )

    context = "\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are an HR assistant for a startup.

Answer ONLY from the provided context.
If the answer is not present in the context, say:
"I could not find that information in the HR handbook."

HR Handbook Context:
{context}

Question:
{question}
"""

    llm = get_llm()

    response = llm.invoke(prompt)

    return response.content

#get_manager
def get_manager(employee_name):
    result = employee_df[
        employee_df["name"].str.lower() == employee_name.lower()
    ]

    if result.empty:
        return "Employee not found."

    return f"{employee_name}'s manager is {result.iloc[0]['manager']}."

#get_employee_details
def get_employee_details(employee_name, query):

    result = employee_df[
        employee_df["name"].str.lower() == employee_name.lower()
    ]

    if result.empty:
        return "Employee not found."

    row = result.iloc[0]


    if "department" in query or "dept" in query:
        return f"{employee_name}'s department is {row['department']}."


    elif "joining" in query or "join date" in query or "joining_date" in query:
        return f"{employee_name} joined on {row['joining_date']}."


    return "Information not available."

#get_leave_info
def get_leave_info(employee_name, query):

    employee = leave_df[
        leave_df["Name"].str.lower() == employee_name.lower()
    ]

    if employee.empty:
        return "Employee not found."

    row = employee.iloc[0]


    # Specific CL used
    if "cl" in query and any(word in query for word in ["used", "taken", "utilized", "consumed"]):
        return f"{employee_name}'s CL used count is {row['CL Taken']} days."


    # Specific EL used
    elif "el" in query and any(word in query for word in ["used", "taken", "utilized", "consumed"]):
        return f"{employee_name}'s EL used count is {row['EL Taken']} days."


    # Specific SL used
    elif "sl" in query and any(word in query for word in ["used", "taken", "utilized", "consumed"]):
        return f"{employee_name}'s SL used count is {row['SL Taken']} days."


    # Total used leaves
    elif any(word in query for word in ["used", "taken", "utilized", "consumed"]):
        return f"{employee_name} has used {row['Total Taken']} total leaves."


    # Specific CL balance
    elif "cl" in query and any(word in query for word in ["balance", "left", "remaining"]):
        return f"{employee_name}'s CL balance is {row['CL Balance']} days."


    # Specific EL balance
    elif "el" in query and any(word in query for word in ["balance", "left", "remaining"]):
        return f"{employee_name}'s EL balance is {row['EL Balance']} days."


    # Specific SL balance
    elif "sl" in query and any(word in query for word in ["balance", "left", "remaining"]):
        return f"{employee_name}'s SL balance is {row['SL Balance']} days."


    # Complete leave details
    else:
        return f"""
{employee_name}'s Leave Details:

CL Taken: {row['CL Taken']}
EL Taken: {row['EL Taken']}
SL Taken: {row['SL Taken']}

CL Balance: {row['CL Balance']}
EL Balance: {row['EL Balance']}
SL Balance: {row['SL Balance']}

Total Taken: {row['Total Taken']}
Total Balance: {row['Total Balance']}
"""

#get_attendance
def get_attendance(employee_name):
    result = attendance_df[
        attendance_df["Name"].str.lower() == employee_name.lower()
    ]

    if result.empty:
        return "Employee not found."

    row = result.iloc[0]

    return f"""
Attendance Percentage: {row['Attendance %']}%
Present Days: {row['Present']}
Paid Leave: {row['Paid Leave']}
Absent Days: {row['Absent (LOP)']}
"""

#get_attendance_details
def get_attendance_details(employee_name, query):

    result = attendance_df[
        attendance_df["Name"].str.lower() == employee_name.lower()
    ]

    if result.empty:
        return "Employee not found."

    row = result.iloc[0]

    absent_days = []
    leave_days = []
    present_days = []
    weekoff_days = []

    for day in range(1, 31):

        status = str(row[str(day)]).strip().upper()

        if status == "A":
            absent_days.append(day)

        elif status == "L":
            leave_days.append(day)

        elif status == "P":
            present_days.append(day)

        elif status == "WO":
            weekoff_days.append(day)


    # Specific absent days
    if "absent" in query or "absence" in query:
        return f"{employee_name} was absent on days: {absent_days}"


    # Specific leave days
    elif "leave" in query:
        return f"{employee_name} was on leave on days: {leave_days}"


    # Specific week off
    elif "week off" in query or "weekoff" in query or "wo" in query:
        return f"{employee_name}'s week off days are: {weekoff_days}"


    # Complete attendance details
    else:
        return f"""
{employee_name}'s Attendance Details:

Present Days: {len(present_days)}
Absent Days: {len(absent_days)}
Leave Days: {len(leave_days)}
Week Off Days: {len(weekoff_days)}

Absent on: {absent_days}
Leave on: {leave_days}
Week Off on: {weekoff_days}
"""

#get_attendance_summary
def get_attendance_summary(employee_name, query):

    result = attendance_df[
        attendance_df["Name"].str.lower() == employee_name.lower()
    ]

    if result.empty:
        return "Employee not found."

    row = result.iloc[0]


    if "payable" in query:
        return f"{employee_name}'s payable days are {row['Payable Days']}."


    elif "attendance" in query or "attendance %" in query:
        return f"{employee_name}'s attendance percentage is {row['Attendance %']}%."


    return "Attendance information not available."

#hr_bot
def hr_bot(question):

    global last_employee

    q = question.lower().strip()

    employee_name = None

    # Find employee name in the question
    for name in employee_df["name"]:
        if name.lower() in q:
            employee_name = name
            last_employee = name
            break

    # If user uses pronouns, use previous employee
    if employee_name is None:
        if any(word in q for word in [
            "he",
            "she",
            "his",
            "her"
        ]):
            employee_name = last_employee

    # Greetings
    if q in ["hi", "hello", "hey","Hello","Hi","Hey","Hi!"]:
        return "Hello! How can I help you with HR queries?"

    if q in ["nice","amazing","nice work","perfect"]:
        return "Thank you! How can I help you further?"

    if q in ["thanks", "thank you","ok thanks", "ok thanks!","Thank You","Thank you","Ok thank you!","ok thank you","thanks buddy","thanks dear"]:
        return "You're welcome! How can I help you with HR queries."

    # Manager query
    if "manager" in q:

        for name in employee_df["name"]:
            if name.lower() in q:
                return get_manager(name)

    # Leave query
    if any(word in q for word in [
        "cl",
        "cl+el+sl",
        "cl,el,sl",
        "el",
        "sl",
        "leave",
        "balance",
        "used",
        "taken",
        "utilized",
        "consumed",
        "remaining",
        "left"
    ]):

        for name in leave_df["Name"]:
            if name.lower() in q:
                return get_leave_info(name, q)

    # Employee details query
    if any(word in q for word in [
        "department",
        "dept",
        "joining",
        "join date"
    ]):

        for name in employee_df["name"]:
            if name.lower() in q:
                return get_employee_details(name, q)

    # Attendance summary query (KEEP THIS BEFORE ATTENDANCE DETAILS)
    if any(word in q for word in [
        "payable",
        "attendance %",
        "attendance percentage",
        "percentage"
    ]):

        for name in attendance_df["Name"]:
            if name.lower() in q:
                return get_attendance_summary(name, q)

    # Attendance details query
    if any(word in q for word in [
        "attendance",
        "present",
        "absent",
        "absence",
        "lop",
        "week off",
        "weekoff",
        "wo"
    ]):

        for name in attendance_df["Name"]:
            if name.lower() in q:
                return get_attendance_details(name, q)

    # HR Handbook (RAG)
    return handbook_query(question)




