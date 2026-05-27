import os
import re
import shutil
import subprocess
import sys
import math
import traceback
import hashlib
import time
from typing import List, Optional
from collections import Counter

# ==================== نصب خودکار پیش‌نیازها ====================

def install_dependencies():
    # دیگر نیازی به نصب در زمان اجرا نداریم. 
    # تمام کتابخانه‌ها توسط PyInstaller بسته‌بندی شده‌اند.
    print("Dependencies are pre-packaged.")
# ==================== Imports ====================

import uvicorn
from fastapi import FastAPI, Form, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors as pdf_colors
import ezdxf
from shapely.geometry import LineString, Polygon, box, Point
from shapely.ops import unary_union, polygonize
from shapely import affinity
import arabic_reshaper
from bidi.algorithm import get_display

# ==================== CONFIG ====================

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

for d in [OUTPUT_DIR, STATIC_DIR, TEMPLATES_DIR]:
    os.makedirs(d, exist_ok=True)

app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ==================== ODA FILE CONVERTER PATH ====================

ODA_CONVERTER_PATH = r"C:\Program Files\ODA\ODAFileConverter 27.1.0\ODAFileConverter.exe"

# ==================== FONT & TRANSLATIONS ====================

FONT_NAME = "Vazir"
FONT_PATH = os.path.join(BASE_DIR, "Vazir.ttf")
try:
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))
    USED_FONT = FONT_NAME
except:
    USED_FONT = "Helvetica"

TRANSLATIONS = {
    "fa": {
        "header": "پلان چیدمان گرمایش کف برقی تاپسان",
        "info": "مشتری: {n} | کد: {c} | فضا: {r} | ابعاد: {w}x{l} متر | مساحت: {a} مترمربع | فاصله فیلم‌ها: {gap} سانتی متر ",
        "approval_1": "پلان چیدمان گرمایش کف برقی تاپسان مطابق با ابعاد اعلامی کارفرما آقا/خانم ......................................... مورد تایید بوده و لذا درخواست آماده سازی و تولید محصولات طبق پلان",
        "approval_2": " ارائه شده فوق را از شرکت تاپسان هیتینگ دارم. ",
        "sign_name": "نام و نام خانوادگی و امضای تایید‌کننده:",
        "sign_pos": "سمت تایید‌کننده:",
        "changes": "نیاز به تغییرات در ابعاد و پلان وجود دارد.",
        "date": "تاریخ تایید پلان چیدمان:",
        "bom_title": "جدول متره و برآورد تجهیزات (BOM)",
        "bom_row": "ردیف",
        "bom_desc": "شرح کالا",
        "bom_qty": "تعداد",
        "bom_unit": "واحد",
        "bom_total": "مقدار کل",
        "grand_total": "مجموع کل متراژ فیلم‌ها",
        "thermostat": "ترموستات دمای کف مخصوص تاپسان",
        "cp_single": "تابلو فرمان",
        "cp_multi": "تابلو فرمان مرکزی"
    }
}

# ==================== HELPERS ====================

def f_t(text, lang="fa"):
    if lang == "fa":
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    return text

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    return re.sub(r'[\s_-]+', '-', text)

def generate_customer_id(name, phone):
    raw = f"{name}{phone}"
    h = hashlib.md5(raw.encode()).hexdigest().upper()
    return f"TS-{name[0].upper() if name else 'X'}{h[:4]}"

def get_unique_filename(folder, base, ext):
    path = os.path.join(folder, f"{base}.{ext}")
    if not os.path.exists(path): return f"{base}.{ext}"
    count = 1
    while os.path.exists(os.path.join(folder, f"{base}_{count}.{ext}")): count += 1
    return f"{base}_{count}.{ext}"

def is_valid_heating_room(name: str, area: float, width: float, length: float) -> bool:
    name_clean = str(name or "").lower().strip().replace("ي", "ی").replace("ك", "ک")
    no_heat_keywords = ["سرویس", "حمام", "دستشویی", "wc", "bath", "toilet", "تراس", "بالکن", "terrace", "balcony", "پاسیو", "نورگیر"]
    if any(k in name_clean for k in no_heat_keywords): return False
    if area < 6.0: return False
    min_dim = min(width, length)
    if 0.40 <= min_dim <= 0.95:
        return False
    return True

