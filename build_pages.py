# Regenerates every tool page, sitemap.xml, robots.txt and the SEO parts of index.html.
# 1) Set BASE to your real site address (must end with "/"), 2) run: python build_pages.py
import html, json, re, os, datetime
BASE = "https://YOUR-USERNAME.github.io/convertly/"
D = os.path.dirname(os.path.abspath(__file__))
E = html.escape
T = [
("p2w","pdf-to-word","PDF to Word Converter","Convert PDF to editable Word (.docx) in your browser. Keeps page size, fonts, colours and text positions. Free, private, no upload.","Turn a PDF into a Word document that looks like the original. Text stays editable and the page graphics are kept as the background.","Will the layout stay the same?","Page size, text position, font size and colour are kept, and images and graphics sit behind the text. Fonts that are not installed on your computer are replaced by a similar one.",0,"PDF"),
("p2x","pdf-to-excel","PDF to Excel Converter","Convert PDF to Excel (.xlsx) online, free. Text lands in cells at the same position with its original font, size and colour. Private, no upload.","Convert each PDF page into an Excel sheet. Text is placed in cells at matching positions with its original font, size and colour.","Does it detect tables?","It mirrors the page layout rather than detecting table structure: each page becomes a sheet, text goes in cells at the same position, and page graphics are the sheet background.",0,"PDF"),
("p2p","pdf-to-powerpoint","PDF to PowerPoint Converter","Convert PDF to PowerPoint (.pptx) online. Every page becomes a slide that looks exactly like the original. Free and private, no upload.","Turn every PDF page into a PowerPoint slide with the exact same look.","Can I edit the text on the slides?","No. Each slide holds the page as a high-quality image, so the look is exact but the text is not editable.",0,"PDF"),
("p2j","pdf-to-jpg","PDF to JPG Converter","Convert PDF pages to JPG images online. Choose the quality, get one image per page. Free, private, nothing is uploaded.","Save every page of a PDF as a JPG image. Multi-page files download as one ZIP.","What quality are the images?","Pages are rendered at high resolution. Pick Standard, High or Small depending on whether you want sharpness or a smaller file.",0,"PDF"),
("j2p","jpg-to-pdf","JPG to PDF Converter","Combine JPG and PNG images into one PDF online. Choose the order, each image becomes a page. Free and private, no upload.","Combine one or more images into a single PDF. Each image becomes a page at its own size, in the order you select.","Which image formats work?","JPG and PNG. Select several files at once and they are added to the PDF in the order selected.",1,"images"),
("pda","pdf-to-pdfa","PDF to PDF/A Converter","Create an archival PDF/A-1b copy of your PDF in the browser. Free and private, no upload. Pages are flattened to images.","Create an archival PDF/A-1b copy of a PDF for long-term storage.","Is the result officially certified PDF/A?","It targets PDF/A-1b by flattening pages and adding the required metadata and colour profile, but it is not formally certified. If compliance matters, check the file with the free veraPDF validator.",0,"PDF"),
("mrg","merge-pdf","Merge PDF Files","Merge PDF files into one online. Choose the order and optionally shrink the result. Free and private, files never leave your device.","Combine several PDFs into one document, in the order you select. Merging is lossless unless you choose to reduce the size.","Does merging reduce quality?","No. By default pages are copied as they are, so the merged file is roughly the combined size of the originals. You can optionally reduce it to a percentage of that size.",1,"PDF files"),
("spl","split-pdf","Split PDF","Split a PDF by page ranges or into single pages online. Free, private, no upload. Download the parts as a ZIP.","Extract pages or ranges from a PDF into separate files.","How do I choose what to split?","Type ranges such as 1-3,4,5-8. Each comma-separated range becomes its own PDF. Leave it blank to split every page.",0,"PDF"),
("cmp","compress-pdf","Compress PDF to a Chosen Size","Reduce PDF file size to the percentage you choose, for example 50 percent. Free, private PDF size reducer, no upload.","Shrink a PDF to a percentage of its original size, for example half. Useful for email limits and upload forms.","Can I choose the final size?","Yes. Pick a percentage of the original size. Pages are re-rendered as images to reach it, so text can no longer be selected, and very small targets may not be reachable.",0,"PDF"),
("rot","rotate-pdf","Rotate PDF Pages","Rotate all or selected PDF pages by 90, 180 or 270 degrees online. Free and private, no upload.","Rotate every page, or just the pages you list, and download the fixed PDF.","Can I rotate only some pages?","Yes. Enter a page range such as 2-4,7 to rotate only those pages, or leave it blank to rotate all of them.",0,"PDF"),
("org","organize-pdf","Organize PDF Pages","Reorder, duplicate or drop PDF pages online by typing the new page order. Free and private, no upload.","Rearrange the pages of a PDF by typing the order you want.","How do I reorder pages?","Type the new order, for example 3,1,2,4-6. Pages can be repeated or left out.",0,"PDF"),
("rem","remove-pdf-pages","Remove Pages from PDF","Delete pages from a PDF online. Type the page numbers to remove and download the result. Free, private, no upload.","Delete unwanted pages from a PDF and download a clean copy.","Does it change my original file?","No. Your original stays untouched. You download a new PDF without the pages you removed.",0,"PDF"),
("num","add-page-numbers-to-pdf","Add Page Numbers to PDF","Add page numbers to a PDF online. Choose left, centre or right and the starting number. Free and private, no upload.","Stamp page numbers on every page of your PDF.","Where are the numbers placed?","At the bottom of each page. You choose left, centre or right, and the number to start from.",0,"PDF"),
("wm","watermark-pdf","Watermark PDF","Add a text watermark to every page of a PDF online. Choose the text and opacity. Free and private, no upload.","Add a diagonal text watermark such as CONFIDENTIAL or DRAFT to every page.","Can I control how visible it is?","Yes. Type your own text and choose Light, Medium or Strong opacity.",0,"PDF"),
("crp","crop-pdf","Crop PDF","Crop PDF margins online by setting top, right, bottom and left trim. Free and private, no upload.","Trim white margins from every page of a PDF.","What unit are the margins in?","Points: 72 points equal one inch. The same trim is applied to every page.",0,"PDF"),
("prt","protect-pdf","Protect PDF with Password","Protect a PDF with a password online so it cannot be opened without it. Free and private, nothing is uploaded.","Encrypt a PDF so a password is required to open it. You can also limit others to printing or viewing only.","Are the pages still selectable text?","No. Pages are re-rendered as images before encryption, so text in the protected copy cannot be selected. Always keep a copy of your password.",0,"PDF"),
("unl","unlock-pdf","Unlock PDF","Remove the password from a PDF you own online. Enter the password and save an unlocked copy. Free and private, no upload.","Save an unlocked copy of a password-protected PDF.","Can it unlock a PDF without the password?","No. You must know the password. Use it only on files you own or have permission to unlock. Pages are saved as images in the unlocked copy.",0,"PDF"),
("sgn","sign-pdf","Sign PDF","Sign a PDF online by drawing your signature and placing it on any page. Free and private, nothing is uploaded.","Draw your signature and place it on a page of your PDF.","Is the signature legally binding?","It places an image of your drawn signature. It is not a certified digital signature, and legal requirements differ by country and document, so ask a legal adviser if it matters.",0,"PDF"),
("imr","reduce-image-size","Reduce Image Size by Percentage","Reduce JPG, PNG or WebP image size to the percentage you choose, for example 50 percent. Free, private, no upload.","Shrink one or many images to a percentage of their original file size.","How does the percentage work?","It aims for a file that is that percentage of the original by lowering JPEG quality and, if needed, the image dimensions. PNG and WebP files are saved as JPG.",1,"images"),
]
idx_p = os.path.join(D, "index.html"); idx = open(idx_p, encoding="utf-8").read()
libs = "\n".join(re.findall(r'<script src="[^"]+"></script>', idx))
ICON = '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 100 100%27%3E%3Ctext y=%27.9em%27 font-size=%2790%27%3E📄%3C/text%3E%3C/svg%3E">'
NAV = '<div class="tools"><span id="sw"></span><button id="tm" aria-label="Switch light or dark theme">🌓</button></div>'
def links(skip=None):
    return "".join(f'<li><a href="{t[1]}.html">{E(t[2])}</a></li>' for t in T if t[0] != skip)
