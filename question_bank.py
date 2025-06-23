import customtkinter as ctk

class QuestionBank:
    def __init__(self):
        self.questions = {}
        self.topic = {}
        self.difficulty = {}

    def add_question(self, question_id, question_text, topic, difficulty):
        if question_id in self.questions:
            raise ValueError(f"Question ID {question_id} already exists.")
        self.questions[question_id] = {
            "text": question_text,
            "topic": topic,
            "difficulty": difficulty
        }
        if topic not in self.topic:
            self.topic[topic] = []
        self.topic[topic].append(question_id)
        if difficulty not in self.difficulty:
            self.difficulty[difficulty] = []
        self.difficulty[difficulty].append(question_id)

    def search_questions(self, topic=None, difficulty=None):
        results = []
        for question_id, question in self.questions.items():
            if (topic is None or question["topic"] == topic) and \
               (difficulty is None or question["difficulty"] == difficulty):
                results.append((question_id, question["text"]))
        return results

    def delete_question(self, question_id):
        if question_id not in self.questions:
            raise ValueError(f"Question ID {question_id} does not exist.")
        question = self.questions.pop(question_id)
        self.topic[question["topic"]].remove(question_id)
        self.difficulty[question["difficulty"]].remove(question_id)
        if not self.topic[question["topic"]]:
            del self.topic[question["topic"]]
        if not self.difficulty[question["difficulty"]]:
            del self.difficulty[question["difficulty"]]
        return f"Question {question_id} removed: {question['text']}"

# --- GUI PART ---
qb = QuestionBank()

def add_question():
    try:
        qid = int(entry_id.get())
        text = entry_text.get()
        topic = entry_topic.get()
        diff = entry_diff.get()
        qb.add_question(qid, text, topic, diff)
        output.configure(text=f"Added question {qid}")
    except Exception as e:
        output.configure(text=str(e))

def search_questions():
    topic = entry_topic.get() or None
    diff = entry_diff.get() or None
    results = qb.search_questions(topic, diff)
    if results:
        output.configure(text="\n".join([f"{qid}: {txt}" for qid, txt in results]))
    else:
        output.configure(text="No results found.")

def delete_question():
    try:
        qid = int(entry_id.get())
        msg = qb.delete_question(qid)
        output.configure(text=msg)
    except Exception as e:
        output.configure(text=str(e))

ctk.set_appearance_mode("light")
root = ctk.CTk()
root.title("Question Bank")

entry_id = ctk.CTkEntry(root, placeholder_text="Question ID")
entry_id.pack(padx=10, pady=5)
entry_text = ctk.CTkEntry(root, placeholder_text="Question Text")
entry_text.pack(padx=10, pady=5)
entry_topic = ctk.CTkEntry(root, placeholder_text="Topic")
entry_topic.pack(padx=10, pady=5)
entry_diff = ctk.CTkEntry(root, placeholder_text="Difficulty")
entry_diff.pack(padx=10, pady=5)

btn_add = ctk.CTkButton(root, text="Add Question", command=add_question)
btn_add.pack(padx=10, pady=5)
btn_search = ctk.CTkButton(root, text="Search Questions", command=search_questions)
btn_search.pack(padx=10, pady=5)
btn_delete = ctk.CTkButton(root, text="Delete Question", command=delete_question)
btn_delete.pack(padx=10, pady=5)

output = ctk.CTkLabel(root, text="", wraplength=400, justify="left")
output.pack(padx=10, pady=10)

root.mainloop()
