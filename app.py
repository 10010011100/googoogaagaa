from flask import Flask, render_template, request
import random as ran
import time as t
import requests as req
import string as str
from spellchecker import SpellChecker

uid = "0"
app = Flask(__name__)
inputList = []
wrongInput = []
wrongLetter = []
wrongPInput = []
correctInput = []

@app.route("/")
def home():
    global wrongInput, inputList, attempts, word, uid, wrongLetter, wrongPInput, correctInput
    inputList = []
    wrongInput = []
    wrongLetter = []
    wrongPInput = []
    correctInput = []
    uid = "0"
    length = 20
    uid = str.ascii_letters + str.digits
    with open("words.txt") as file:
        words = file.read().splitlines()
    word = ran.choice(words)
    ascii = 97
    for i in range(26):
        streak = 0
        for j in range(len(word)):
            if chr(ascii) == word[j]:
                break
            elif chr(ascii) != word[j]:
                streak += 1
            if streak == len(word):
                wrongLetter.append(chr(ascii))
        ascii += 1
    attempts = 0
    boom = ''.join(ran.choices(uid, k=length))
    print(wrongLetter)
    return render_template("index.html", uid = boom)
bang = uid
@app.route("/<bang>", methods=["GET","POST"])
def start(bang):
    global wrongInput, inputList, attempts, wordle, word, wrongLetter, wrongPInput, correctInput
    wordle = ""
    length = len(word)
    session = t.strftime("%H:%M:%S")
    result = ""
    wrong = ""
    spell = SpellChecker()
    if request.method == "POST":
        user_input = request.form["guess"].lower()
        if user_input == word:
            result = "correct"
            attempts += 1
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = req.get(url)
            data = response.json()
            meaning = data[0]["meanings"][0]["definitions"][0]["definition"]
            return render_template(
            "index2.html",
            user_input=user_input,
            meaning=meaning,
            attempts=attempts,
            inputList=inputList)
        
        elif len(user_input) != len(word) or user_input not in spell:
            result = "invalid"
            attempts += 1
            return render_template(
            "index1.html",
            session=session, 
            result=result, 
            length=length, 
            wrong=wrong,
            wordle=wordle,
            attempts=attempts,
            word=word,
            wrongInput=wrongInput,
            inputList=inputList,
            correctInput=correctInput,
            wrongPInput=wrongPInput)
        
        else:
            attempts += 1
            result = "wrong"
            
        guess_data = []

        for i in range(len(word)):
            letter = user_input[i]

            if letter == word[i]:
                status = "correct"
                correctInput.append(letter)

            elif letter in word:
                status = "partial"
                wrongPInput.append(letter)

            else:
                status = "wrong"
                wrongInput.append(letter)

            guess_data.append({
                "letter": letter,
                "status": status
            })

        inputList.append(guess_data)
        print(inputList)
        wrongInput = list(set(wrongInput))
        wrongPInput = list(set(wrongPInput))
        correctInput = list(set(correctInput))

    return render_template(
        "index1.html",
        session=session, 
        result=result, 
        length=length, 
        wrong=wrong,
        wordle=wordle,
        attempts=attempts,
        wrongLetter=wrongLetter,
        word=word,
        wrongInput=wrongInput,
        inputList=inputList,
        correctInput=correctInput,
        wrongPInput=wrongPInput)

if __name__ == "__main__":
    app.run(debug=True)