const question = document.getElementById('question');

console.log(question);

const answerButton = document.getElementById('answer-button');

answerButton.addEventListener('click', () => {

    const selectedAnswer = document.querySelector("input[name='answer']:checked").value;
    const correctAnswer = question.dataset.correctAnswer;
    const explanation = question.dataset.explanation;

    const isCorrect = (selectedAnswer === correctAnswer);
    const explanationBox = document.createElement("div");

    explanationBox.classList.add(isCorrect ? 'success' : 'danger');
    explanationBox.innerHTML = `<span>Answer: ${correctAnswer}</span><br>
    <span class="${isCorrect ? 'text-primary': 'text-danger'}">${isCorrect ? 'Correct!' : 'Wrong.'}</span><br>
                                <p>${explanation}</p>`;
    question.appendChild(explanationBox);

    const nextButton = document.getElementById('next-button');
    nextButton.classList.remove('d-none');

    // Answerボタンを削除
    answerButton.remove();
});

document.getElementById('next-button').addEventListener('click', function () {
    // 通常の送信を行う
    document.getElementById('question-form').submit();
});