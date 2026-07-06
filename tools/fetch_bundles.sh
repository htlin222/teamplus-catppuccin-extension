#!/usr/bin/env bash
# Download all Team+ CSS bundles needed to regenerate the dark theme.
# Usage: ./tools/fetch_bundles.sh <output-dir>
set -euo pipefail

OUT="${1:-bundles}"
mkdir -p "$OUT"

BASE="https://team.kfsyscc.org"
BUNDLES=(
  BundleOutput/EIM/CSS/MessengerMain.min.css
  BundleOutput/EIM/CSS/comCss.min.css
  BundleOutput/EIM/CSS/ContactMessageFeed.min.css
  BundleOutput/EIM/CSS/DeptNav.min.css
  BundleOutput/EIM/CSS/AvayaCall.min.css
  BundleOutput/EIM/CSS/Base.min.css
  BundleOutput/EIM/CSS/ExternalUserInfoPopup.min.css
  BundleOutput/EIM/CSS/InviteLog.min.css
  BundleOutput/EIM/CSS/MeetingGroup.min.css
  BundleOutput/EIM/CSS/MoreLoadingCSS.min.css
  BundleOutput/EIM/CSS/MsgWallApp.min.css
  BundleOutput/EIM/CSS/StartNoticeBox.min.css
  BundleOutput/EIM/CSS/Tab.min.css
  BundleOutput/EIM/CSS/Team.min.css
  BundleOutput/EIM/CSS/TeamLabelPopup.min.css
  BundleOutput/EIM/CSS/TeamMore.min.css
  BundleOutput/EIM/CSS/User.min.css
  BundleOutput/Js/Plugin/E8DPictureViewerCSS.min.css
  BundleOutput/Js/Plugin/E8DScrollCSS.min.css
  EIM/CSS/Lang_zh-TW.css
  JS/Plugin/NoticeBadge/NoticeBadge.css
)

for path in "${BUNDLES[@]}"; do
  name="$(basename "$path")"
  echo "fetching $name"
  curl -sk "$BASE/$path" -o "$OUT/$name"
done
echo "done: $OUT"
