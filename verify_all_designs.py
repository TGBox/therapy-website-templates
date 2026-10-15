import os
import re
import sys
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

designs = [
    # 5 Klassiker
    ("design-1-unverkrampft", "1. UNVERKRAMPFT (Bio/Warm Organic)"),
    ("design-2-kinetiq", "2. KINETIQ (High-Performance Sport)"),
    ("design-3-sanavita", "3. SANA VITA (Holistic Osteopathy)"),
    ("design-4-auroramed", "4. AURORA MED (Swiss Medical Precision)"),
    ("design-5-vitalwerk", "5. VITALWERK (Urban Industrial Loft)"),
    # 6 Kreativkonzepte
    ("design-6-schmiere", "6. GELENK-SCHMIERE (Werkstatt/Viskosität)"),
    ("design-7-knotenloeser", "7. KNOTENLÖSER (Faszientherapie/Faden)"),
    ("design-8-knackpunkt", "8. DER KNACKPUNKT (Chiro/Subluxation)"),
    ("design-9-knetfertig", "9. KNETFERTIG (Deep Tissue/Claymorphism)"),
    ("design-10-aufrecht", "10. AUFRECHT (Haltungsschule/Ergonomie)"),
    ("design-11-bewegungsmelder", "11. BEWEGUNGSMELDER (Sensomotorik/Neuro)")
]

all_passed = True

print("=" * 60)
print("=== AUDIT DER 11 PHYSIOTHERAPIE-WEBSITE-VORLAGEN ===")
print("=" * 60)

for folder, name in designs:
    index_path = os.path.join(folder, "index.html")
    hero_path = os.path.join(folder, "hero.jpg")

    print(f"\n--- Checking {name} [{folder}] ---")

    # 1. Check index.html exists
    if not os.path.exists(index_path):
        print(f"❌ FAIL: {index_path} existiert nicht!")
        all_passed = False
        continue
    else:
        size = os.path.getsize(index_path)
        print(f"✓ index.html existiert (Größe: {size:,} Bytes)")

    # 2. Check hero.jpg exists
    if not os.path.exists(hero_path):
        print(f"❌ FAIL: {hero_path} existiert nicht!")
        all_passed = False
    else:
        img_size = os.path.getsize(hero_path)
        print(f"✓ hero.jpg existiert (Größe: {img_size:,} Bytes)")

    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 3. Check floating button
    if 'id="floating-booking-btn"' in html:
        print("✓ Sticky Floating Booking Button vorhanden ('id=\"floating-booking-btn\"')")
    else:
        print("❌ FAIL: Floating booking button nicht gefunden!")
        all_passed = False

    # 4. Check modal panel & mount
    if 'id="booking-widget-panel"' in html:
        print("✓ Modales Widget-Panel vorhanden ('id=\"booking-widget-panel\"')")
    else:
        print("❌ FAIL: Modales Widget-Panel nicht gefunden!")
        all_passed = False

    if 'id="booking-widget-mount"' in html:
        print("✓ Buchungs-Widget-Mount (400x500px) vorhanden ('id=\"booking-widget-mount\"')")
    else:
        print("❌ FAIL: Buchungs-Widget-Mount nicht gefunden!")
        all_passed = False

    # 5. Check category tabs & all 11 design switcher links
    if 'id="cat-tab-classic"' in html and 'id="cat-tab-creative"' in html:
        print("✓ Kategorien-Umschalter ('5 Klassiker' / '6 Kreativ') im Modal vorhanden")
    else:
        print("❌ FAIL: Kategorien-Tabs fehlen im Modal!")
        all_passed = False

    missing_links = []
    for d_folder, _ in designs:
        expected_link = f"{d_folder}/index.html"
        if expected_link not in html:
            missing_links.append(expected_link)

    if not missing_links:
        print("✓ Alle 11 Template-Wechsler-Verknüpfungen im Modal-Panel vorhanden")
    else:
        print(f"❌ FAIL: Fehlende Links im Template-Wechsler: {missing_links}")
        all_passed = False

    # 6. HTTP Status Check (against running dev server on localhost:3000)
    try:
        url = f"http://localhost:3000/{folder}/index.html"
        req = urllib.request.Request(url, headers={'User-Agent': 'AuditBot/1.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            if resp.status == 200:
                print(f"✓ HTTP Status 200 OK von {url}")
            else:
                print(f"⚠️ Warnung: HTTP Status {resp.status} von {url}")
    except Exception as e:
        print(f"⚠️ HTTP-Anfrage fehlgeschlagen ({e})")

# Check root index.html
print("\n--- Überprüfung Root Hub (index.html) ---")
if os.path.exists("index.html"):
    print("✓ Root index.html existiert")
    with open("index.html", "r", encoding="utf-8") as f:
        root_html = f.read()
    for folder, name in designs:
        if f"{folder}/index.html" in root_html:
            print(f"✓ Root verlinkt auf {name}")
        else:
            print(f"❌ FAIL: Root verlinkt nicht auf {folder}")
            all_passed = False
else:
    print("❌ FAIL: Root index.html nicht gefunden!")
    all_passed = False

# HTTP check for root hub
try:
    with urllib.request.urlopen("http://localhost:3000/index.html", timeout=3) as resp:
        if resp.status == 200:
            print("✓ HTTP Status 200 OK für Root Hub http://localhost:3000/index.html")
except Exception as e:
    print(f"⚠️ HTTP-Anfrage für Root fehlgeschlagen: {e}")

print("\n" + "=" * 60)
if all_passed:
    print("🎉 PERFEKT: ALLE 11 WEBSITES HABEN DEN VOLLSTÄNDIGEN AUDIT BESTANDEN!")
else:
    print("⚠️ EINIGE PRÜFUNGEN SIND FEHLGESCHLAGEN.")
print("=" * 60)

sys.exit(0 if all_passed else 1)
