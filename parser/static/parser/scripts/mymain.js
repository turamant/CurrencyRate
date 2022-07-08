const imgElement = document.querySelector("#my_image");
imgElement.addEventListener("mouseover", hovered, false);
imgElement.addEventListener("mouseout", hoveredOut, false);
function hovered(e) {
imgElement.setAttribute("width", "300");
}
function hoveredOut(e) {
imgElement.setAttribute("width", "200");
}