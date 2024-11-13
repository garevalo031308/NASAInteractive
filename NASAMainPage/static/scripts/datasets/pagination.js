// console.log(cls_info);
// console.log(dataset);
// console.log(total_images)
// console.log(images)

// for (const [cls, imageArray] of Object.entries(images)) {
//     console.log('Class:', cls);
//     for (const item of imageArray) {
//         for (const [name, path] of Object.entries(item)) {
//             console.log('Name:', name);
//             console.log('Path:', path);
//         }
//     }
// }
document.addEventListener('DOMContentLoaded', function() {
    const imageContainer = document.getElementById("dataset-images")
    const pagination = document.getElementById("pagination")
    const prevButton = document.getElementById("prev")
    const nextButton = document.getElementById("next")
    const pageNumbers = document.getElementById("page-numbers")

    const imagediv = document.getElementById("image")
    const test = document.getElementById("test")

    const totalPages = Math.ceil(total_images / 100)
    let currentPage = 1;
    console.log(totalPages)

    imagediv.innerHTML = totalPages.toString()

    function displayPage(page) {
        const startIndex = (page - 1) * cardsPerPage
        const endIndex = startIndex + cardsPerPage;
    }
});