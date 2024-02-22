// static/script.js

function subjectChanged(selectElement, subjects) {
    alert("entered the function")
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

function addRow(subjects) {
    const subjectsDiv = document.getElementById('subjects');
    const rowCount = subjectsDiv.childElementCount + 1;
    let newRowHTML = `
        <div class="row">
            <select name="subject[${rowCount - 1}]" class="subject">
                <option value="">Select Subject</option>
    `;

    for (const subject in subjects) {
        newRowHTML += `<option value="${subject}">${subject}</option>`;
    }


    newRowHTML += `
            </select>
            <select name="under_subject[${rowCount - 1}]" class="under-subject" disabled 
            onchange="subjectChanged(this, ${subjects})">
                <option value="">Select Under Subject</option>
            </select>
            <select name="under_under_subject[${rowCount - 1}]" class="under-under-subject" 
            disabled onchange="underSubjectChanged(this, ${subjects})">
                <option value="">Select Under Under Subject</option>
            </select>
            <input type="number" name="hours[${rowCount - 1}]" placeholder="Hours" min="1" required>
            <input type="number" name="t_count[${rowCount - 1}]" placeholder="T Count" min="1" required>
        </div>
    `;


    const newDiv = document.createElement('div');
    newDiv.innerHTML = newRowHTML;
    subjectsDiv.appendChild(newDiv);
}

