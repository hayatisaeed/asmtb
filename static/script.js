// static/script.js

document.addEventListener('DOMContentLoaded', function() {
    const addButton = document.getElementById('add-row');
    const subjectsDiv = document.getElementById('subjects');

    addButton.addEventListener('click', function() {
        const lastRow = subjectsDiv.lastElementChild;
        const newRow = lastRow.cloneNode(true);
        subjectsDiv.appendChild(newRow);
    });
});
