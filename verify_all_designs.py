import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

designs = [
    ("design-1-unverkrampft", "UNVERKRAMPFT"),
    ("design-2-kinetiq", "KINETIQ"),
    ("design-3-sanavita", "SANA VITA"),
    ("design-4-auroramed", "AURORA MED"),
    ("design-5-vitalwerk", "VITALWERK")
]

all_passed = True

print("=== STARTING AUDIT OF 5 PHYSIOTHERAPY WEBSITES ===")

for folder, name in designs:
    index_path = os.path.join(folder, "index.html")
    hero_path = os.path.join(folder, "hero.jpg")

    print(f"\n--- Checking {name} ({folder}) ---")

    # 1. Check index.html exists
    if not os.path.exists(index_path):
        print(f"❌ FAIL: {index_path} does not exist!")
        all_passed = False
        continue
    else:
        size = os.path.getsize(index_path)
        print(f"✓ index.html exists (size: {size} bytes)")

    # 2. Check hero.jpg exists
    if not os.path.exists(hero_path):
        print(f"❌ FAIL: {hero_path} does not exist!")
        all_passed = False
    else:
        img_size = os.path.getsize(hero_path)
        print(f"✓ hero.jpg exists (size: {img_size} bytes)")

    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 3. Check floating button
    if 'id="floating-booking-btn"' in html:
        print("✓ Floating booking button found ('id=\"floating-booking-btn\"')")
    else:
        print("❌ FAIL: Floating booking button not found!")
        all_passed = False

    # 4. Check modal panel
    if 'id="booking-widget-panel"' in html:
        print("✓ Modal widget panel found ('id=\"booking-widget-panel\"')")
    else:
        print("❌ FAIL: Modal widget panel not found!")
        all_passed = False

    # 5. Check 5 design switcher buttons in modal
    switcher_links = [
        "design-1-unverkrampft/index.html",
        "design-2-kinetiq/index.html",
        "design-3-sanavita/index.html",
        "design-4-auroramed/index.html",
        "design-5-vitalwerk/index.html"
    ]
    missing_links = []
    for link in switcher_links:
        if link not in html:
            missing_links.append(link)

    if not missing_links:
        print("✓ All 5 design switcher buttons present in modal panel!")
    else:
        print(f"❌ FAIL: Missing switcher links: {missing_links}")
        all_passed = False

    # 6. Check interactive booking placeholder
    if 'id="booking-widget-mount"' in html:
        print("✓ Embeddable 400x500px booking placeholder container found")
    else:
        print("❌ FAIL: Booking placeholder container not found!")
        all_passed = False

    # Special check for Design 1: confirm top booking CTA is removed
    if folder == "design-1-unverkrampft":
        if '<span>Online-Termin</span>' in html:
            print("❌ FAIL: Design 1 still has top nav 'Online-Termin' button!")
            all_passed = False
        else:
            print("✓ Design 1 top nav 'Online-Termin' button successfully removed!")

        if '<button onclick="openBookingModal()" class="bg-terra-500' in html:
            print("❌ FAIL: Design 1 still has hero 'Termin online buchen' button!")
            all_passed = False
        else:
            print("✓ Design 1 hero 'Termin online buchen' button successfully replaced!")

# Check root index.html
print("\n--- Checking Root Hub (index.html) ---")
if os.path.exists("index.html"):
    print("✓ Root index.html exists")
    with open("index.html", "r", encoding="utf-8") as f:
        root_html = f.read()
    for folder, name in designs:
        if f"{folder}/index.html" in root_html:
            print(f"✓ Root links to {name}")
        else:
            print(f"❌ FAIL: Root does not link to {folder}")
            all_passed = False
else:
    print("❌ FAIL: Root index.html not found!")
    all_passed = False

print("\n" + "="*50)
if all_passed:
    print("🎉 ALL AUDIT CHECKS PASSED PERFECTLY!")
else:
    print("⚠️ SOME CHECKS FAILED.")
print("="*50)
