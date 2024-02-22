// static/script.js

document.addEventListener('DOMContentLoaded', function() {
    const subjects = {{ subjects | tojson }};
    const subjectsDropdowns = document.querySelectorAll('.subject');

    subjectsDropdowns.forEach(function(dropdown) {
        dropdown.addEventListener('change', function() {
            const underSubjectsDropdown = dropdown.parentElement.querySelector('.under-subject');
            const underUnderSubjectsDropdown = dropdown.parentElement.querySelector('.under-under-subject');
            const selectedSubject = dropdown.value;

            // Clear existing options and disable dropdowns
            underSubjectsDropdown.innerHTML = '<option value="" disabled selected>Select Under Subject</option>';
            underUnderSubjectsDropdown.innerHTML = '<option value="" disabled selected>Select Under Under Subject</option>';
            underSubjectsDropdown.disabled = true;
            underUnderSubjectsDropdown.disabled = true;

            // Populate underSubjectsDropdown based on the selected subject
            const underSubjects = subjects[selectedSubject];
            Object.keys(underSubjects).forEach(function(underSubject) {
                const option = document.createElement('option');
                option.text = underSubject;
                option.value = underSubject;
                underSubjectsDropdown.add(option);
            });

            // Enable underSubjectsDropdown
            underSubjectsDropdown.disabled = false;
        });
    });

    // Handle change in underSubjectsDropdown
    document.querySelectorAll('.under-subject').forEach(function(underSubjectDropdown) {
        underSubjectDropdown.addEventListener('change', function() {
            const underUnderSubjectsDropdown = underSubjectDropdown.parentElement.querySelector('.under-under-subject');
            const selectedSubject = underSubjectDropdown.parentElement.querySelector('.subject').value;
            const selectedUnderSubject = underSubjectDropdown.value;

            // Clear existing options and disable dropdown
            underUnderSubjectsDropdown.innerHTML = '<option value="" disabled selected>Select Under Under Subject</option>';
            underUnderSubjectsDropdown.disabled = true;

            // Populate underUnderSubjectsDropdown based on the selected subject and under subject
            const underUnderSubjects = subjects[selectedSubject][selectedUnderSubject];
            underUnderSubjects.forEach(function(underUnderSubject) {
                const option = document.createElement('option');
                option.text = underUnderSubject;
                option.value = underUnderSubject;
                underUnderSubjectsDropdown.add(option);
            });

            // Enable underUnderSubjectsDropdown
            underUnderSubjectsDropdown.disabled = false;
        });
    });

    const addButton = document.getElementById('add-row');
    const subjectsDiv = document.getElementById('subjects');

    addButton.addEventListener('click', function() {
        const lastRow = subjectsDiv.lastElementChild;
        const newRow = lastRow.cloneNode(true);
        subjectsDiv.appendChild(newRow);

        // Reset cloned row
        const clonedSubjectDropdown = newRow.querySelector('.subject');
        const clonedUnderSubjectDropdown = newRow.querySelector('.under-subject');
        const clonedUnderUnderSubjectDropdown = newRow.querySelector('.under-under-subject');
        const clonedHoursInput = newRow.querySelector('input[name="hours[]"]');
        const clonedTCountInput = newRow.querySelector('input[name="t_count[]"]');

        clonedSubjectDropdown.value = '';
        clonedUnderSubjectDropdown.innerHTML = '<option value="" disabled selected>Select Under Subject</option>';
        clonedUnderUnderSubjectDropdown.innerHTML = '<option value="" disabled selected>Select Under Under Subject</option>';
        clonedUnderSubjectDropdown.disabled = true;
        clonedUnderUnderSubjectDropdown.disabled = true;
        clonedHoursInput.value = '';
        clonedTCountInput.value = '';
    });
});
