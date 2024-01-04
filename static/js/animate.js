const timer = 700;
let animation = document.getElementById("animation-section");
let a = animation.childNodes;
let current_animated_div, current_animated_div_2;
while (true) {
    // Wait for timer milliseconds
    current_animated_div = a[Math.floor(Math.random() * a.length)];
    current_animated_div.classList += "hover";
    await new Promise((r) => setTimeout(r, timer));
    current_animated_div.classList -= "hover";
    console.log("displatched");
}
