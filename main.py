import os
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from test import data

paper_name = ""
select_window = tk.Tk()
select_window.title("Select Paper")
select_window.config(padx=50, background="white", highlightthickness=0)


def resize_image(image, max_width, max_height):
    width, height = image.size
    aspect_ratio = width / height

    # Calculate new dimensions to maintain aspect ratio
    if width > max_width or height > max_height:
        if aspect_ratio > 1:  # Image is wider
            new_width = max_width
            new_height = int(max_width / aspect_ratio)
            if new_height > max_height:
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
        else:  # Image is taller
            new_height = max_height
            new_width = int(max_height * aspect_ratio)
            if new_width > max_width:
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
    else:
        new_width, new_height = width, height

    return image.resize((new_width, new_height), Image.LANCZOS)


def display_question():
    global num, is_paused
    if is_paused:
        canvas.config(background="white")  # Hide the question when paused
        return

    canvas.config(background="white")  # Set canvas background to white
    canvas.delete("all")

    if 0 <= num < len(questions_data):
        question_image = questions_data[num]["question"]

        # Resize the image to fit the canvas while maintaining aspect ratio
        resized_image = resize_image(question_image, 800, 500)
        photo_image = ImageTk.PhotoImage(resized_image)

        # Display the image centered
        canvas.create_image(400, 250, anchor=CENTER, image=photo_image)
        canvas.image = photo_image  # Keep a reference to avoid garbage collection

        # Highlight selected answer
        if user_answers[num] == "A":
            a_button.config(bg="yellow")
            b_button.config(bg="SystemButtonFace")
            c_button.config(bg="SystemButtonFace")
            d_button.config(bg="SystemButtonFace")
        elif user_answers[num] == "B":
            a_button.config(bg="SystemButtonFace")
            b_button.config(bg="yellow")
            c_button.config(bg="SystemButtonFace")
            d_button.config(bg="SystemButtonFace")
        elif user_answers[num] == "C":
            a_button.config(bg="SystemButtonFace")
            b_button.config(bg="SystemButtonFace")
            c_button.config(bg="yellow")
            d_button.config(bg="SystemButtonFace")
        elif user_answers[num] == "D":
            a_button.config(bg="SystemButtonFace")
            b_button.config(bg="SystemButtonFace")
            c_button.config(bg="SystemButtonFace")
            d_button.config(bg="yellow")
        else:
            a_button.config(bg="SystemButtonFace")
            b_button.config(bg="SystemButtonFace")
            c_button.config(bg="SystemButtonFace")
            d_button.config(bg="SystemButtonFace")


def load_images():
    global questions_data
    questions_data = []

    for file_name in sorted(os.listdir(image_directory), key=lambda x: int(x.split('.')[0])):
        if file_name.endswith('.png'):
            image_path = os.path.join(image_directory, file_name)
            image = Image.open(image_path)
            questions_data.append({"question": image})


def record_answer(answer):
    global num
    user_answers[num] = answer
    display_question()  # Update the button colors


def navigate(direction):
    global num
    num += direction
    if num < 0:
        num = 0
    elif num >= len(questions_data):
        num = len(questions_data) - 1
    display_question()


def finish_quiz():
    global user_answers, correct_answers, score

    # Calculate the score
    for user_answer, correct_answer in zip(user_answers, correct_answers):
        if user_answer == correct_answer:
            score += 1

    result_text = f"You finished the quiz!\nYour score is: {score}/{len(correct_answers)}"
    canvas.delete("all")
    canvas.create_text(400, 250, text=result_text, font=("Ariel", 30, "bold"), fill=TEXT_COLOR)

    # Disable buttons
    a_button.config(state="disabled")
    b_button.config(state="disabled")
    c_button.config(state="disabled")
    d_button.config(state="disabled")

    finish_button.config(state="disabled")
    pause_button.config(state="disabled")

    # Stop the timer
    stop_countdown()
    i = 1
    for ans in correct_answers:
        print(f"{i} {ans}")
        i += 1
    print("OVER")


def update_timer():
    global quiz_duration, timer_id, is_paused

    if not is_paused:
        minutes, seconds = divmod(quiz_duration, 60)
        timer_label.config(text=f"{minutes:02}:{seconds:02}")
        quiz_duration -= 1

        if quiz_duration >= 0:
            timer_id = window.after(1000, update_timer)
        else:
            finish_quiz()


def pause_quiz():
    global is_paused
    if is_paused:
        is_paused = False

        pause_button.config(image=pause_image)
        update_timer()
        display_question()  # Re-display the question when resumed
    else:
        is_paused = True
        pause_button.config(image=resume_image)
        stop_countdown()
        canvas.delete("all")  # Hide the question when paused


def stop_countdown():
    global timer_id
    if timer_id is not None:
        window.after_cancel(timer_id)
        timer_id = None


def leave_now(paper):
    global paper_name
    paper_name = paper
    select_window.destroy()