# ==================== CONVERT DWG TO DXF ====================

def convert_dwg_to_dxf(dwg_path: str) -> str:
    """
    تبدیل DWG به DXF با ODA File Converter
    """

    try:
        import os
        import subprocess
        import time
        import traceback

        if not os.path.exists(dwg_path):
            print("❌ DWG file not found")
            return None

        input_dir = os.path.dirname(dwg_path)
        filename = os.path.basename(dwg_path)

        base_name = os.path.splitext(filename)[0]

        output_dir = os.path.join(input_dir, "converted")

        os.makedirs(output_dir, exist_ok=True)

        dxf_path = os.path.join(output_dir, base_name + ".dxf")

        # حذف فایل قبلی
        if os.path.exists(dxf_path):
            try:
                os.remove(dxf_path)
            except:
                pass

        print("\n================ DWG CONVERSION ================")
        print(f"INPUT DIR : {input_dir}")
        print(f"OUTPUT DIR: {output_dir}")
        print(f"FILE      : {filename}")

        # دستور صحیح ODA
        cmd = [
            ODA_CONVERTER_PATH,
            input_dir,          # input folder
            output_dir,         # output folder
            "ACAD2018",         # version
            "DXF",              # output format
            "0",                # recursive
            "1",                # audit
            filename            # file filter
        ]

        print("RUNNING CMD:")
        print(" ".join(cmd))

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180,
            encoding='utf-8',
            errors='ignore'
        )

        print("\nSTDOUT:")
        print(result.stdout)

        print("\nSTDERR:")
        print(result.stderr)

        # کمی صبر برای write شدن فایل
        time.sleep(2)

        # جستجوی DXF
        if os.path.exists(dxf_path):

            size_kb = os.path.getsize(dxf_path) / 1024

            if size_kb > 5:
                print(f"\n✅ DXF CREATED SUCCESSFULLY")
                print(f"SIZE: {size_kb:.1f} KB")

                return dxf_path

        # fallback search
        for f in os.listdir(output_dir):
            if f.lower().endswith(".dxf"):

                full = os.path.join(output_dir, f)

                if os.path.getsize(full) > 5000:
                    print(f"\n✅ FOUND DXF: {f}")
                    return full

        print("\n❌ DXF NOT CREATED")
        return None

    except Exception as e:
        print(f"\n❌ DWG Conversion Error: {e}")
        traceback.print_exc()
        return None
# ==================== GENERATE ADAPTIVE LAYOUT ====================

