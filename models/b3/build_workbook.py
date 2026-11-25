"""Build B3 formula workbook with artifact_tool (no field observations invented).

Run from repo root: python models/b3/build_workbook.py
"""
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "data" / "baseline" / "b3-transformer-model.xlsx"
wb = Workbook.create()

NAVY = "#1C344A"
TEAL = "#167C80"
PAPER = "#EDF4F5"
LIGHT = "#F5F8FA"
GRAY = "#4B5563"
BLUE = "#DCEBF5"
YELLOW = "#FFF3DA"


def sheet(name, title, subtitle, headers, row, widths):
    s = wb.worksheets.add(name)
    cols = len(headers)
    last_col = chr(64 + cols)
    s.merge_cells(f"A1:{last_col}1")
    s.get_range("A1").values = [[title]]
    s.get_range(f"A1:{last_col}1").format = {
        "fill": NAVY, "font": {"bold": True, "color": "#FFFFFF", "size": 16},
        "row_height": 34, "vertical_alignment": "center"
    }
    s.merge_cells(f"A2:{last_col}2")
    s.get_range("A2").values = [[subtitle]]
    s.get_range(f"A2:{last_col}2").format = {
        "fill": PAPER, "font": {"color": GRAY, "size": 10},
        "row_height": 24, "vertical_alignment": "center", "wrap_text": True
    }
    s.get_range_by_indexes(row - 1, 0, 1, cols).values = [headers]
    s.get_range_by_indexes(row - 1, 0, 1, cols).format = {
        "fill": TEAL, "font": {"bold": True, "color": "#FFFFFF"},
        "row_height": 27, "wrap_text": True, "vertical_alignment": "center"
    }
    for i, width in enumerate(widths):
        s.get_range_by_indexes(0, i, 80, 1).format.column_width = width
    s.freeze_panes.freeze_rows(row)
    return s


def fill_note(s, cell, msg, colspan):
    r = int(''.join([c for c in cell if c.isdigit()]))
    from_col = cell.rstrip('0123456789')
    col_ordinal = ord(from_col) - ord('A')
    end_col = chr(ord('A') + col_ordinal + colspan - 1)
    if colspan > 1:
        s.merge_cells(f"{cell}:{end_col}{r}")
    s.get_range(cell).values = [[msg]]
    s.get_range(f"{cell}:{end_col}{r}").format = {"fill": YELLOW, "font": {"color": GRAY}, "wrap_text": True, "row_height": 38}


guide = sheet("Guide", "B3 | First-Principles Transformers", "Working analytical model — no field accountability measurement has been made", ["Module", "What changes", "Main output", "Evidence caveat"], 4, [20, 42, 36, 55])
guide.get_range("A5:D8").values = [
 ["Decompose", "One 'loan' → separate information and physical events", "Approximate 300 s journey plus event map", "Time values are reported estimates, not observed stage timings"],
 ["Aggregate", "Individual states → one reconciled item inventory", "Hypothetical 50-asset balance", "All stock counts are fictitious test numbers"],
 ["Normalize", "Raw counts → rates with correct denominator", "Strict/complete/conditional rates", "Category examples are fabricated solely for formula checks"],
 ["Perturb", "Transfers, compliance and admin seconds", "Event record completeness and workload scenarios", "Not an observed baseline, effect, or causal forecast"],
]
guide.get_range("A5:D8").format.wrap_text = True
guide.get_range("A5:D8").format.row_height = 56
fill_note(guide, "A10", "Primary metric is measured only by an independent item snapshot: verified location AND custodian AND condition divided by audited durable assets.", 4)
fill_note(guide, "A12", "All scenario inputs can be edited. 'Records captured' is NOT 'records correct', and neither alone proves an improvement in actual hostel accountability.", 4)
guide.get_range("A15:D17").values = [
 ["Primary transformers", "Decompose + Aggregate", "For the 6-slide presentation", "Must connect operation → insight → design choice → test"],
 ["Supporting", "Normalize + Perturb", "Guard against denominator and burden errors", "Counterfactual calculations are explicitly hypothetical"],
 ["Source", "A1–A4, B1–B2, professor's term-project brief", "Detailed references in docs/first-principles/", "No identifiable student data stored"],
]
guide.get_range("A15:D17").format.wrap_text = True
guide.get_range("A15:D17").format.row_height = 45

