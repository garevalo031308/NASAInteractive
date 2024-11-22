document.addEventListener('DOMContentLoaded', function() {
    function addNestedInline(parentInlineId, nestedInlineClass) {
        const parentInline = document.getElementById(parentInlineId);
        if (!parentInline) return;

        const nestedInlines = parentInline.getElementsByClassName(nestedInlineClass);
        const totalFormsInput = parentInline.querySelector('input[name$="-TOTAL_FORMS"]');
        let totalForms = parseInt(totalFormsInput.value, 10);

        const newNestedInline = nestedInlines[0].cloneNode(true);
        newNestedInline.innerHTML = newNestedInline.innerHTML.replace(/__prefix__/g, totalForms);
        parentInline.appendChild(newNestedInline);

        totalForms += 1;
        totalFormsInput.value = totalForms;
    }

    // Example usage:
    // addNestedInline('id_foldinfo_set-group', 'foldclassinfo_set');
});