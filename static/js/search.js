
function wireAllEventListeners() {
    const cancelButton = document.getElementById("cancel-search")
    const searchButton = document.getElementById("open-search")
    searchButton.addEventListener("click", () => {
        document.getElementById("home").style.display = "none"
        document.getElementById("search-panel").style.display = "block"
    })
    cancelButton.addEventListener("click", () => {
        document.getElementById("search-panel").style.display = "none"
        document.getElementById("home").style.display = "block"
    })

}

window.onload = () => {
  wireAllEventListeners()
}