inputs = sheet("Inputs", "Editable inputs & provenance", "Blue values denote recalled/derived inputs; amber denotes illustrative what-if assumptions", ["Parameter", "Value", "Unit", "Evidence class", "Provenance / caveat"], 3, [36, 16, 23, 25, 70])
input_rows = [
 ["Total journey time approx", 300, "seconds", "E: recalled estimate", "Secretary describes approx five minutes end-to-end"],
 ["Walk to / around guard approx", 120, "seconds", "E: recalled estimate", "Approximate; not timed"],
 ["Guard interaction/register approx", 120, "seconds", "E: recalled estimate", "Approximate; not timed"],
 ["Arithmetic remainder (not measured)", None, "seconds", "I: difference", "Total minus other two; NOT observed pickup time"],
 ["Sport-use occasions/wk low", 20, "occasions", "I: reported cadence", "Daily badminton/volleyball; football/cricket alternate days"],
 ["Sport-use occasions/wk high", 22, "occasions", "I: reported cadence", "Not observed loans or distinct borrowers"],
 ["Illustrative usable stock share", 0.80, "fraction", "E: what-if assumption", "80:20 was explicitly NOT audited"],
 ["Illustrative loan multiplier", 2, "loans per occasion", "S: scenario assumption", "Never infer measured transaction count"],
 ["Illustrative initial record capture", 0.95, "probability", "S: model assumption", "Not a measured compliance rate"],
 ["Illustrative per-transfer capture", 0.80, "probability", "S: model assumption", "Assumed independent event compliance"],
 ["Illustrative location capture", 0.90, "probability", "S: model assumption", "Not independently correct location"],
 ["Illustrative condition capture", 0.90, "probability", "S: model assumption", "Not independently correct condition"],
 ["Illustrative transfers per loan", 2, "events", "S: model assumption", "No observed transfer count"],
 ["Illustrative extra admin time", 30, "seconds/loan", "S: model assumption", "Does not count extra transfers or returns"],
]
inputs.get_range("A4:E17").values = input_rows
inputs.get_range("B7").formulas = [["=B4-B5-B6"]]
inputs.get_range("B12:B17").format.fill = YELLOW
inputs.get_range("B4:B6").format.fill = BLUE
inputs.get_range("B8:B9").format.fill = BLUE
inputs.get_range("A4:E17").format.wrap_text = True
inputs.get_range("A4:E17").format.row_height = 31
inputs.get_range("B10:B15").set_number_format("0.00")
fill_note(inputs, "A20", "A3 sports cadence implies 20–22 sport-use occasions/week. Multiplying by assumed borrowing events is a hypothetical scenario, not a guard register count.", 5)

decomp = sheet("Decompose", "T1 | Decompose", "300 seconds is a rough recollection, not a stopwatch record; split physical events from log events", ["Segment", "Seconds", "Evidence", "What is actually recorded", "Design/validation point"], 4, [34, 18, 24, 46, 65])
decomp.get_range("A5:A8").values = [["Walking"],["Guard interaction + writing"],["Unallocated estimated remainder"],["Total (approx.)"]]
for row, ref in [(5, "B5"),(6, "B6"),(7, "B7")]:
    decomp.get_range(f"B{row}").formulas = [[f"=Inputs!{ref}"]]
decomp.get_range("B8").formulas = [["=SUM(B5:B7)"]]
decomp.get_range("C5:E8").values = [
 ["Secretary recollection", "Not applicable", "Measure travel separately"],
 ["Secretary recollection", "Guard writes declared items, signature and time", "Separate queue, interaction and entry time"],
 ["Arithmetic only", "Not a measured collection duration", "Do not attribute it to a particular step"],
 ["Estimate, unverified", "Not a measured service time", "Not evidence of an intervention's benefit"],
]
decomp.get_range("A11:E11").values = [["Event boundary", "Actor", "Physical event", "Recorded in current register?", "Potential mismatch"]]
decomp.get_range("A11:E11").format = {"fill": TEAL, "font": {"bold": True, "color": "#FFFFFF"}, "row_height": 25}
decomp.get_range("A12:E17").values = [
 ["Access/key sign-out", "Guard and student", "Key changes hands", "Yes (reported)", "A key receipt is not asset custody"],
 ["Item withdrawal", "Student", "Unverified assets leave storage", "Declared items only", "Quantity/identity unverified"],
 ["Custody transfer", "Student/team", "Equipment passed during or after play", "No routine update", "Last holder not established"],
 ["Physical return", "Student", "Equipment purportedly put back", "Return declaration, not verified", "Missing item may be logged returned"],
 ["Condition inspection", "No assigned routine role", "Usability may have changed", "Not systematically", "Damaged and usable mixed"],
 ["Repair/retirement", "Secretary/vendor", "Availability changes", "Bills and informal coordination", "Incomplete item status history"],
]
decomp.get_range("A5:E17").format.wrap_text = True
decomp.get_range("A12:E17").format.row_height = 48

