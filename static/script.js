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

function addRow() {
    alert("we are in the function addRow")
    const subjectsDiv = document.getElementById('subjects');
    const lastRow = subjectsDiv.lastElementChild.cloneNode(true);
    subjectsDiv.appendChild(lastRow);
    // Reset the cloned row
    const clonedDropdowns = lastRow.querySelectorAll('select');
    clonedDropdowns.forEach(function(dropdown) {
        dropdown.selectedIndex = 0;
        dropdown.disabled = true;
    });
    lastRow.querySelector('input[name="hours[]"]').value = '';
    lastRow.querySelector('input[name="t_count[]"]').value = '';
}
