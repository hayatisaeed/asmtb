// static/script.js

function subjectChanged(selectElement, subjects) {
    const underSubjectsDropdown = selectElement.parentElement.querySelector('.under-subject');
    const underUnderSubjectsDropdown = selectElement.parentElement.querySelector('.under-under-subject');
    const selectedSubject = selectElement.value;

    // Enable the under subject dropdown
    underSubjectsDropdown.disabled = false;

    // Clear existing options
    underSubjectsDropdown.innerHTML = '<option value="">درس را انتخاب کنید</option>';
    underUnderSubjectsDropdown.innerHTML = '<option value="">مبحث را انتخاب کنید</option>';

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
    underUnderSubjectsDropdown.innerHTML = '<option value="">مبحث را انتخاب کنید</option>';

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

    const newRow = document.createElement('div');
    newRow.classList.add('row');

    const subjectSelect = document.createElement('select');
    subjectSelect.name = `subject[${rowCount - 1}]`;
    subjectSelect.classList.add('subject');
    subjectSelect.addEventListener('change', function() {
        subjectChanged(this, subjects);
    });
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'کتاب را انتخاب کنید';
    subjectSelect.appendChild(defaultOption);
    for (const subject in subjects) {
        const option = document.createElement('option');
        option.value = subject;
        option.textContent = subject;
        subjectSelect.appendChild(option);
    }

    const underSubjectSelect = document.createElement('select');
    underSubjectSelect.name = `under_subject[${rowCount - 1}]`;
    underSubjectSelect.classList.add('under-subject');
    underSubjectSelect.disabled = true;
    underSubjectSelect.addEventListener('change', function() {
        underSubjectChanged(this, subjects);
    });
    const underSubjectDefaultOption = document.createElement('option');
    underSubjectDefaultOption.value = '';
    underSubjectDefaultOption.textContent = 'درس را انتخاب کنید';
    underSubjectSelect.appendChild(underSubjectDefaultOption);

    const underUnderSubjectSelect = document.createElement('select');
    underUnderSubjectSelect.name = `under_under_subject[${rowCount - 1}]`;
    underUnderSubjectSelect.classList.add('under-under-subject');
    underUnderSubjectSelect.disabled = true;
    const underUnderSubjectDefaultOption = document.createElement('option');
    underUnderSubjectDefaultOption.value = '';
    underUnderSubjectDefaultOption.textContent = 'مبحث را انتخاب کنید';
    underUnderSubjectSelect.appendChild(underUnderSubjectDefaultOption);

    const hoursInput = document.createElement('input');
    hoursInput.type = 'number';
    hoursInput.name = `hours[${rowCount - 1}]`;
    hoursInput.placeholder = 'ساعت';
    hoursInput.min = 1;
    hoursInput.required = true;

    const tCountInput = document.createElement('input');
    tCountInput.type = 'number';
    tCountInput.name = `t_count[${rowCount - 1}]`;
    tCountInput.placeholder = 'تعداد تست';
    tCountInput.min = 1;
    tCountInput.required = true;

    newRow.appendChild(subjectSelect);
    newRow.appendChild(underSubjectSelect);
    newRow.appendChild(underUnderSubjectSelect);
    newRow.appendChild(hoursInput);
    newRow.appendChild(tCountInput);

    subjectsDiv.appendChild(newRow);
}
