const loading = document.getElementById("loading");
const loadingPyscript = document.getElementById("loading-pyscript");
const loadingSetup = document.getElementById("loading-setup");

addEventListener("py:ready", () => {
        loading.childNodes.forEach((it) => it.hidden = true);
        loadingSetup.hidden = false;
});

loadingPyscript.hidden = false;
loading.showModal();
