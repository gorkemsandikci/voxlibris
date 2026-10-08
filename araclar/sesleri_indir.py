"""Türkçe Piper seslerini modeller/piper/ altına indirir (sadece stdlib).

    python araclar/sesleri_indir.py              # üç ses
    python araclar/sesleri_indir.py fettah       # tek ses

dfki resmi listede (CC BY-NC-SA 4.0 — ticari olmayan kullanım). fahrettin ve fettah (CC0) resmi listeden kalktı;
Hugging Face'teki eski bir sürümden indirilir.
"""
import sys
import urllib.request
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "modeller" / "piper"
TABAN = "https://huggingface.co/rhasspy/piper-voices/resolve"
SESLER = {
    "dfki": ("main", "CC BY-NC-SA 4.0"),
    "fahrettin": ("6fb8245d6d27fef8988272e0c8e9f5018da1bbbf", "CC0"),
    "fettah": ("6fb8245d6d27fef8988272e0c8e9f5018da1bbbf", "CC0"),
}


def indir(ses: str) -> None:
    surum, lisans = SESLER[ses]
    HEDEF.mkdir(parents=True, exist_ok=True)
    for uzanti in ("onnx.json", "onnx"):
        ad = f"tr_TR-{ses}-medium.{uzanti}"
        yol = HEDEF / ad
        if yol.exists() and yol.stat().st_size > 0:
            continue
        url = f"{TABAN}/{surum}/tr/tr_TR/{ses}/medium/{ad}"
        gecici = yol.with_name(ad + ".tmp")
        print(f"⬇ {ad} …", flush=True)
        with urllib.request.urlopen(url) as cevap, open(gecici, "wb") as f:
            while parca := cevap.read(1 << 20):
                f.write(parca)
        gecici.replace(yol)
    print(f"✅ {ses} ({lisans})")


def main(argv=None) -> int:
    secilen = (argv if argv is not None else sys.argv[1:]) or list(SESLER)
    bilinmeyen = [s for s in secilen if s not in SESLER]
    if bilinmeyen:
        print(f"Bilinmeyen ses: {', '.join(bilinmeyen)} (seçenekler: {', '.join(SESLER)})", file=sys.stderr)
        return 1
    for ses in secilen:
        indir(ses)
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    sys.exit(main())
