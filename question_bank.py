import customtkinter as ctk

next_id = 1


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
            "difficulty": difficulty,
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
            if (topic is None or question["topic"] == topic) and (
                difficulty is None or question["difficulty"] == difficulty
            ):
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


qb = QuestionBank()


def update_next_id():
    global next_id
    entry_id.configure(state="normal")
    entry_id.delete(0, "end")
    entry_id.insert(0, str(next_id))
    entry_id.configure(state="readonly")


def add_question():
    global next_id
    try:
        qid = int(entry_id.get())
        text = entry_text.get()
        topic = entry_topic.get()
        diff = entry_diff.get()
        qb.add_question(qid, text, topic, diff)
        output.configure(text=f"Added question {qid}")
        next_id += 1
        update_next_id()
        update_topic_dropdown()
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
    global next_id
    try:
        qid = int(entry_id.get())
        msg = qb.delete_question(qid)
        output.configure(text=msg)
        if qb.questions:
            max_id = max(qb.questions.keys())
            next_id = max_id + 1
        else:
            next_id = 1
        update_next_id()
        update_topic_dropdown()
    except Exception as e:
        output.configure(text=str(e))


def update_topic_dropdown():
    topics = list(qb.topic.keys())
    entry_topic.configure(values=topics)


def open_cycle_window():
    cycle_win = ctk.CTkToplevel(root)
    cycle_win.title("Cycle Through Questions")
    cycle_win.geometry("500x300")

    questions = list(qb.questions.items())
    if not questions:
        msg = ctk.CTkLabel(cycle_win, text="No questions available.")
        msg.pack(pady=20)
        return

    idx = [0]

    def show_question():
        qid, q = questions[idx[0]]
        question_label.configure(
            text=f"ID: {qid}\nTopic: {q['topic']}\nDifficulty: {q['difficulty']}\n\n{q['text']}"
        )

    def next_question():
        idx[0] = (idx[0] + 1) % len(questions)
        show_question()

    def prev_question():
        idx[0] = (idx[0] - 1) % len(questions)
        show_question()

    question_label = ctk.CTkLabel(cycle_win, text="", wraplength=450, justify="left")
    question_label.pack(pady=20)

    btn_prev = ctk.CTkButton(cycle_win, text="Previous", command=prev_question)
    btn_prev.pack(side="left", padx=40, pady=10)
    btn_next = ctk.CTkButton(cycle_win, text="Next", command=next_question)
    btn_next.pack(side="right", padx=40, pady=10)

    show_question()


ctk.set_appearance_mode("light")
root = ctk.CTk()
root.title("Question Bank")
root.geometry("600x600")  # Window size

entry_id = ctk.CTkEntry(root, placeholder_text="Question ID", width=400, height=40)
entry_id.pack(padx=20, pady=10)
entry_text = ctk.CTkEntry(root, placeholder_text="Question Text", width=400, height=40)
entry_text.pack(padx=20, pady=10)
entry_topic = ctk.CTkComboBox(root, values=["Categories"], width=400, height=40)
entry_topic.pack(padx=20, pady=10)
entry_diff = ctk.CTkComboBox(
    root, values=["Easy", "Medium", "Hard"], width=400, height=40
)
entry_diff.pack(padx=20, pady=10)

update_next_id()
update_topic_dropdown()

btn_add = ctk.CTkButton(
    root, text="Add Question", command=add_question, width=200, height=40
)
btn_add.pack(padx=20, pady=10)
btn_search = ctk.CTkButton(
    root, text="Search Questions", command=search_questions, width=200, height=40
)
btn_search.pack(padx=20, pady=10)
btn_delete = ctk.CTkButton(
    root, text="Delete Question", command=delete_question, width=200, height=40
)
btn_delete.pack(padx=20, pady=10)
btn_cycle = ctk.CTkButton(
    root, text="Cycle Questions", command=open_cycle_window, width=200, height=40
)
btn_cycle.pack(padx=20, pady=10)

output = ctk.CTkLabel(
    root, text="", wraplength=500, justify="left", width=500, height=100
)
output.pack(padx=20, pady=20)

root.mainloop()
