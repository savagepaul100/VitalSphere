import os

path = r"C:\Users\PAUL\Documents\VitalSphere\public\index.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Tab buttons: "Donors" and "Recipients"
old_tabs = '''          <div class="tab-switch">
            <button class="tab-btn active" id="btnTabDonors" onclick="switchDirectoryTab('donors')">Donors (<span id="tabDonorsCount">256</span>)</button>
            <button class="tab-btn" id="btnTabRecipients" onclick="switchDirectoryTab('recipients')">Recipients Who Want Blood (<span id="tabRecipientsCount">64</span>)</button>
          </div>'''

new_tabs = '''          <div class="tab-switch">
            <button class="tab-btn active" id="btnTabDonors" onclick="switchDirectoryTab('donors')">Donors</button>
            <button class="tab-btn" id="btnTabRecipients" onclick="switchDirectoryTab('recipients')">Recipients</button>
          </div>'''

if old_tabs in content:
    content = content.replace(old_tabs, new_tabs, 1)
    print("Replaced tab buttons with clean Donors and Recipients")
else:
    # Try alternate if span was different
    old_tabs_alt = '''            <button class="tab-btn active" id="btnTabDonors" onclick="switchDirectoryTab('donors')">Donors</button>'''
    if old_tabs_alt not in content:
        print("Warning: old_tabs not found")

# 2. Update Hero Stats: replace hardcoded 256 and 32 with dynamic spans
old_hero_stats = '''      <div class="stat-card">
        <div class="stat-number">256</div>
        <div class="stat-label">ENROLLED DONORS</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">32</div>
        <div class="stat-label">ACTIVE PATIENT REQUESTS</div>
      </div>'''

new_hero_stats = '''      <div class="stat-card">
        <div class="stat-number" id="heroDonorCount">256</div>
        <div class="stat-label">ENROLLED DONORS</div>
      </div>
      <div class="stat-card">
        <div class="stat-number" id="heroRecipientCount">64</div>
        <div class="stat-label">ACTIVE PATIENT REQUESTS</div>
      </div>'''

if old_hero_stats in content:
    content = content.replace(old_hero_stats, new_hero_stats, 1)
    print("Updated hero stat numbers with dynamic IDs")
else:
    print("Warning: old_hero_stats not found")

# 3. Add updateHeroStatsCounters() function in script
old_update_badge = '    window.updateNotificationBadge = function() {'
new_update_stats = '''    window.updateHeroStatsCounters = function() {
      const dEl = document.getElementById('heroDonorCount');
      if (dEl && window.fullDonorsList) dEl.innerText = window.fullDonorsList.length;
      const rEl = document.getElementById('heroRecipientCount');
      if (rEl && window.fullRecipientsList) rEl.innerText = window.fullRecipientsList.length;
      const navBtn = document.querySelector('#navAuthArea button');
      if (navBtn && window.fullDonorsList) navBtn.innerText = `View ${window.fullDonorsList.length} Donors`;
    };

    window.updateNotificationBadge = function() {'''

if old_update_badge in content:
    content = content.replace(old_update_badge, new_update_stats, 1)
    print("Added updateHeroStatsCounters function")
else:
    print("Warning: old_update_badge not found")

# 4. Call updateHeroStatsCounters in DOMContentLoaded
old_dom_load = '''      initPanIndiaSelectors();
      updateNotificationBadge();'''

new_dom_load = '''      initPanIndiaSelectors();
      updateNotificationBadge();
      updateHeroStatsCounters();'''

if old_dom_load in content:
    content = content.replace(old_dom_load, new_dom_load, 1)
    print("Called updateHeroStatsCounters on DOMContentLoaded")
else:
    print("Warning: old_dom_load not found")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("update_desktop_tabs_and_stats.py completed successfully")
