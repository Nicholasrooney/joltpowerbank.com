import os, io, json, re
from PIL import Image, ImageOps, ImageFilter
import cairosvg
try: import pillow_avif
except: pass

# file -> (venue name as in the sheet, mode)   mode: logo | photo | dark (light logo needing dark tile)
MAP = {
 "150x150.webp": ("Tesco Express Temple Bar", "logo"),
 "157f6ef3c7383b88298913a25a10da2fede6c529.jpg": ("Temple Bar Hotel Dublin", "photo"),
 "299404332.jpg": ("The Lombard", "photo"),
 "313533885.jpg": ("The Gibson Hotel", "photo"),
 "408853765_7789344124425482_1323782974158944186_n.webp": ("Pawn Shop", "photo"),
 "484858594_1069132701922707_1429655594557082151_n-1024x1024.webp": ("Pygmalion", "photo"),
 "52.jpg": ("J. T. Pim's", "photo"),
 "BX-client-logo-37DawsonSt.png": ("37 Dawson Street", "logo"),
 "CUH-logo-300x192.png": ("Cork University Hospital A&E", "logo"),
 "Copper_face_Jacks_logo.jpg": ("Copper Face Jacks", "logo"),
 "DISNDAT-LOGO-WHITEI.png": ("Disndat", "dark"),
 "Dublin-42-Doheny_&_Nesbitt-1993-gje.jpg": ("Doheny & Nesbitt", "photo"),
 "IMG_2682.jpg": ("Gibney's Of Malahide, Ireland", "photo"),
 "IMG_9969.webp": ("The Harbour Bar", "photo"),
 "JDBS_01_Green_sRGB-2-771x1024.webp": ("Jameson Distillery Bow St.", "logo"),
 "Keoghs-LG.png": ("The Stags Head", "logo"),
 "OREILLYSLOGO2021 copy.avif": ("O'Reilly's bar", "dark"),
 "QwRY54Li1HMwD7oNfpG6hwmV4Wp5TBbX6CaqE3T3Go.webp": ("Dicey's Garden", "photo"),
 "Royal_Dublin_Society.png": ("RDS", "logo"),
 "St-James-Logo.jpeg": ("St James's Hospital A&E", "logo"),
 "StVincents-UCD-1024x319.jpg": ("St Vincent's University Hospital", "logo"),
 "Untitled+design+(11).webp": ("Tapped Late Bar", "logo"),
 "Untitled-design.jpg": ("The Gleneagle Hotel & Apartments", "logo"),
 "__page__screenshot_2025-01-31_at_00.16.44.png": ("O'Donoghues Bar Dublin", "photo"),
 "alfies-1.jpeg": ("Alfies Restaurant & Cocktail Bar", "photo"),
 "brand-footer.png": ("The Quays Dublin - Temple Bar", "logo"),
 "caption.jpg": ("Merchants Quay Shopping Centre (ground floor)", "photo"),
 "clayton-hotel-ballsbridge-logo.jpg": ("Clayton Hotel Ballsbridge", "logo"),
 "cropped-IMG_6425-1.webp": ("Searsons", "logo"),
 "devitts_logo_new.png": ("Devitts Pub", "dark"),
 "flannerys-bar-63232828999584.42873189.png": ("Flannery's Bar", "photo"),
 "gleeson-fresh-food-cream.webp": ("Gleeson's", "dark"),
 "harcourt-logo.svg": ("Harcourt Hotel", "dark"),
 "images (1).jpg": ("The Galway Hooker Bar", "logo"),
 "images (1).png": ("Clayton Hotel Liffey Valley", "logo"),
 "images (10).jpg": ("Café en Seine", "photo"),
 "images (2).jpg": ("The Quays Bar and Restaurant Galway", "photo"),
 "images (3).jpg": ("The Old Storehouse Bar and Restaurant", "photo"),
 "images (4).jpg": ("Wexford General Hospital A&E", "photo"),
 "images (5).jpg": ("The Workman's Club", "logo"),
 "images (6).jpg": ("Portiuncula University Hospital - Emergency Department", "photo"),
 "images (7).jpg": ("McDonnell's Bar & Beer Garden", "logo"),
 "images (8).jpg": ("The Sallynoggin Inn", "photo"),
 "images (9).jpg": ("Dublin Zoo Front Entrance", "photo"),
 "images.jpg": ("Beaumont Hospital", "logo"),
 "images.png": ("The George", "logo"),
 "jr-mahons-signage.jpg": ("J.R. Mahon’s Public House & Brewery", "photo"),
 "kehoes+front1.webp": ("Kehoes Pub", "photo"),
 "logo-7.jpg": ("Our Lady's Hospital", "logo"),
 "main-header-logo.svg": ("The Norseman", "logo"),
 "main-header-logo2.webp": ("The Auld Dubliner", "dark"),
 "martello_outside.jpeg": ("The Martello Hotel", "photo"),
 "nmh.png": ("The National Maternity Hospital", "logo"),
 "rn-image_picker_lib_temp_16c52bf3-4137-4ec9-ba57-0ac71059b87d.webp": ("Connolly Hospital A+E Department", "logo"),
 "shelbourne-park-2024-2-line-logo.png": ("Shelbourne Park Greyhound Stadium", "dark"),
 "slatteryw.png": ("Slattery's", "dark"),
 "whelans-logo-black-new.png": ("Whelan's", "logo"),
 "white-text-600x56.png": ("Lemon & Duke", "dark"),
}
# images (1).png is Liffey Valley shopping centre's logo -> attach to the Liffey Valley food court entry instead
MAP["images (1).png"] = ("Foodcourt Liffey Valley", "logo")

