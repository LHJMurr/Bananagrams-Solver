import tkinter as tk

def loadWords():
    with open('words.txt') as f:
        words = ''
        for line in f.read():
            words += line
        wordsList = words.split(' ')
    return wordsList

wordsList = loadWords()

def countLetters(word):
    ''' Takes in a string and outputs a dictionary of each letter and the number of times it occurs. '''
    word = word.lower() # case is irrelevant, choose lowercase for simplicity
    dict = {}
    for char in word:
        if char not in dict.keys():
            dict[char] = 1
        else:
            dict[char] += 1
    return dict

def anagram(string, words = wordsList, max_len = 7, known = []):
    ''' Takes in a string of letters and a list of words and outputs all possible combinations to be made from those
    letters in the given list '''
    ans = []
    for word in words:
        if word in known:
            ans.append(word)
        letter_count = countLetters(string)
        if len(word) > max_len:
            continue
        flag = True
        for char in word:
            if char not in letter_count.keys():
                flag = False
                break
            elif letter_count[char] == 0:
                flag = False
                break
            else:
                letter_count[char] -= 1
        if flag:
            ans.append(word)
    return ans[::-1]

# Tkinter Button Functions
def get_anagrams():
    global anagram_words
    global index
    global status
    # Clear previous set of words
    anagram_words = []
    index = 0
    # Clear the display window
    anagram_entry.delete(0,'end')
    # Get the new words
    string = text_entry.get()
    words = anagram(string, words = loadWords(), max_len=15)
    if words == []:
        anagram_words = ['']
    else:
        anagram_words = words
    # Display the first word in the list
    anagram_entry.insert(0,anagram_words[index])
    # Add the Status Bar
    status.grid_forget()
    status = tk.Label(root, text=f'Anargram {index + 1} of {len(anagram_words)}', bd=1, relief='sunken')
    status.grid(row=3, column=2)

def scroll_left():
    global anagram_words
    global index
    global status
    new_index = index - 1
    if new_index >= 0:
        anagram_entry.delete(0,'end')
        anagram_entry.insert(0,anagram_words[new_index])
        index = new_index

        status.grid_forget()
        status = tk.Label(root, text=f'Anargram {index + 1} of {len(anagram_words)}', bd=1, relief='sunken')
        status.grid(row=3, column=2)
    else:
        pass


def scroll_right():
    global anagram_words
    global index
    global status
    new_index = index + 1
    if new_index < len(anagram_words):
        anagram_entry.delete(0,'end')
        anagram_entry.insert(0,anagram_words[new_index])
        index = new_index

        status.grid_forget()
        status = tk.Label(root, text=f'Anargram {index + 1} of {len(anagram_words)}', bd=1, relief='sunken')
        status.grid(row=3, column=2)
    else:
        pass

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Anagram Solver')
    # Get constant UI elements
    text_entry = tk.Entry(root, width = 60, border = 5)
    text_entry.grid(row=0, column=0, columnspan=3)
    anag_button = tk.Button(root, text='Get Anagrams!', width = 20, height = 5, command=get_anagrams)
    left_button = tk.Button(root, text='Back', width = 20, height = 5, command=scroll_left)
    right_button = tk.Button(root, text='Next', width = 20, height = 5, command=scroll_right)
    buttons = [left_button, anag_button, right_button]
    for i in range(len(buttons)):
        buttons[i].grid(row=1, column=i, columnspan=1)
    anagram_entry = tk.Entry(root, width=60, border=5)
    anagram_entry.grid(row=2, column=0, columnspan=3,pady=10)

    anagram_words = []
    index = 0

    status = tk.Label(root, text='')

    tk.mainloop()