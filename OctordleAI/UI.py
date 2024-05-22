import tkinter as tk
import random
from general_solver import General_Solver
import copy
import time

class OctordleUI:
    def __init__(self, master):
        self.   master = master
        master.title('Octordle Game')

        file_path = 'answers.txt'
        with open(file_path, 'r') as file:
            self.target_words = file.read().splitlines()

        #generate random 8 target words
        self.target_words = random.sample(self.target_words, 8) 
  
        self.target_words = [word.upper() for word in self.target_words]
        self.current_guess_index = 0
        self.solved_boards = [False] * len(self.target_words)
        master.geometry('1280x800')
        self.colors = {"correct": "#538d4e", "present": "#b59f3b", "absent": "#3a3a3c"}

        # Create label for "Octordle" text
        octordle_label = tk.Label(master, text="Octordle", font=('Helvetica', 40))
        octordle_label.grid(row=0, column=5, columnspan=5, pady=(10, 5))

        self.frames = [tk.Frame(master, width=100, height=600) for _ in range(8)]
        for index, frame in enumerate(self.frames):
            frame.grid(row=1, column=index * 2, padx=(5, 0), pady=5, sticky="nsew")
            if index < 7:
                separator = tk.Frame(master, width=2, height=400, bg="black")
                separator.grid(row=1, column=index * 2 + 1, sticky="ns")

        self.guess_labels = [[[tk.Label(frame, text=' ', bg="#3a3a3c", fg="white", font=('Helvetica', 16), width=2,
                                        height=1) for _ in range(5)] for _ in range(13)] for frame in self.frames]
        for frame_index, frame_labels in enumerate(self.guess_labels):
            for guess_index, row in enumerate(frame_labels):
                for letter_index, label in enumerate(row):
                    label.grid(row=guess_index, column=letter_index, padx=2, pady=2)

        self.feedback_array_all_guess = [None for _ in range(13)]
        self.feedback_array_current_guess = [[None for _ in range(5)] for _ in range(8)]

        self.guess_word = None

        self.solver = General_Solver(game=self)
        self.guess_word = self.solver.octordle_solver()

        self.start_automatic_guessing()

    def start_automatic_guessing(self):
        interval = 1
        
        while not self.check_board_solved() and self.current_guess_index < 13:
            self.submit_guess()
            time.sleep(interval)

    def submit_guess(self):
        guess = self.guess_word
        if len(guess) == 5 and self.current_guess_index < 13:
            for word_index, target_word in enumerate(self.target_words):
                if not self.solved_boards[word_index]:
                    if self.update_guess(word_index, self.current_guess_index, guess, target_word):
                        self.solved_boards[word_index] = True
            self.current_guess_index += 1
            self.update_ui()  # Update the UI after each guess
            if self.check_board_solved():
                self.display_congratulations()
                return
            elif self.current_guess_index >= 13:
                self.display_failure()
                return

        feedback = self.feedback_array_all_guess[self.current_guess_index - 1]
        self.solver.add_to_encoded_guesses(feedback)
        self.guess_word = self.solver.octordle_solver()

    def update_guess(self, word_index, guess_index, guess, target_word):
        target_word = target_word.lower()
        guess = guess.lower()
        correct_guess = True
        for i, char in enumerate(guess):
            if char == target_word[i]:
                correct_color = self.colors["correct"]
                feedback = [char, 3]
            elif char in target_word:
                correct_color = self.colors["present"]
                correct_guess = False
                feedback = [char, 2]
            else:
                correct_color = self.colors["absent"]
                correct_guess = False
                feedback = [char, 1]
            self.guess_labels[word_index][guess_index][i].config(text=char, bg=correct_color, fg="white")
            self.feedback_array_current_guess[word_index][i] = feedback
        self.feedback_array_all_guess[guess_index] = copy.deepcopy(self.feedback_array_current_guess)
        return correct_guess and guess == target_word

    def check_board_solved(self):
        return all(self.solved_boards)
    
    def update_ui(self):
        self.master.update()  # Update the UI to reflect changes

    def display_congratulations(self):
        congrats_label = tk.Label(self.master, text="Congratulations! You solved Octordle in {} guesses.".format(self.current_guess_index), font=('Helvetica', 20))
        congrats_label.grid(row=5, column=0, columnspan=20, sticky="nsew")
    
    def display_failure(self):
        failure_label = tk.Label(self.master, text="You failed to solve Octordle.", font=('Helvetica', 20))
        failure_label.grid(row=5, column=0, columnspan=20, sticky="nsew")
        
        # Create a label to display the target words
        target_words_label = tk.Label(self.master, text="Target Words: " + ", ".join(self.target_words), font=('Helvetica', 16))
        target_words_label.grid(row=6, column=0, columnspan=20, sticky="nsew")

root = tk.Tk()
app = OctordleUI(root)
root.mainloop()