def seo(title, desc, url, ld):
    return (f'<title>{E(title)}</title>\n<meta name="description" content="{E(desc)}">\n<link rel="canonical" href="{url}">\n'
            f'<meta property="og:type" content="website"><meta property="og:site_name" content="Convertly"><meta property="og:title" content="{E(title)}">'
            f'<meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary">\n'
            f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')
for t in T:
    i, slug, h1, desc, intro, q, a, multi, ft = t
    url = f"{BASE}{slug}.html"; title = f"{h1} - Free & Private | Convertly"
    faqs = [(q, a), ("Are my files uploaded to a server?", "No. Everything runs inside your browser, so your files never leave your device."), ("Is it free?", "Yes. There is no sign-up and no limit on how many files you process.")]
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "SoftwareApplication", "name": h1, "url": url, "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any (web browser)", "description": desc, "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": x, "acceptedAnswer": {"@type": "Answer", "text": y}} for x, y in faqs]}]}
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{seo(title, desc, url, ld)}
{ICON}
<link rel="stylesheet" href="style.css">
</head><body class="tp" data-tool="{i}">
<header><nav class="bar"><a class="brand" href="index.html">Convertly</a>{NAV}</nav><section class="hero"><h1>{E(h1)}</h1><p>{E(intro)}</p></section></header>
<div id="ov"><div id="pn"></div></div>
<main id="m"></main>
<section class="doc"><h2>How to use it</h2><ol><li>Choose your {ft} with the file picker above.</li><li>Adjust the options if the tool has any.</li><li>Click the button. The result downloads straight away and nothing is uploaded.</li></ol>
<h2>Frequently asked questions</h2>{"".join(f"<details><summary>{E(x)}</summary><p>{E(y)}</p></details>" for x, y in faqs)}
<h2>More free tools</h2><ul class="links">{links(i)}</ul></section>
<footer>Private by design: no uploads, no accounts. <a href="index.html">All Convertly tools</a></footer>
{libs}
</body></html>
'''
    open(os.path.join(D, slug + ".html"), "w", encoding="utf-8").write(page)
# ---- index.html: SEO head block + static tool links ----
it = "Free Online PDF Tools: Convert, Merge, Compress | Convertly"
idesc = "Free PDF tools that run in your browser: PDF to Word, Excel, JPG, merge, split, compress to a chosen size, sign and protect. No upload, no sign-up."
iseo = seo(it, idesc, BASE, {"@context": "https://schema.org", "@type": "WebSite", "name": "Convertly", "url": BASE, "description": idesc})
idx = re.sub(r"<title>.*?</title>\s*", "", idx, flags=re.S)
idx = re.sub(r'<meta name="description"[^>]*>\s*', "", idx)
if "<!--SEO-->" not in idx: idx = idx.replace('<link rel="stylesheet" href="style.css">', "<!--SEO--><!--/SEO-->\n" + '<link rel="stylesheet" href="style.css">', 1)
idx = re.sub(r"<!--SEO-->.*?<!--/SEO-->", lambda m: "<!--SEO-->\n" + iseo + "\n<!--/SEO-->", idx, flags=re.S)
if "<!--TOOLS-->" not in idx: idx = idx.replace("<footer>", "<!--TOOLS--><!--/TOOLS-->\n<footer>", 1)
blk = f'<section class="doc"><h2>All PDF and image tools</h2><ul class="links">{links()}</ul><h2>Free, private and fast</h2><p>Convertly runs entirely in your browser. Your PDFs and images are processed on your own device and are never uploaded, so there is nothing to sign up for and nothing stored on a server.</p></section>'
idx = re.sub(r"<!--TOOLS-->.*?<!--/TOOLS-->", lambda m: "<!--TOOLS-->\n" + blk + "\n<!--/TOOLS-->", idx, flags=re.S)
idx = idx.replace("<h1>PDF Tools</h1>", "<h1>Free Online PDF Tools</h1>")
open(idx_p, "w", encoding="utf-8").write(idx)
today = datetime.date.today().isoformat()
urls = [BASE] + [f"{BASE}{t[1]}.html" for t in T]
open(os.path.join(D, "sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(D, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
print("Built", len(T), "tool pages + index, sitemap.xml, robots.txt for", BASE)
