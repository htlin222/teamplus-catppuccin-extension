// catppuccin-teamplus content script — injects the selected flavor stylesheet
// based on chrome.storage.local {enabled, flavor}.

const LINK_ID = "ctp-theme";
const FLAVORS = ["latte", "frappe", "macchiato", "mocha"];
const DEFAULTS = { enabled: true, flavor: "mocha" };

function applyTheme(flavor) {
  if (!FLAVORS.includes(flavor)) flavor = DEFAULTS.flavor;
  let link = document.getElementById(LINK_ID);
  if (!link) {
    link = document.createElement("link");
    link.id = LINK_ID;
    link.rel = "stylesheet";
    (document.head || document.documentElement).appendChild(link);
  }
  link.href = chrome.runtime.getURL(`css/theme-${flavor}.css`);
  moveToEnd();
}

function removeTheme() {
  document.getElementById(LINK_ID)?.remove();
}

// 原站規則多帶 !important，同權重時以文件順序決勝，
// 所以載入完成後要把我們的樣式表移到所有原站 CSS 之後。
function moveToEnd() {
  const move = () => {
    const link = document.getElementById(LINK_ID);
    if (link) document.documentElement.appendChild(link);
  };
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", move, { once: true });
  } else {
    move();
  }
}

function sync() {
  chrome.storage.local.get(DEFAULTS, ({ enabled, flavor }) => {
    enabled ? applyTheme(flavor) : removeTheme();
  });
}

sync();

chrome.storage.onChanged.addListener((changes, area) => {
  if (area === "local" && (changes.enabled || changes.flavor)) sync();
});
