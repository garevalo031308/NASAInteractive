document.addEventListener('DOMContentLoaded', function() {
    const imagediv = document.getElementById("dataset-images");
    const prevButton = document.getElementById("prev");
    const nextButton = document.getElementById("next");
    const pageNumbers = document.getElementById("page-numbers");
    const searchFilter = document.getElementById("class-filter");

    // Filter Elements
    const classFilters = document.querySelectorAll(".class_labels");
    const filterButton = document.getElementById("filterbutton");
    const resetButton = document.getElementById("resetbutton");

    const cardsPerPage = 100; // Number of images to show per page
    let totalPages = Math.ceil(total_images / cardsPerPage);
    searchFilter.min = 1;
    searchFilter.max = totalPages;

    let currentPage = 1;
    let filteredImages = images;

    searchFilter.value = currentPage;
    resetButton.disabled = true;

    function getTotalPages(className) {
        if (className === "") {
            totalPages = Math.ceil(total_images / cardsPerPage);
        } else {
            for (const [cls, image] of Object.entries(filteredImages)) {
                if (className === cls) {
                    totalPages = Math.ceil(image.length / cardsPerPage);
                }
            }
        }
    }

    function displayPage(page) {
        imagediv.innerHTML = ''; // Clear previous images
        const startIndex = (page - 1) * cardsPerPage;
        const endIndex = startIndex + cardsPerPage;
        let count = 0;
        const fragment = document.createDocumentFragment();

        for (const [cls, imageArray] of Object.entries(filteredImages)) {
            if (count >= endIndex) break;
            for (const item of imageArray) {
                if (count >= endIndex) break;
                if (count >= startIndex) {
                    for (const [name, path] of Object.entries(item)) {
                        const imgDiv = document.createElement("div");
                        imgDiv.id = "dataset-image-div";

                        const imgClass = document.createElement("p");
                        imgClass.id = "dataset-image-class";
                        imgClass.innerHTML = "Class: " + cls;

                        const img = document.createElement("img");
                        img.src = "/static/" + path;
                        img.id = 'dataset-image';
                        img.alt = name;

                        const header3 = document.createElement("p");
                        header3.id = "dataset-image-name";
                        header3.innerHTML = name;

                        imgDiv.appendChild(img);
                        imgDiv.appendChild(header3);
                        imgDiv.appendChild(imgClass);
                        fragment.appendChild(imgDiv);
                    }
                }
                count++;
            }
        }
        imagediv.appendChild(fragment);
        pageNumbers.textContent = `Page ${currentPage} of ${totalPages}`;
        prevButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages;
    }

    function filterImages(filterClass) {
        filteredImages = Object.fromEntries(
            Object.entries(images).filter(([cls]) => cls.toLowerCase().includes(filterClass.toLowerCase()))
        );
        getTotalPages(filterClass);
        currentPage = 1;
        displayPage(currentPage);
    }

    function searchPage() {
        const pageNumber = parseInt(searchFilter.value, 10);
        if (pageNumber > totalPages) {
            alert("Page number is bigger than the amount of pages");
        } else if (pageNumber < 1) {
            alert("Page number is smaller than the amount of pages");
        } else {
            currentPage = pageNumber;
            displayPage(pageNumber);
        }
    }

    resetButton.addEventListener('click', () => {
        filterImages("");
        resetButton.disabled = true;
        searchFilter.value = 1;
        currentPage = 1;
        searchFilter.value = currentPage;
        classFilters.forEach(button => {
            button.checked = false;
        });
    });

    filterButton.addEventListener('click', () => {
        let checkedButton = null;
        currentPage = 1;
        searchFilter.value = currentPage;
        classFilters.forEach(button => {
            if (button.checked) {
                checkedButton = button;
            }
        });
        if (checkedButton) {
            filterImages(checkedButton.id);
            resetButton.disabled = false;
        }
    });

    prevButton.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent default anchor behavior
        if (currentPage > 1) {
            currentPage--;
            searchFilter.value = currentPage;
            displayPage(currentPage);
        }
    });

    nextButton.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent default anchor behavior
        if (currentPage < totalPages) {
            currentPage++;
            searchFilter.value = currentPage;
            displayPage(currentPage);
        }
    });

    searchFilter.addEventListener('input', searchPage);

    displayPage(currentPage); // Initial page load
});