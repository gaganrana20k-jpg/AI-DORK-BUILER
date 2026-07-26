function generateDork() {

    let website = document.getElementById("website").value.trim();
    let dorkType = document.getElementById("dorkType").value;

    if (website === "") {
        alert("Please enter a website.");
        return;
    }

    let dork = dorkType + " site:" + website;

    let dorks = [
    "site:" + website,
    "site:" + website + " filetype:pdf",
    "site:" + website + " filetype:xls",
    "site:" + website + " filetype:doc",
    "site:" + website + " inurl:login",
    "site:" + website + " inurl:admin",
    'site:' + website + ' intitle:"index of"',
    "site:" + website + " ext:sql"
];

let output = "";

dorks.forEach(function(dork){

    output += `
    <div class="result-card">
        <p>${dork}</p>

        <div class="button-group">
    <button onclick="copyText('${dork}')"> Copy</button>

    <button onclick="searchGoogle('${dork}')"> Search</button>
</div>
    </div>
    `;

});

document.getElementById("result").innerHTML = output;
document.getElementById("totalDorks").innerText = dorks.length;
document.getElementById("tips").innerHTML = `
<li>✔ PDF searches are useful for finding public documentation.</li>
<li>✔ Login page searches help locate authentication pages.</li>
<li>✔ Always use these queries only on systems you own or are authorized to test.</li>
<li>✔ Combine different search operators for more specific results.</li>
`;

fetch("/save_dork", {
    method: "POST",
    headers: {
        "Content-Type": "application/x-www-form-urlencoded"
    },
    body: "dork=" + encodeURIComponent(dorks.join("\n"))
});
}
function copyDork() {
    let text = document.getElementById("result").innerText;

    if (text === "") {
        alert("Generate a dork first!");
        return;
    }

    navigator.clipboard.writeText(text);

    alert("Dork copied!");
}
function copyText(text){

    navigator.clipboard.writeText(text);

    alert("Copied:\n\n" + text);

}
function searchGoogle(dork){

    let url = "https://www.google.com/search?q=" + encodeURIComponent(dork);

    window.open(url, "_blank");

}

function copyResult() {

    let result = document.getElementById("result");

    if (!result) {
        alert("No result found!");
        return;
    }

    navigator.clipboard.writeText(result.innerText)
        .then(() => {
            alert("✅ Result copied successfully!");
        })
        .catch(err => {
            console.error(err);
            alert(" Failed to copy.");
        });

}

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("lookupForm");
    const button = document.getElementById("lookupBtn");

    if (form && button) {

        form.addEventListener("submit", function () {

            button.innerHTML = "⏳ Looking up...";
            button.disabled = true;

        });

    }

});

function searchHistory() {

    let input = document.getElementById("historySearch").value.toLowerCase();

    let cards = document.querySelectorAll(".result-card");

    cards.forEach(card => {

        if (card.innerText.toLowerCase().includes(input)) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }

    });

}

function confirmLogout() {

    if(confirm("Are you sure you want to logout?")){
        window.location="/logout";
    }

}

const text = "🛡 AI Powered Google Dork Builder";
const typing = document.getElementById("typing");

if (typing) {

    let i = 0;

    function typeWriter() {

        if (i < text.length) {
            typing.innerHTML += text.charAt(i);
            i++;
            setTimeout(typeWriter, 60);
        }

    }

    typeWriter();

}