agg = sheet("Aggregate", "T2 | Aggregate", "FICTITIOUS 50-ASSET example only: no Alaknanda physical inventory audit", ["Exclusive admin state", "Toy item count", "Share of counted", "State meaning / note"], 4, [36, 18, 22, 70])
agg.get_range("A5:B11").values = [
 ["Available",31],["Issued",9],["Pending inspection",2],["Quarantined",3],
 ["Off-site repair",2],["Missing/unknown",1],["Retired",2],
]
agg.get_range("A12:A15").values = [["All registered (including retired)"], ["Active (not retired)"], ["Immediately available"], ["Reconciliation check"]]
agg.get_range("B12").formulas = [["=SUM(B5:B11)"]]
agg.get_range("B13").formulas = [["=B12-B11"]]
agg.get_range("B14").formulas = [["=B5"]]
agg.get_range("B15").formulas = [["=B12-SUM(B5:B11)"]]
for r in range(5,12):
    agg.get_range(f"C{r}").formulas = [[f"=IFERROR(B{r}/$B$12,0)"]]
agg.get_range("C5:C11").set_number_format("0.0%")
agg.get_range("D5:D15").values = [
 ["Usable and in authorized storage"], ["In responsible custody; separate condition attribute"],
 ["Returned but not inspected"], ["Unusable/pending repair decision"],
 ["At repair shop, not in storage"],["Unreconciled whereabouts, not proven stolen"],
 ["Written off, excluded from active"],["Toy accounting sum"],
 ["Includes unresolved/missing until retired"],["Subset of active"],["Must equal 0"],
]
agg.get_range("A5:D15").format.wrap_text = True
agg.get_range("B5:B11").format.fill = YELLOW
fill_note(agg, "A18", "Never count a kit and all its component assets separately. Track durable assets individually, consumables by lot/quantity, and condition as a separate attribute.", 4)

norm = sheet("Normalize", "T3 | Normalize", "ALL ROWS ARE INVENTED FOR A DENOMINATOR EXAMPLE — not measured hostel results", ["Sport (toy)", "Audited", "Assessable", "Verified correct", "Strict verified", "Record completeness", "Accuracy if assessable"], 4, [27, 15, 18, 18, 20, 23, 25])
norm.get_range("A5:D7").values = [["Badminton (fictitious)", 20, 8, 5],["Cricket (fictitious)",10,5,3],["Football (fictitious)",12,10,8]]
norm.get_range("A8").values = [["Synthetic combined sample"]]
for col in ("B","C","D"):
    norm.get_range(f"{col}8").formulas = [[f"=SUM({col}5:{col}7)"]]
for r in range(5,9):
    norm.get_range(f"E{r}").formulas = [[f'=IFERROR(D{r}/B{r},"")']]
    norm.get_range(f"F{r}").formulas = [[f'=IFERROR(C{r}/B{r},"")']]
    norm.get_range(f"G{r}").formulas = [[f'=IFERROR(D{r}/C{r},"")']]
norm.get_range("E5:G8").set_number_format("0.0%")
norm.get_range("B5:D7").format.fill = YELLOW
fill_note(norm, "A11", "Strict verified (primary KPI) = fully independently correct triads ÷ all audited. Unknown is not automatically an incorrect observation.", 7)
fill_note(norm, "A13", "Record completeness = fully assessable ÷ all audited; conditional accuracy = correct ÷ assessable. A missing denominator means undefined, not zero.", 7)

pert = sheet("Perturb", "T4 | Perturb", "Hypothetical independent record-capture model, and hypothetical staffing overhead (NOT field baseline)", ["Transfer capture", "k=0", "k=1", "k=2", "k=3", "k=4", "k=5", "Interpretation"], 4, [23, 14, 14, 14, 14, 14, 14, 43])
pert.get_range("A5:A8").values = [[0.5], [0.7], [0.8], [0.95]]
pert.get_range("A5:A8").set_number_format("0%")
for r in range(5,9):
    for i,col in enumerate('BCDEFG'):
        pert.get_range(f"{col}{r}").formulas = [[f"=Inputs!$B$12*$A{r}^{i}*Inputs!$B$14*Inputs!$B$15"]]
