# Sadâ ses üretici: ses-listesi.json içindeki her cümle için audio/<kod>.mp3 üretir.
# Var olan dosyaları atlar; yarıda kalırsa tekrar çalıştırmak yeterlidir.
import asyncio, json, os, sys
try:
    import edge_tts
except ImportError:
    print("edge-tts yüklü değil. Önce ses_uret.bat dosyasını çalıştırın."); sys.exit(1)

HERE = os.path.dirname(os.path.abspath(__file__))
LISTE = os.path.join(HERE, "ses-listesi.json")
KLASOR = os.path.join(HERE, "audio")
AYNI_ANDA = 4

async def uret(item, sem, sayac, toplam, hatalar):
    yol = os.path.join(KLASOR, item["k"] + ".mp3")
    async with sem:
        for deneme in range(4):
            try:
                await edge_tts.Communicate(item["t"], item["v"], rate="-8%").save(yol + ".tmp")
                os.replace(yol + ".tmp", yol)
                break
            except Exception as e:
                if deneme == 3:
                    hatalar.append(item["k"]); print("  HATA:", item["k"], e)
                await asyncio.sleep(2 + deneme * 3)
        sayac[0] += 1
        if sayac[0] % 25 == 0 or sayac[0] == toplam:
            print(f"  {sayac[0]}/{toplam} hazır")

async def main():
    os.makedirs(KLASOR, exist_ok=True)
    liste = json.load(open(LISTE, encoding="utf-8"))
    eksik = [x for x in liste if not os.path.exists(os.path.join(KLASOR, x["k"] + ".mp3"))]
    print(f"Toplam {len(liste)} ses; üretilecek: {len(eksik)}")
    if not eksik:
        print("Tüm sesler zaten hazır."); return
    sem = asyncio.Semaphore(AYNI_ANDA); sayac = [0]; hatalar = []
    await asyncio.gather(*(uret(x, sem, sayac, len(eksik), hatalar) for x in eksik))
    print("Bitti." if not hatalar else f"Bitti, {len(hatalar)} ses üretilemedi. Dosyayı tekrar çalıştırın.")

asyncio.run(main())