def generate_adaptive_layout(room_poly, room_name="", doors=None):
    try:
        import math
        from shapely.geometry import LineString, Point, box
        from shapely import affinity

        if doors is None: doors = []

        MAIN_WIDTH = 0.80
        COMP_WIDTH = 0.40
        SMART_GAP = 0.15
        MARGIN = 0.18
        MIN_LENGTH = 0.7

        if not room_poly.is_valid:
            room_poly = room_poly.buffer(0)

        ext_coords = list(room_poly.exterior.coords)
        walls = [LineString([ext_coords[i], ext_coords[i+1]]) for i in range(len(ext_coords)-1)]

        if doors:
            valid_doors = [d for d in doors if hasattr(d, 'distance')]
            target_wall = min(walls, key=lambda w: min(w.distance(d) for d in valid_doors)) if valid_doors else max(walls, key=lambda w: w.length)
        else:
            target_wall = max(walls, key=lambda w: w.length)

        coords = list(target_wall.coords)
        x1, y1 = coords[0]
        x2, y2 = coords[-1]

        angle_rad = math.atan2(y2 - y1, x2 - x1)
        angle_deg = math.degrees(angle_rad)

        p1 = Point(x1, y1)
        p2 = Point(x2, y2)
        anchor_pt = min([p1, p2], key=lambda p: min(p.distance(d) for d in doors) if doors else (p.y, p.x))

        aligned_poly = affinity.translate(room_poly, -anchor_pt.x, -anchor_pt.y)
        aligned_poly = affinity.rotate(aligned_poly, -angle_deg, origin=(0, 0))

        minx, miny, maxx, maxy = aligned_poly.bounds

        final_strips = []
        curr_x = minx + MARGIN / 2

        while curr_x + COMP_WIDTH <= maxx - MARGIN:
            placed_in_row = False
            for width in [MAIN_WIDTH, COMP_WIDTH]:
                if curr_x + width > maxx - MARGIN: continue
                mid_x = curr_x + width / 2
                scan_line = LineString([(mid_x, miny - 2), (mid_x, maxy + 2)])
                inter = scan_line.intersection(aligned_poly.buffer(-0.03))
                if inter.is_empty: continue
                segments = [inter] if inter.geom_type == 'LineString' else list(inter.geoms) if hasattr(inter, 'geoms') else []
                for part in segments:
                    if part.geom_type != 'LineString': continue
                    bx_min, by_min, bx_max, by_max = part.bounds
                    length = round((by_max - by_min) - (2 * MARGIN), 2)
                    if length >= MIN_LENGTH:
                        mid_y = (by_min + by_max) / 2
                        film_box = box(mid_x - width/2, mid_y - length/2, mid_x + width/2, mid_y + length/2)
                        final_geom = affinity.rotate(film_box, angle_deg, origin=(0, 0))
                        final_geom = affinity.translate(final_geom, anchor_pt.x, anchor_pt.y)
                        final_strips.append({
                            'geometry': final_geom, 'geom': final_geom,
                            'width': width, 'length': length, 'gap': SMART_GAP, 'angle': angle_deg
                        })
                if final_strips and final_strips[-1]['width'] == width:
                    curr_x += (width + SMART_GAP)
                    placed_in_row = True
                    break
            if not placed_in_row:
                curr_x += 0.05

        print(f"DEBUG: Generated {len(final_strips)} strips for {room_name}")
        return final_strips

    except Exception as e:
        print(f"Error in generate_adaptive_layout ({room_name}): {e}")
        traceback.print_exc()
        return []

# ==================== EXTRACT ROOMS AND DOORS ====================

def extract_rooms_and_doors(filepath):
    try:
        doc = ezdxf.readfile(filepath)
        msp = doc.modelspace()
        all_edges, door_elements, obstacle_geoms = [], [], []

        def process_entity(e):
            t = e.dxftype()
            layer = getattr(e.dxf, 'layer', '').lower()
            color = getattr(e.dxf, 'color', 0)
            is_obstacle = (color == 1) or any(k in layer for k in ["obstacle", "furniture", "column", "جزیره", "ستون", "cabinet", "کابینت"])

            pts = []
            if t in ("LWPOLYLINE", "POLYLINE"):
                pts = [(float(p[0]), float(p[1])) for p in e.get_points()]
            elif t == "LINE":
                pts = [(e.dxf.start.x, e.dxf.start.y), (e.dxf.end.x, e.dxf.end.y)]

            if len(pts) >= 2:
                ls = LineString(pts)
                if is_obstacle:
                    if len(pts) > 2 and abs(pts[0][0]-pts[-1][0]) < 0.01 and abs(pts[0][1]-pts[-1][1]) < 0.01:
                        obstacle_geoms.append(Polygon(pts))
                    else:
                        obstacle_geoms.append(ls.buffer(0.1))
                else:
                    all_edges.append(ls)

            if "door" in layer or "درب" in layer or t == "ARC":
                if t == "ARC":
                    center = e.dxf.center
                    radius = e.dxf.radius
                    pts_arc = [(center.x + radius * math.cos(math.radians(e.dxf.start_angle + (e.dxf.end_angle - e.dxf.start_angle) * i / 10)),
                                center.y + radius * math.sin(math.radians(e.dxf.start_angle + (e.dxf.end_angle - e.dxf.start_angle) * i / 10))) for i in range(11)]
                    door_elements.append(LineString(pts_arc))
                elif t == "LINE":
                    door_elements.append(LineString([(e.dxf.start.x, e.dxf.start.y), (e.dxf.end.x, e.dxf.end.y)]))

        for entity in msp:
            if entity.dxftype() == "INSERT":
                for sub in entity.virtual_entities():
                    process_entity(sub)
            else:
                process_entity(entity)

        merged = unary_union(all_edges)
        polygons = list(polygonize(merged))

        valid_polygons_data = []
        for p in polygons:
            if p.area < 0.5: continue
            is_inner = not any(p_other.contains(p.buffer(0.01)) for p_other in polygons if p != p_other)
            if is_inner:
                actual_geom = p
                for obs in obstacle_geoms:
                    if p.intersects(obs):
                        try:
                            actual_geom = actual_geom.difference(obs)
                        except:
                            continue
                minx, miny, maxx, maxy = actual_geom.bounds
                w, l = maxx - minx, maxy - miny
                if is_valid_heating_room("check", actual_geom.area, w, l):
                    valid_polygons_data.append({
                        "geom": actual_geom, "width": w, "length": l, 
                        "bounds": (minx, miny, maxx, maxy), "original": p
                    })

        final_rooms = []
        for idx, data in enumerate(valid_polygons_data, 1):
            room_doors = [d for d in door_elements if data["original"].intersects(d.buffer(0.5))]
            final_rooms.append({
                "name": f"فضا {idx}", 
                "width": round(data["width"], 2), 
                "length": round(data["length"], 2),
                "polygon": data["geom"], 
                "bounds": data["bounds"], 
                "area": round(data["geom"].area, 1), 
                "doors": room_doors
            })
        return final_rooms

    except Exception as e:
        print(f"[EXTRACT ERROR] {e}")
        traceback.print_exc()
        return []