pert.get_range("B5:G8").set_number_format("0.0%")
pert.get_range("H5:H8").values = [["Chance all required *records* exist; assumes independence"] for _ in range(4)]
pert.get_range("A5:A8").format.fill = YELLOW
pert.get_range("H5:H8").format.wrap_text = True
pert.get_range("A5:H8").format.row_height = 36
pert.merge_cells("A11:H11")
pert.get_range("A11").values = [["Documentation friction: estimated events/week × additional seconds/event ÷ 60 = hypothetical person-minutes/week"]]
pert.get_range("A11:H11").format = {"fill": PAPER, "font": {"bold": True, "color": NAVY}, "row_height": 30, "wrap_text": True}
pert.get_range("A13:H13").values = [["Events per occasion", "Extra sec/event", "Loans/week low", "Loans/week high", "Extra min/week low", "Extra min/week high", "Evidence status", "Meaning"]]
pert.get_range("A13:H13").format = {"fill": TEAL, "font": {"bold": True, "color": "#FFFFFF"}, "row_height": 30, "wrap_text": True}
r = 14
for mult in (1,2,3):
    for sec in (15,30,60,120):
        pert.get_range(f"A{r}:B{r}").values = [[mult,sec]]
        pert.get_range(f"C{r}").formulas = [[f"=Inputs!$B$8*A{r}"]]
        pert.get_range(f"D{r}").formulas = [[f"=Inputs!$B$9*A{r}"]]
        pert.get_range(f"E{r}").formulas = [[f"=C{r}*B{r}/60"]]
        pert.get_range(f"F{r}").formulas = [[f"=D{r}*B{r}/60"]]
        pert.get_range(f"G{r}:H{r}").values = [["Scenario only", "Does not include return or additional transfer events"]]
        r+=1
pert.get_range("A14:B25").format.fill = YELLOW
pert.get_range("A14:H25").format.row_height = 23
pert.get_range("E14:F25").set_number_format("0.0")
fill_note(pert, "A28", "These modelled percentages are probability of capturing EVERY required record under toy independent event assumptions — NOT probability the data are true, NOT measured accountability, and NOT intervention effectiveness.", 8)

trace = sheet("Traceability", "Research → equation → decision → test", "Provisional design implications; Phase C comparisons and Phase E measurements remain outstanding", ["Transformer", "Mathematical operation", "Insight", "Candidate design consequence", "Validation method", "Evidence status"], 4, [18, 50, 47, 55, 57, 32])
trace.get_range("A5:F8").values = [
 ["Decompose", "T_total=sum(T_stages); separate unlogged event boundaries", "Key access record is not verified custody/condition", "Trial low-friction item, group and kit-level logging", "Observe real/controlled handovers and match actual vs recorded events", "Structural; effect unmeasured"],
 ["Aggregate", "N_all=sum(exclusive states); N_active=N_all-N_retired", "Current stock needs independently reconciled states", "Durable IDs, quantity lots, quarantine, kit manifests", "Permissioned physical census and ledger matching", "Identity valid; inputs toy"],
 ["Normalize", "strict=correct/audited; completeness=assessable/audited", "Missingness and correctness must not be conflated", "Report rates with unknowns, numerator/denominator, audit time", "Independent item-level audits across sports", "Baseline unmeasured"],
 ["Perturb", "P=p_issue*p_transfer^k*p_location*p_condition; W=N*t/60", "Handovers and added logging burden expose trade-off", "Test group custody/quick kit checkout/offline options", "Counterbalanced task tests with staff/student effort and correctness", "Only hypothetical"],
]
trace.get_range("A5:F8").format.wrap_text = True
trace.get_range("A5:F8").format.row_height = 66

# avoid stale metadata / style complexity and export only meaningful finished artifact
TARGET.parent.mkdir(parents=True, exist_ok=True)
SpreadsheetFile.export_xlsx(wb).save(str(TARGET))
print("EXPORTED", TARGET, "bytes", TARGET.stat().st_size)
print("INSPECT", wb.inspect({"kind":"table", "range":"Perturb!A4:H8", "include":"values,formulas", "table_max_rows":5, "table_max_cols":8}).ndjson[:1700])
print("ERRORS", wb.inspect({"kind":"match", "search_term":"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A", "options":{"use_regex":True, "max_results":30}, "summary":"B3 errors"}).ndjson[:1000])
