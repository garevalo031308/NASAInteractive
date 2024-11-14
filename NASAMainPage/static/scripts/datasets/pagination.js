document.addEventListener('DOMContentLoaded', function() {
    const imagediv = document.getElementById("dataset-images");
    const pagination = document.getElementById("pagination");
    const prevButton = document.getElementById("prev");
    const nextButton = document.getElementById("next");
    const pageNumbers = document.getElementById("page-numbers");
    const classFilter = document.getElementById("class-filter");

    const cardsPerPage = 100; // Number of images to show per page
    const totalPages = Math.ceil(total_images / cardsPerPage);
    let currentPage = 1;
    let filteredImages = images;

    function displayPage(page) {
        imagediv.innerHTML = ''; // Clear previous images
        const startIndex = (page - 1) * cardsPerPage;
        const endIndex = startIndex + cardsPerPage;
        let count = 0;

        for (const [cls, imageArray] of Object.entries(filteredImages)) {
            if (count >= endIndex) break;
            for (const item of imageArray) {
                if (count >= endIndex) break;
                if (count >= startIndex) {
                    for (const [name, path] of Object.entries(item)) {
                        const imgDiv = document.createElement("div");
                        imgDiv.id = "dataset-image";

                        const img = document.createElement("img");
                        img.src = "/static/" + path;
                        img.alt = name;

                        const header3 = document.createElement("h3");
                        header3.innerHTML = name;

                        imgDiv.appendChild(img);
                        imgDiv.appendChild(header3);
                        imagediv.appendChild(imgDiv);
                    }
                }
                count++;
            }
        }
        pageNumbers.textContent = `Page ${currentPage} of ${totalPages}`;
        prevButton.disabled = currentPage === 1;
        nextButton.disabled = currentPage === totalPages;
    }

    function filterImages() {
        const filterValue = classFilter.value.toLowerCase();
        filteredImages = Object.fromEntries(
            Object.entries(images).filter(([cls]) => cls.toLowerCase().includes(filterValue))
        );
        currentPage = 1;
        displayPage(currentPage);
    }

    prevButton.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent default anchor behavior
        if (currentPage > 1) {
            currentPage--;
            displayPage(currentPage);
        }
    });

    nextButton.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent default anchor behavior
        if (currentPage < totalPages) {
            currentPage++;
            displayPage(currentPage);
        }
    });

    classFilter.addEventListener('input', filterImages);

    displayPage(currentPage); // Initial page load
});