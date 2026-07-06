// catppuccin-teamplus service worker — keeps the toolbar badge in sync.

function updateBadge(enabled) {
  chrome.action.setBadgeText({ text: enabled ? "" : "OFF" });
  chrome.action.setBadgeBackgroundColor({ color: "#6c7086" });
}

chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.get({ enabled: true }, ({ enabled }) => updateBadge(enabled));
});

chrome.storage.onChanged.addListener((changes, area) => {
  if (area === "local" && changes.enabled) {
    updateBadge(changes.enabled.newValue);
  }
});
