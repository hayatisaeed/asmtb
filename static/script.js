// static/script.js

document.addEventListener('DOMContentLoaded', function() {
    const subjects = {{ subjects | tojson }};
    const subjectsDropdowns = document.querySelectorAll('.subject');

    subjectsDropdowns.forEach(function(dropdown) {
        dropdown.addEventListener('change', function() {
            const underSubjectsDropdown = dropdown.parentElement.querySelector('.under-subject');
            const underUnderSubjectsDropdown = dropdown.parentElement.querySelector('.under-under-subject');
            const selectedSubject = dropdown.value;

            // Clear existing options
            underSubjectsDropdown.innerHTML = '<option value="">Select Under Subject</option>';
            underUnderSubjectsDropdown.innerHTML = '<option value="">Select Under Under Subject</option>';

            // Populate underSubjectsDropdown based on the selected subject
            Object.keys(subjects[selectedSubject]).forEach(function(underSubject) {
                const option = document.createElement('option');
                option.text = underSubject;
                option.value = underSubject;
                underSubjectsDropdown.add(option);
            });
        });
    });

    // Handle change in underSubjectsDropdown
    document.querySelectorAll('.under-subject').forEach(function(underSubjectDropdown) {
        underSubjectDropdown.addEventListener('change', function() {
            const underUnderSubjectsDropdown = underSubjectDropdown.parentElement.querySelector('.under-under-subject');
            const selectedSubject = underSubjectDropdown.parentElement.querySelector('.subject').value;
            const selectedUnderSubject = underSubjectDropdown.value;

            // Clear existing options
            underUnderSubjectsDropdown.innerHTML = '<option value="">Select Under Under Subject</option>';

            // Populate underUnderSubjectsDropdown based on the selected subject and under subject
            subjects[selectedSubject][selectedUnderSubject].forEach(function(underUnderSubject) {
                const option = document.createElement('option');
                option.text = underUnderSubject;
                option.value = underUnderSubject;
                underUnderSubjectsDropdown.add(option);
            });
        });
    });

    const addButton = document.getElementById('add-row');
    const subjectsDiv = document.getElementById('subjects');

    addButton.addEventListener('click', function() {
        const lastRow = subjectsDiv.lastElementChild;
        const newRow = lastRow.cloneNode(true);
        subjectsDiv.appendChild(newRow);
    });
});