# ==================== FastAPI ENDPOINTS ====================
@app.post("/generate")
async def generate(
    full_name: str = Form(...),
    phone: str = Form(None),
    input_mode: str = Form("manual"),
    lang_select: str = Form("fa"),
    room_names: List[str] = Form([]),
    room_widths: List[str] = Form([]),
    room_lengths: List[str] = Form([]),
    project_file: Optional[UploadFile] = File(None)
):
    try:
        print("\n================ START GENERATE ================")

        lang = lang_select if lang_select in TRANSLATIONS else "fa"
        txt = TRANSLATIONS[lang]
        phone_clean = re.sub(r"[^\d+]", "", str(phone or "")).strip()

        print(f"FULL NAME: {full_name}")
        print(f"PHONE: {phone_clean}")
        print(f"INPUT MODE: {input_mode}")

        customer_id = generate_customer_id(full_name, phone_clean)
        safe_name = slugify(full_name)

        user_folder = os.path.join(OUTPUT_DIR, f"{re.sub(r'\\D', '', phone_clean) or 'no-phone'}-{safe_name}")
        os.makedirs(user_folder, exist_ok=True)
        print(f"USER FOLDER: {user_folder}")

        rooms_to_process = []

        if input_mode == "file" and project_file and project_file.filename:
            print(f"UPLOADED FILE: {project_file.filename}")
            path = os.path.join(user_folder, f"Original_{project_file.filename}")
            with open(path, "wb") as b:
                shutil.copyfileobj(project_file.file, b)
            print(f"FILE SAVED: {path}")

            file_ext = os.path.splitext(project_file.filename)[1].lower()
            process_path = path
            if file_ext == '.dwg':
                dxf_path = convert_dwg_to_dxf(path)
                if dxf_path:
                    process_path = dxf_path
                else:
                    return JSONResponse({"status":"error", "message":"تبدیل فایل DWG به DXF با خطا مواجه شد."}, status_code=400)

            rooms_to_process = extract_rooms_and_doors(process_path)
            print(f"DETECTED ROOMS: {len(rooms_to_process)}")

        else:
            print("MANUAL ROOM MODE")
            for i in range(len(room_names)):
                try:
                    w = float(room_widths[i])
                    l = float(room_lengths[i])
                    print(f"ROOM {i+1}: {room_names[i]} | {w} x {l}")
                    rooms_to_process.append({
                        "name": room_names[i] or f"فضا {i+1}",
                        "width": w, "length": l,
                        "polygon": Polygon([(0,0),(w,0),(w,l),(0,l)]),
                        "bounds": (0,0,w,l),
                        "area": round(w*l, 1),
                        "doors": []
                    })
                except Exception as e:
                    print(f"ROOM ERROR: {e}")

        if not rooms_to_process:
            print("NO VALID ROOMS FOUND")
            return JSONResponse({"status":"error","message":"هیچ فضای واجد شرایطی یافت نشد."}, status_code=400)

        # ==================== PDF INIT ====================
        pdf_name = get_unique_filename(user_folder, f"TopSUN-{safe_name}", "pdf")
        pdf_path = os.path.join(user_folder, pdf_name)
        print(f"PDF PATH: {pdf_path}")

        canv = canvas.Canvas(pdf_path, pagesize=landscape(A4))
        W, H = landscape(A4)
        logo_path = os.path.join(STATIC_DIR, "logo.png")
        all_strips_summary = []
        total_insulation_sqm = 0.0

