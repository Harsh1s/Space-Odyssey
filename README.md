## Space Odyssey

A treasure hunt web-app made for the Technex theme launch event.

## Features

1. Question can be text or image.
    - Questions are stored in a `questions.json` file. Every question is of type `i` (image) or `t` (text).
    - If image, the question text is the URL to the image. Store in [images](static/images/questions) folder.
2. Hints
    - Supports hints for every question, which can be shown by clicking the show hint button.
3. Leaderboard
    - A leaderboard that shows the rank of all registered users
4. Sequence generation.
    - Each question must have a `difficulty` attribute and this is used for generating a sequence. For example, if a user has to solve 15 questions in total. They can be of `easy`, `medium`, `hard` type.
    - Every user must also start with one question from a list of specific "start" questions with the location as the event starting location, the question difficulty can also be set as `start` and the user will have his first question as one of the any questions with difficulty as `start`.
5. Can pass HTML to question field.
    - Can pass raw HTML to question and hint field, and it is rendered. This can be used for building complex questions like crosswords.
6. Spreadsheet writer
    - Writes all registrations to a spreadsheet using Google Cloud.
    - Store credentials in a `credentials-spreadsheet.json` file.

## Config

1. `questions.json` - All questions, hints and answers.

    - JSONList.

    ```JSON
    [
       {
       "no": 1,
       "type": "i", // 'i' or 't' for image or text.
       "text": "1.png", // Question text or file name. Images must be stored in /static/images folder.
       "ans": "uranus", // Answer. Case insensitive.
       "hint": "7th planet from the sun.", // Hint, shown when user clicks show hint button on the play site
       "difficulty": "easy", // Difficulty, used for generating a sequence of questions for every user, i.e solve easy questions first and then medium and then hard, etc.
       "key": "KEY1234", // Obsolete at the moment, ignore.
       "location": "Outside Gymkhana" // Obsolete at the moment, ignore.
       },
       {
           // 2nd question.
       }
    ]
    ```

## Techstack

1. Server - Flask (Python)
    - to process the requests and handle the registration, login and play logic.
2. Database - Firebase.
    - It stores the data in [Firebase's realtime database](https://firebase.google.com/products/realtime-database)
    - NoSQL database structure is
    ```
        space-odyssey
            - users
                - regno1
                    - name
                    - email
                    - pw_hash
                    - etc
                - regno2
                    - name
                    - email
                    - pw_hash
                    - etc
    ```
    - Store the keys in a `credentials-space-odyssey.json` file in the root directory.
3. Frontend - Plain HTML, CSS and JS.
    - present in[ /templates](/templates/) and [/static](/static/) folder
4. Docker - For deployment
    - Both [`Dockerfile`](Dockerfile) and [`docker-compose.yml`](docker-compose.yml) are included for ease of use.