W, H = 360, 200
os.makedirs("out", exist_ok=True)
def load(f):
    p = "src/" + f
    if f.endswith(".svg"):
        return Image.open(io.BytesIO(cairosvg.svg2png(url=p, output_width=900))).convert("RGBA")
    return Image.open(p).convert("RGBA")

def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]

def bg_of(im):
    px = [im.getpixel(p) for p in [(2,2),(im.width-3,2),(2,im.height-3),(im.width-3,im.height-3)]]
    if all(a < 20 for *_, a in px): return None          # transparent background
    r = sum(p[0] for p in px)//4; g = sum(p[1] for p in px)//4; b = sum(p[2] for p in px)//4
    return (r, g, b)

result = {}
for f, (venue, mode) in MAP.items():
    im = load(f)
    if mode == "photo":
        tile = ImageOps.fit(im.convert("RGB"), (W, H), Image.LANCZOS, centering=(0.5, 0.45))
    else:
        bbox = im.getchannel("A").point(lambda a: 255 if a > 10 else 0).getbbox() or (0,0,im.width,im.height)
        im = im.crop(bbox)
        bg = bg_of(im)
        if bg is not None:   # solid background: trim to where the logo actually is
            from PIL import ImageChops
            rgb = im.convert("RGB"); diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, bg)).convert("L").point(lambda v: 255 if v > 38 else 0)
            bb = diff.getbbox()
            if bb:
                pad = 6; im = im.crop((max(0,bb[0]-pad), max(0,bb[1]-pad), min(im.width,bb[2]+pad), min(im.height,bb[3]+pad)))
        if mode == "dark": bg = (18, 22, 18)
        elif bg is None: bg = (255, 255, 255)
        tile = Image.new("RGB", (W, H), bg)
        lim = im.copy(); lim.thumbnail((int(W*0.78), int(H*0.72)), Image.LANCZOS)
        tile.paste(lim, ((W-lim.width)//2, (H-lim.height)//2), lim)
    name = slug(venue) + ".webp"
    tile.save("out/" + name, "WEBP", quality=84, method=6)
    result[venue] = name
json.dump(result, open("logo_map.json", "w"), indent=1)
print(len(result))