# استفاده از محاسبات دقیق هندسی ۱.۵ متری برای هر اتاق
        room_insulation = calculate_single_room_insulation(poly)
        total_insulation_sqm += room_insulation

        # ==================== GLOBAL PLAN PAGE (دقیقاً مثل Protocol-SF) ====================
        if input_mode == "file" and rooms_to_process:
            print("\n================ GLOBAL PLAN PAGE ================")

            if os.path.exists(logo_path):
                canv.drawImage(ImageReader(logo_path),45,H-55,width=65,height=35,preserveAspectRatio=True,mask='auto')

            canv.setFont(USED_FONT, 16)
            canv.drawRightString(W-45, H-42, f_t("پلان کلی و جانمایی تابلو فرمان", lang))
            canv.line(45, H-60, W-45, H-60)

            all_poly = unary_union([r['polygon'] for r in rooms_to_process])
            g_minx, g_miny, g_maxx, g_maxy = all_poly.bounds
            g_width = max(g_maxx - g_minx, 1)
            g_height = max(g_maxy - g_miny, 1)
            g_scale = min((W-150)/g_width, (H-200)/g_height)
            g_ox = (W - g_width*g_scale)/2
            g_oy = (H - g_height*g_scale)/2

            print(f"GLOBAL SCALE: {g_scale}")

            for room in rooms_to_process:
                print(f"GLOBAL ROOM: {room['name']}")
                p = room['polygon']
                pts = list(p.exterior.coords)
                canv.setLineWidth(2)
                canv.setStrokeColorRGB(0, 0, 0)
                for i in range(len(pts)-1):
                    x1 = g_ox + (pts[i][0] - g_minx) * g_scale
                    y1 = g_oy + (pts[i][1] - g_miny) * g_scale
                    x2 = g_ox + (pts[i+1][0] - g_minx) * g_scale
                    y2 = g_oy + (pts[i+1][1] - g_miny) * g_scale
                    canv.line(x1, y1, x2, y2)

                label_x = g_ox + (p.centroid.x - g_minx) * g_scale
                label_y = g_oy + (p.centroid.y - g_miny) * g_scale
                canv.setFont(USED_FONT, 10)
                canv.drawCentredString(label_x, label_y + 20, f_t(room['name'], lang))

            canv.showPage()

        # ==================== BOM PAGE ====================
        if all_strips_summary:
            if os.path.exists(logo_path):
                canv.drawImage(ImageReader(logo_path),45,H-55,width=65,height=35,preserveAspectRatio=True,mask='auto')

            canv.setFont(USED_FONT, 16)
            canv.drawRightString(W-45, H-42, f_t(txt["bom_title"], lang))
            canv.line(45, H-60, W-45, H-60)

            counts = Counter(all_strips_summary)
            sorted_keys = sorted(counts.keys(), key=lambda x: (x, x), reverse=True)

            table_rows = [[f_t(txt["bom_total"], lang), f_t(txt["bom_unit"], lang), f_t(txt["bom_qty"], lang), f_t(txt["bom_desc"], lang), f_t(txt["bom_row"], lang)]]

            total_80m = sum(qty * round(l, 1) for (w, l), qty in counts.items() if abs(w - 0.8) < 0.01)
            total_40m = sum(qty * round(l, 1) for (w, l), qty in counts.items() if abs(w - 0.4) < 0.01)

            for i, (fw, fl) in enumerate(sorted_keys, 1):
                fl_r = round(fl, 1)
                qty = counts[(fw, fl)]
                table_rows.append([str(round(qty * fl_r, 1)), f_t("متر طول", lang), str(qty),
                                   f_t(f"فیلم حرارتی عرض {int(fw*100)} سانتی‌متر - طول {fl_r} متر", lang), str(i)])

            lidx = len(sorted_keys)
            
            # --- بخش جدید: اعمال منطق رول/مترمربع عایق در جدول PDF ---
            insulation_value, insulation_unit = finalize_insulation_bom(total_insulation_sqm)
            table_rows.append([str(insulation_value), f_t(insulation_unit, lang), "-", f_t("عایق بازتابشی AlumSUN", lang), str(lidx + 1)])
            # ---------------------------------------------------------

            table_rows.append([str(calculate_thermostats([{'w':r['width'],'l':r['length']} for r in rooms_to_process])), f_t("دستگاه", lang), str(calculate_thermostats([{'w':r['width'],'l':r['length']} for r in rooms_to_process])), f_t(txt["thermostat"], lang), str(lidx + 2)])

            cp_label = txt["cp_single"] if len(rooms_to_process) == 1 else txt["cp_multi"]
            table_rows.append(["1", f_t("دستگاه", lang), "1", f_t(cp_label, lang), str(lidx + 3)])

            if total_80m > 0:
                table_rows.append([str(round(total_80m, 1)), f_t("متر طول", lang), "", f_t("مجموع فیلم‌های عرض 80 سانتی‌متر", lang), ""])
            if total_40m > 0:
                table_rows.append([str(round(total_40m, 1)), f_t("متر طول", lang), "", f_t("مجموع فیلم‌های عرض 40 سانتی‌متر", lang), ""])

            table = Table(table_rows, colWidths=[80, 70, 60, 270, 50])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), pdf_colors.lightgrey),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,-1), USED_FONT),
                ('GRID', (0,0), (-1,-1), 1, pdf_colors.black),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
            ]))

            tw, th = table.wrap(W, H)
            table.drawOn(canv, (W - tw) / 2, H - 120 - th)
            canv.showPage()

        canv.save()
        return JSONResponse({
            "status": "success",
            "pdf_url": f"/outputs/{os.path.basename(user_folder)}/{pdf_name}"
        })
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse({"status":"error", "message": str(e)}, status_code=500)

