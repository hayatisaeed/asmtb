// static/script.js

function subjectChanged(selectElement, subjects) {
    alert("we are in the function subjectChanged")
    const underSubjectsDropdown = selectElement.parentElement.querySelector('.under-subject');
    const underUnderSubjectsDropdown = selectElement.parentElement.querySelector('.under-under-subject');
    const selectedSubject = selectElement.value;

    // Enable the under subject dropdown
    underSubjectsDropdown.disabled = false;

    // Clear existing options
    underSubjectsDropdown.innerHTML = '<option value="">Select Under Subject</option>';
    underUnderSubjectsDropdown.innerHTML = '<option value="">Select Under Under Subject</option>';

    // Get the under subjects for the selected subject
    const underSubjects = subjects[selectedSubject];

    // Populate underSubjectsDropdown with the under subjects
    Object.keys(underSubjects).forEach(function(underSubject) {
        const option = document.createElement('option');
        option.text = underSubject;
        option.value = underSubject;
        underSubjectsDropdown.add(option);
    });

    // Disable the under under subject dropdown until under subject is selected
    underUnderSubjectsDropdown.disabled = true;
}

function underSubjectChanged(selectElement, subjects) {
    alert("we are in the function underSubjectChanged")
    const underUnderSubjectsDropdown = selectElement.parentElement.querySelector('.under-under-subject');
    const selectedSubject = selectElement.parentElement.querySelector('.subject').value;
    const selectedUnderSubject = selectElement.value;

    const underUnderSubjects = subjects[selectedSubject][selectedUnderSubject];

    // Enable the under under subject dropdown
    underUnderSubjectsDropdown.disabled = false;

    // Clear existing options
    underUnderSubjectsDropdown.innerHTML = '<option value="">Select Under Under Subject</option>';

    // Populate underUnderSubjectsDropdown based on the selected subject and under subject
    underUnderSubjects.forEach(function(underUnderSubject) {
        const option = document.createElement('option');
        option.text = underUnderSubject;
        option.value = underUnderSubject;
        underUnderSubjectsDropdown.add(option);
    });
}

let rowCount = 1; // Initialize row counter

function addRow() {
    const subjectsDiv = document.getElementById('subjects');
    rowCount++; // Increment row counter

    // HTML template for a new row
    const newRowHTML = `
        <div class="row">
                <select name="subject[]" class="subject" onchange="subjectChanged(this, {{ subjects }})">
                    <option value="">Select Subject</option>
                    {% for subject in subjects %}
                    <option value="{{ subject }}">{{ subject }}</option>
                    {% endfor %}
                </select>
                <select name="under_subject[]" class="under-subject" disabled onchange="underSubjectChanged(this, {{ subjects }})">
                    <option value="">Select Under Subject</option>
                </select>
                <select name="under_under_subject[]" class="under-under-subject" disabled>
                    <option value="">Select Under-Under Subject</option>
                </select>
                <input type="number" name="hours[]" placeholder="Hours" min="1" required>
                <input type="number" name="t_count[]" placeholder="T Count" min="1" required>
            </div>
    `;

    // Create a new div element and set its innerHTML to the new row HTML
    const newDiv = document.createElement('div');
    newDiv.innerHTML = newRowHTML;

    // Append the new row to the subjects div
    subjectsDiv.appendChild(newDiv);
}

