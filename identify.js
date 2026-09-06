const imageInput = document.getElementById("plant-image");

const cameraInput = document.getElementById("camera-input");

const uploadBox = document.getElementById("upload-box");

const previewContainer =
    document.getElementById("preview-container");

const imagePreview =
    document.getElementById("image-preview");

const analyzeButton =
    document.getElementById("analyze-button");

const removeImage =
    document.getElementById("remove-image");

const analysisStatus =
    document.getElementById("analysis-status");

const resultContainer =
    document.getElementById("result-container");


// Initially hide sections

previewContainer.style.display = "none";

analysisStatus.style.display = "none";

resultContainer.style.display = "none";


// ========================================
// HANDLE IMAGE
// ========================================

function handleImage(file) {

    if (!file) {
        return;
    }


    // Check file type

    if (!file.type.startsWith("image/")) {

        alert("Please select an image file.");

        return;
    }


    // Check file size

    if (file.size > 10 * 1024 * 1024) {

        alert("Image must be smaller than 10 MB.");

        return;
    }


    const imageURL =
        URL.createObjectURL(file);


    imagePreview.src = imageURL;


    previewContainer.style.display = "block";

    resultContainer.style.display = "none";

    analysisStatus.style.display = "none";


    // Scroll to preview

    previewContainer.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });

}


// ========================================
// FILE INPUT
// ========================================

imageInput.addEventListener("change", function () {

    const file = imageInput.files[0];

    handleImage(file);

});


// ========================================
// CAMERA INPUT
// ========================================

cameraInput.addEventListener("change", function () {

    const file = cameraInput.files[0];

    handleImage(file);

});


// ========================================
// DRAG & DROP
// ========================================

uploadBox.addEventListener("dragover", function (event) {

    event.preventDefault();

    uploadBox.classList.add("dragging");

});


uploadBox.addEventListener("dragleave", function () {

    uploadBox.classList.remove("dragging");

});


uploadBox.addEventListener("drop", function (event) {

    event.preventDefault();

    uploadBox.classList.remove("dragging");


    const file = event.dataTransfer.files[0];

    handleImage(file);

});


// ========================================
// REMOVE IMAGE
// ========================================

removeImage.addEventListener("click", function () {

    imageInput.value = "";

    cameraInput.value = "";

    imagePreview.src = "";

    previewContainer.style.display = "none";

});


// ========================================
// ANALYZE PLANT
// ========================================

analyzeButton.addEventListener("click", function () {

    previewContainer.style.display = "none";

    analysisStatus.style.display = "block";


    analysisStatus.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });


    // Temporary demo delay

    setTimeout(function () {

        analysisStatus.style.display = "none";

        resultContainer.style.display = "block";


        document.getElementById("plant-name")
            .textContent = "🌿 Money Plant";


        document.getElementById("plant-confidence")
            .textContent = "AI Confidence: 94%";


        document.getElementById("plant-description")
            .textContent =
            "This is a demonstration result. Later, FloraSense will connect this page to a real plant identification model.";

    }, 2500);

});