@app.get("/", response_class=HTMLResponse)
async def index():
    try:
        with open(os.path.join(TEMPLATES_DIR, "index.html"), "r", encoding="utf-8") as f: return f.read()
    except: return "Error: templates/index.html not found."

if __name__ == "__main__": uvicorn.run(app, host="127.0.0.1", port=8000)

# ==================== TOTAL METERS ====================
def get_total_meters_from_file(file_path):
    if not os.path.exists(file_path): return 0.0, 0.0

    process_path = file_path
    if file_path.lower().endswith('.dwg'):
        process_path = convert_dwg_to_dxf(file_path)
        if not process_path: return 0.0, 0.0

    rooms = extract_rooms_and_doors(process_path)
    total_80 = 0.0
    total_40 = 0.0

    for room in rooms:
        strips = generate_adaptive_layout(room['polygon'], room['name'], room.get('doors', []))
        for s in strips:
            length = round(s['length'], 1)
            if abs(s['width'] - 0.8) < 0.01: total_80 += length
            elif abs(s['width'] - 0.4) < 0.01: total_40 += length
               
    return round(total_80, 2), round(total_40, 2)


# ==================== توابع محاسباتی برای Streamlit App ====================

def calculate_thermostats(rooms):
    total = 0
    for room in rooms:
        area = room['w'] * room['l']
        total += 1
        if area > 45: total += 1
    return total


def get_meters_from_manual_rooms(rooms):
    if not rooms:
        return 0.0, 0.0, 0.0, "مترمربع"
        
    total_area = sum(r['w'] * r['l'] for r in rooms)
    m80 = round(total_area * 0.75, 2)
    m40 = round(total_area * 0.15, 2)
   
    # محاسبه متراژ ناخالص واقعی عایق بر اساس چیدمان نواری عرض 1.5 متر
    total_insulation_area = 0.0
    for r in rooms:
        # تعداد ردیف‌های ۱.۵ متری مورد نیاز برای عرض این اتاق (گرد شده به بالا)
        rows_count = math.ceil(r['w'] / 1.5)
        # متراژ عایق مصرفی این اتاق با احتساب دورریز لبه‌ها
        total_insulation_area += rows_count * 1.5 * r['l']

    # واحد اولیه همیشه مترمربع هندسی است و پردازش رول/متر در فایل مالی انجام می‌شود
    return m80, m40, round(total_insulation_area, 1), "مترمربع"
