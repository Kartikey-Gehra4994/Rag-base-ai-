const form = document.getElementById("questionForm");

const questionInput =
    document.getElementById("question");

const askButton =
    document.getElementById("askButton");

const loading =
    document.getElementById("loading");

const answerCard =
    document.getElementById("answerCard");

const answer =
    document.getElementById("answer");

const copyButton =
    document.getElementById("copyButton");


form.addEventListener("submit", async function (event) {

    event.preventDefault();


    const question =
        questionInput.value.trim();


    if (!question) {
        return;
    }


    loading.classList.add("active");

    answerCard.classList.remove("active");

    askButton.disabled = true;

    askButton.textContent = "Thinking...";


    try {

        const response = await fetch("/ask", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });


        if (!response.ok) {

            throw new Error(
                "Server returned an error"
            );

        }


        const data =
            await response.json();


        answer.textContent =
            data.answer;


        answerCard.classList.add("active");


        setTimeout(() => {

            answerCard.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });

        }, 100);


    } catch (error) {

        answer.textContent =
            "Something went wrong while processing your question. Please try again.";

        answerCard.classList.add("active");

        console.error(error);

    } finally {

        loading.classList.remove("active");

        askButton.disabled = false;

        askButton.textContent = "Ask AI";

    }

});


/* Example question buttons */

document.querySelectorAll(".example").forEach(button => {

    button.addEventListener("click", function () {

        questionInput.value =
            this.dataset.question;

        questionInput.focus();

    });

});


/* Copy answer */

copyButton.addEventListener("click", async function () {

    const text = answer.textContent;

    if (!text) {
        return;
    }


    try {

        await navigator.clipboard.writeText(text);

        copyButton.textContent = "Copied";

        setTimeout(() => {

            copyButton.textContent = "Copy";

        }, 1500);

    } catch (error) {

        console.error(error);

    }

});


/* Enter key */

questionInput.addEventListener("keydown", function (event) {

    if (event.key === "Enter") {

        event.preventDefault();

        form.requestSubmit();

    }

});