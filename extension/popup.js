// popup — flavor picker + master toggle, persisted in chrome.storage.local.

const DEFAULTS = { enabled: true, flavor: "mocha" };
const toggle = document.getElementById("toggle");
const buttons = [...document.querySelectorAll(".flavor")];

function render({ enabled, flavor }) {
  toggle.setAttribute("aria-checked", String(enabled));
  document.body.classList.toggle("disabled", !enabled);
  for (const btn of buttons) {
    btn.setAttribute("aria-pressed", String(btn.dataset.flavor === flavor));
  }
}

chrome.storage.local.get(DEFAULTS, render);

toggle.addEventListener("click", () => {
  chrome.storage.local.get(DEFAULTS, ({ enabled, flavor }) => {
    chrome.storage.local.set({ enabled: !enabled });
    render({ enabled: !enabled, flavor });
  });
});

for (const btn of buttons) {
  btn.addEventListener("click", () => {
    chrome.storage.local.get(DEFAULTS, ({ enabled }) => {
      chrome.storage.local.set({ flavor: btn.dataset.flavor, enabled: true });
      render({ enabled: true, flavor: btn.dataset.flavor });
    });
  });
}