# ==================== generate_layout_plan ====================
def generate_layout_plan(file_path, include_overall=True):
    import tempfile
    rooms = extract_rooms_and_doors(file_path)
    if not rooms:
        raise Exception("هیچ فضای قابل پردازش یافت نشد")
    
    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_pdf.close()
    
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import landscape, A4
    from reportlab.lib.utils import ImageReader
    from reportlab.platypus import Table, TableStyle
    from reportlab.lib import colors as pdf_colors
    
    canv = canvas.Canvas(temp_pdf.name, pagesize=landscape(A4))
    W, H = landscape(A4)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir, "static", "logo.png")

    # ==================== صفحه ۱: پلان کلی (فقط در روش آپلود) ====================
    if include_overall and len(rooms) > 1:
        if os.path.exists(logo_path):
            canv.drawImage(ImageReader(logo_path), 45, H - 55, width=65, height=35, preserveAspectRatio=True, mask='auto')
        
        canv.setFont(USED_FONT, 18)
        canv.drawRightString(W - 45, H - 45, f_t("پلان کلی و جانمایی تابلو فرمان", "fa"))
        canv.line(45, H - 65, W - 45, H - 65)
        
        all_poly = unary_union([r['polygon'] for r in rooms])
        minx, miny, maxx, maxy = all_poly.bounds
        width = maxx - minx
        height = maxy - miny
        scale = min((W - 150) / width, (H - 200) / height)
        ox = (W - width * scale) / 2
        oy = (H - height * scale) / 2 - 30
        
        for room in rooms:
            p = room['polygon']
            pts = list(p.exterior.coords)
            canv.setLineWidth(2.5)
            canv.setStrokeColorRGB(0.1, 0.1, 0.1)
            for i in range(len(pts)-1):
                x1 = ox + (pts[i][0] - minx) * scale
                y1 = oy + (pts[i][1] - miny) * scale
                x2 = ox + (pts[i+1][0] - minx) * scale
                y2 = oy + (pts[i+1][1] - miny) * scale
                canv.line(x1, y1, x2, y2)
            
            canv.setFont(USED_FONT, 11)
            canv.drawCentredString(
                ox + (p.centroid.x - minx) * scale,
                oy + (p.centroid.y - miny) * scale + 15,
                f_t(room['name'], "fa")
            )
        canv.showPage()

    # ==================== صفحات تفکیکی هر فضا ====================
    for idx, room in enumerate(rooms, 1):
        if os.path.exists(logo_path):
            canv.drawImage(ImageReader(logo_path), 45, H - 55, width=65, height=35, preserveAspectRatio=True, mask='auto')
        
        canv.setFont(USED_FONT, 16)
        canv.drawRightString(W - 45, H - 42, f_t(f"پلان چیدمان فضا {idx} - {room['name']}", "fa"))
        canv.line(45, H - 60, W - 45, H - 60)

        strips = generate_adaptive_layout(room['polygon'], room['name'], room.get('doors', []))
        
        p = room['polygon']
        minx, miny, maxx, maxy = p.bounds
        r_width = max(maxx - minx, 1)
        r_height = max(maxy - miny, 1)
        scale = min((W - 180) / r_width, (H - 220) / r_height)
        ox = (W - r_width * scale) / 2
        oy = (H - r_height * scale) / 2 - 30

        # رسم دیوار
        pts = list(p.exterior.coords)
        canv.setLineWidth(3)
        canv.setStrokeColorRGB(0.1, 0.1, 0.1)
        for i in range(len(pts)-1):
            x1 = ox + (pts[i][0] - minx) * scale
            y1 = oy + (pts[i][1] - miny) * scale
            x2 = ox + (pts[i+1][0] - minx) * scale
            y2 = oy + (pts[i+1][1] - miny) * scale
            canv.line(x1, y1, x2, y2)

        # رسم فیلم‌های گرمایشی
        for s in strips:
            s_poly = s['geometry']
            s_pts = list(s_poly.exterior.coords)
            canv.setFillColorRGB(1.0, 0.65, 0.25)
            canv.setStrokeColorRGB(0.85, 0.3, 0.0)
            
            path = canv.beginPath()
            path.moveTo(ox + (s_pts[0][0] - minx) * scale, oy + (s_pts[0][1] - miny) * scale)
            for pt in s_pts[1:]:
                path.lineTo(ox + (pt[0] - minx) * scale, oy + (pt[1] - miny) * scale)
            canv.drawPath(path, fill=1, stroke=1)
            
            canv.setFillColorRGB(0, 0, 0)
            canv.setFont(USED_FONT, 9)
            cx = ox + (s_poly.centroid.x - minx) * scale
            cy = oy + (s_poly.centroid.y - miny) * scale
            canv.drawCentredString(cx, cy, f"{s['width']:.1f}×{s['length']:.1f}")

        # اطلاعات پایین
        canv.setFont(USED_FONT, 11)
        info = f"مساحت: {room['area']:.1f} m² | ابعاد: {room['width']:.1f}×{room['length']:.1f} متر"
        canv.drawCentredString(W / 2, 55, f_t(info, "fa"))

        # باکس تایید
        canv.setStrokeColorRGB(0, 0, 0)
        canv.setLineWidth(1)
        canv.rect(50, 85, W-100, 75, stroke=1, fill=0)
        
        canv.setFont(USED_FONT, 9.8)
        canv.drawString(60, 145, f_t("پلان چیدمان گرمایش کف برقی تاپسان مطابق با ابعاد اعلامی کارفرما آقا/خانم ......................................... مورد تایید بوده", "fa"))
        canv.drawString(60, 125, f_t("و لذا درخواست آماده سازی و تولید محصولات طبق پلان ارائه شده فوق را از شرکت تاپسان هیتینگ دارم.", "fa"))
        
        canv.setFont(USED_FONT, 9.5)
        canv.drawString(60, 102, f_t("نام و نام خانوادگی و امضای تایید‌کننده:", "fa"))
        canv.drawString(W//2 + 20, 102, f_t("سمت تایید‌کننده:", "fa"))
        canv.drawString(60, 82, f_t("تاریخ تایید پلان چیدمان:", "fa"))

        canv.showPage()

    # ==================== صفحه BOM ====================
    canv.setFont(USED_FONT, 18)
    canv.drawRightString(W - 45, H - 45, f_t("جدول متره و برآورد تجهیزات (BOM)", "fa"))
    canv.line(45, H - 65, W - 45, H - 65)

    all_strips = []
    for room in rooms:
        strips = generate_adaptive_layout(room['polygon'], room['name'], room.get('doors', []))
        all_strips.extend(strips)

    from collections import Counter
    counts = Counter([(round(s['width'],1), round(s['length'],1)) for s in all_strips])

    table_rows = [["ردیف", "شرح کالا", "تعداد", "واحد", "مقدار کل (متر)"]]
    for i, ((w, l), qty) in enumerate(sorted(counts.items(), reverse=True), 1):
        total = round(qty * l, 1)
        table_rows.append([
            str(i), 
            f"فیلم حرارتی عرض {int(w*100)} سانتی‌متر - طول {l} متر", 
            str(qty), 
            "متر طول", 
            f"{total}"
        ])

    total_area = sum(r['area'] for r in rooms)
    table_rows.append([str(len(table_rows)), "عایق بازتابشی AlumSUN", "-", "مترمربع", f"{round(total_area * 1.1, 1)}"])

    table = Table(table_rows, colWidths=[45, 280, 50, 60, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), pdf_colors.lightgrey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,-1), USED_FONT),
        ('GRID', (0,0), (-1,-1), 0.8, pdf_colors.black),
        ('FONTSIZE', (0,0), (-1,0), 11),
    ]))
    tw, th = table.wrap(W, H)
    table.drawOn(canv, (W - tw)/2, H - 160 - th)
    
    canv.save()
    
    with open(temp_pdf.name, "rb") as f:
        pdf_bytes = f.read()
    try:
        os.remove(temp_pdf.name)
    except:
        pass
    return pdf_bytes