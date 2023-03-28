var element =  document.getElementById('message');
if (typeof(element) != 'undefined' && element != null) {
    setTimeout(function() {
        element.style.display='none'
    }, 3000)
}


function checkForPage1() {
    // check if these elements exist on page
    // if exists get cookies values
    let correct_element=0;
    let incorrect_element=0;
    if (document.getElementById("correct_answers") && document.getElementById("incorrect_answers")) {
        correct_element = document.getElementById("correct_answers");
        incorrect_element = document.getElementById("incorrect_answers");
    }
    
    // get url params
    const params = new Proxy(new URLSearchParams(window.location.search), {
        get: (searchParams, prop) => searchParams.get(prop),
    });
    // Get the value of "page" from url params
    let page = params.page;
    
    if (correct_element && incorrect_element) {    
        if (page == null || page == 1) {
            localStorage.setItem('correct', 0);
            localStorage.setItem('incorrect', 0);
        }
    } else{
        localStorage.setItem('correct', 0);
        localStorage.setItem('incorrect', 0);
    }

    if (document.getElementById("correct_answers") && document.getElementById("incorrect_answers")) {
        updateUI();
    }
}


function updateUI() {
    // get localStorage object
    obj = Object(localStorage);
    
    // check if correct and incorrect keys exist in localStorage obj
    if ('correct' in obj && 'incorrect' in obj) {
        document.getElementById("correct_answers").textContent = obj.correct;
        document.getElementById("incorrect_answers").textContent = obj.incorrect;
    }
}



function checkAnswer() {
    // get the pathname from url
    pth_name = window.location.pathname.split('/')[1]
    console.log(pth_name);
    // keep the selected response
    selected = document.querySelector('input[name^="answer_question"]:checked');
    
    // get the right response
    correct_answer = document.querySelector('input[value=True]');
    
    // apply css class for correct or wrong answer 
    if (selected === correct_answer) {
        // find the correct element for applying the class
        if (pth_name != 'sima-start-test') {
            document.getElementById(selected.id).nextElementSibling.classList.add('correct');
        }
        
        // get the current value from localStorage
        correct_answers = parseInt(localStorage.getItem('correct'));

        // increment localStorage value
        localStorage.setItem('correct', correct_answers+1);
    } else {
        if (pth_name != 'sima-start-test') {
            document.getElementById(selected.id).nextElementSibling.classList.add('incorrect');
            
            // also show the correct answer
            document.getElementById(correct_answer.id).nextElementSibling.classList.add('correct');
        }

        // get the current value from localStorage
        incorrect_answers = parseInt(localStorage.getItem('incorrect'));

        // increment localStorage value
        localStorage.setItem('incorrect', incorrect_answers+1);
    }

    // update the scores
    updateUI();
    
    // after user check a response disable all responses to be not clickable
    const radioButtons = document.querySelectorAll('input[name^="answer_question"]');
    for(const radioButton of radioButtons){
        radioButton.setAttribute('disabled', '')
    }

    // enable next question button
    if (document.getElementById("next_question")) {
        document.getElementById("next_question").removeAttribute("aria-disabled");
        document.getElementById("next_question").removeAttribute("tabindex");
        document.getElementById("next_question").classList.remove("disabled");
    }

    // get current question
    currentQuestion = parseInt(document.getElementById('current_question').textContent);
    if (currentQuestion === questions) {
        checkScore();
    }
}



// ===========================
// -- calculating the score --
// ===========================
const minSuccessPercentage = .15;

// get total number of question
if (document.getElementById('total_questions')) {
    questions = parseInt(document.getElementById('total_questions').textContent);
    maxCorrectAnswers = Math.floor(questions - questions*minSuccessPercentage);
}


function checkScore() {
    // get correct answers
    correctAnswers = parseInt(localStorage.getItem('correct'));
    if (correctAnswers >= maxCorrectAnswers) {
        msg = 'Felicitari! Ai trecut testul!';
        document.getElementById('show_score').classList.add('alert', 'alert-success');
        document.getElementById('show_score').setAttribute('role', 'alert');
        document.getElementById('show_score').textContent = msg
    } else {
        msg = 'Ne pare rau, ai picat examenul. Mai studiaza si incearca din nou.';
        document.getElementById('show_score').classList.add('alert', 'alert-danger');
        document.getElementById('show_score').setAttribute('role', 'alert');
        document.getElementById('show_score').textContent = msg
    }

    saveScore();
}

function saveScore() {
    correctAnswers = parseInt(localStorage.getItem('correct'));
    incorrectAnswers = parseInt(localStorage.getItem('incorrect'));

    // fill hidden inputs with the above values
    correct_score = document.getElementById('correct').value = correctAnswers;
    incorrect_score = document.getElementById('incorrect').value = incorrectAnswers;
}