def select_quiz():
    physics_label = Label(text="Physics", font=("Ariel", 20, "bold"), padx=20, pady=20, background="white")
    chemistry_label = Label(text="Chemistry", font=("Ariel", 20, "bold"), padx=20, pady=20, background="white")
    physics_label.grid(row=2, column=1)
    chemistry_label.grid(row=2, column=0)

    logo_image = PhotoImage(file="buttons/Quiz.png")
    logo = Label(image=logo_image)
    logo.grid(row=0, column=0, columnspan=2)
    b1 = tk.Button(select_window, text="October 2023 p12", command=lambda: leave_now("9701_w23_qp_12"), width=20)
    b1.grid(row=3, column=0)

    b2 = tk.Button(select_window, text="May 2023 p12", command=lambda: leave_now("9701_s23_qp_12"), width=20)
    b2.grid(row=4, column=0)

    b3 = tk.Button(select_window, text="March 2023 p12", command=lambda: leave_now("9701_m23_qp_12"), width=20)
    b3.grid(row=5, column=0)

    b4 = tk.Button(select_window, text="October 2022 p12", command=lambda: leave_now("9701_w23_qp_12"), width=20)
    b4.grid(row=6, column=0)

    b5 = tk.Button(select_window, text="May 2022 p12", command=lambda: leave_now("9701_s22_qp_12"), width=20)
    b5.grid(row=7, column=0)

    b6 = tk.Button(select_window, text="March 2022 p12", command=lambda: leave_now("9701_m22_qp_12"), width=20)
    b6.grid(row=8, column=0)

    b7 = tk.Button(select_window, text="October 2021 p12", command=lambda: leave_now("9701_w21_qp_12"), width=20)
    b7.grid(row=9, column=0)

    b8 = tk.Button(select_window, text="May 2021 p12", command=lambda: leave_now("9701_s21_qp_12"), width=20)
    b8.grid(row=10, column=0)

    b9 = tk.Button(select_window, text="March 2021 p12", command=lambda: leave_now("9701_m21_qp_12"), width=20)
    b9.grid(row=11, column=0)

    b10 = tk.Button(select_window, text="October 2023 p12", command=lambda: leave_now("9702_w23_qp_12"), width=20)
    b10.grid(row=3, column=1)

    b11 = tk.Button(select_window, text="May 2023 p12", command=lambda: leave_now("9702_s23_qp_12"), width=20)
    b11.grid(row=4, column=1)

    b12 = tk.Button(select_window, text="March 2023 p12", command=lambda: leave_now("9702_m23_qp_12"), width=20)
    b12.grid(row=5, column=1)

    b13 = tk.Button(select_window, text="October 2022 p12", command=lambda: leave_now("9702_w22_qp_12"), width=20)
    b13.grid(row=6, column=1)

    b14 = tk.Button(select_window, text="May 2022 p12", command=lambda: leave_now("9702_s22_qp_12"), width=20)
    b14.grid(row=7, column=1)

    b15 = tk.Button(select_window, text="March 2022 p12", command=lambda: leave_now("9702_m22_qp_12"), width=20)
    b15.grid(row=8, column=1)

    b16 = tk.Button(select_window, text="October 2021 p12", command=lambda: leave_now("9702_w23_qp_12"), width=20)
    b16.grid(row=9, column=1)

    b17 = tk.Button(select_window, text="May 2021 p12", command=lambda: leave_now("9702_s23_qp_12"), width=20)
    b17.grid(row=10, column=1)

    b18 = tk.Button(select_window, text="March 2021 p12", command=lambda: leave_now("9702_m21_qp_12"), width=20)
    b18.grid(row=11, column=1)

    select_window.mainloop()


select_quiz()
TEXT_COLOR = "#2f3640"
LINX_WHITE = "#f5f6fa"
score = 0
num = 0
timer_id = None
quiz_duration = 75 * 60  # 75 minutes in seconds
is_paused = False

# Define the directory where your images are stored
path = fr"questions\Chemistry\{paper_name}"
image_directory = path
questions_data = []
user_answers = [None] * 40  # Assuming there are 40 questions

# Correct answers (you may want to adjust this)
correct_answers = data[paper_name]

# Create the main window
window = Tk()
window.title(f"QUIZ APP BY ABDULREHMAN    {paper_name}")
window.state('zoomed')  # Make window full size but keep the title bar
window.config(background=LINX_WHITE, padx=50, pady=50)

# Paper label
paper_label = Label(text=paper_name, padx=30, pady=30, background=LINX_WHITE, font=("Ariel", 20, "bold"))
paper_label.grid(row=1, column=5, columnspan=2)

# Timer label
timer_label = Label(window, text="75:00", font=("Ariel", 30, "bold"), background=LINX_WHITE)
timer_label.grid(row=2, column=5, columnspan=2)

canvas = Canvas(window, width=800, height=500, background="white")
canvas.grid(row=1, column=0, columnspan=4, rowspan=4)

# Load button images
a_image = PhotoImage(file="buttons/a.png")
b_image = PhotoImage(file="buttons/b.png")
c_image = PhotoImage(file="buttons/c.png")
d_image = PhotoImage(file="buttons/d.png")

# Create answer buttons
a_button = Button(window, image=a_image, command=lambda: record_answer("A"))
b_button = Button(window, image=b_image, command=lambda: record_answer("B"))
c_button = Button(window, image=c_image, command=lambda: record_answer("C"))
d_button = Button(window, image=d_image, command=lambda: record_answer("D"))

a_button.grid(row=5, column=0)
b_button.grid(row=5, column=1)
c_button.grid(row=5, column=2)
d_button.grid(row=5, column=3)

# Create navigation buttons
next_image = PhotoImage(file="buttons/next.png")
back_image = PhotoImage(file="buttons/back.png")
pause_image = PhotoImage(file="buttons/pause.png")
resume_image = PhotoImage(file="buttons/resume.png")
finish_image = PhotoImage(file="buttons/finish.png")


next_button = Button(window, image=next_image, command=lambda: navigate(1))
previous_button = Button(window, image=back_image, command=lambda: navigate(-1))
finish_button = Button(window, image=finish_image, command=finish_quiz)
pause_button = Button(window, image=pause_image, command=pause_quiz)

previous_button.grid(row=4, column=6)
next_button.grid(row=4, column=7)
finish_button.grid(row=5, column=6)
pause_button.grid(row=5, column=7)

load_images()
display_question()
update_timer()

window.mainloop()