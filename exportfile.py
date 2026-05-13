# # # # # import requests
# # # # # import pandas as pd
# # # # # import xml.etree.ElementTree as ET

# # # # # url = "http://localhost:900"

# # # # # xml_request = """
# # # # # <ENVELOPE>
# # # # #  <HEADER>
# # # # #   <TALLYREQUEST>Export</TALLYREQUEST>
# # # # #   <TYPE>Collection</TYPE>
# # # # #   <ID>Ledger Collection</ID>
# # # # #  </HEADER>
# # # # #  <BODY>
# # # # #   <DESC>
# # # # #    <STATICVARIABLES>
# # # # #     <SVEXPORTFORMAT>XML</SVEXPORTFORMAT>
# # # # #    </STATICVARIABLES>
# # # # #    <TDL>
# # # # #     <TDLMESSAGE>
# # # # #      <COLLECTION NAME="Ledger Collection">
# # # # #       <TYPE>Ledger</TYPE>
# # # # #       <FETCH>Name, Parent, OpeningBalance</FETCH>
# # # # #      </COLLECTION>
# # # # #     </TDLMESSAGE>
# # # # #    </TDL>
# # # # #   </DESC>
# # # # #  </BODY>
# # # # # </ENVELOPE>
# # # # # """

# # # # # headers = {"Content-Type": "text/xml"}

# # # # # response = requests.post(url, data=xml_request, headers=headers)

# # # # # root = ET.fromstring(response.text)

# # # # # rows = []

# # # # # for ledger in root.findall(".//LEDGER"):
# # # # #     rows.append({
# # # # #         "Ledger": ledger.findtext("NAME"),
# # # # #         "Group": ledger.findtext("PARENT"),
# # # # #         "Opening Balance": ledger.findtext("OPENINGBALANCE")
# # # # #     })

# # # # # df = pd.DataFrame(rows)

# # # # # df.to_excel("tally_output.xlsx", index=False)

# # # # # print("✅ Exported to tally_output.xlsx")

# # # # #Stock monthly summary export
# # # # import requests
# # # # import pandas as pd
# # # # import xml.etree.ElementTree as ET

# # # # # ---------------- CONFIG ----------------
# # # # URL = "http://localhost:900"
# # # # HEADERS = {"Content-Type": "text/xml"}
# # # # OUTPUT_FILE = "stock_monthly_summary.xlsx"

# # # # # ---------------- XML REQUEST ----------------
# # # # xml_request = """
# # # # <ENVELOPE>
# # # #  <HEADER>
# # # #   <TALLYREQUEST>Export</TALLYREQUEST>
# # # #   <TYPE>Collection</TYPE>
# # # #   <ID>StockVoucherCollection</ID>
# # # #  </HEADER>
# # # #  <BODY>
# # # #   <DESC>
# # # #    <STATICVARIABLES>
# # # #     <SVEXPORTFORMAT>XML</SVEXPORTFORMAT>
# # # #    </STATICVARIABLES>
# # # #    <TDL>
# # # #     <TDLMESSAGE>
# # # #      <COLLECTION NAME="StockVoucherCollection">
# # # #       <TYPE>Voucher</TYPE>
# # # #       <FETCH>Date, VoucherTypeName, StockItemName, BilledQty</FETCH>
# # # #      </COLLECTION>
# # # #     </TDLMESSAGE>
# # # #    </TDL>
# # # #   </DESC>
# # # #  </BODY>
# # # # </ENVELOPE>
# # # # """

# # # # # ---------------- FETCH DATA ----------------
# # # # response = requests.post(URL, data=xml_request, headers=HEADERS)

# # # # if response.status_code != 200:
# # # #     print("❌ Failed to connect to Tally")
# # # #     exit()

# # # # root = ET.fromstring(response.text)

# # # # rows = []

# # # # # ---------------- PARSE XML ----------------
# # # # for voucher in root.findall(".//VOUCHER"):

# # # #     date = voucher.findtext("DATE")
# # # #     vtype = voucher.findtext("VOUCHERTYPENAME")

# # # #     for inv in voucher.findall(".//ALLINVENTORYENTRIES.LIST"):

# # # #         item = inv.findtext("STOCKITEMNAME")
# # # #         qty = inv.findtext("BILLEDQTY")

# # # #         if date and item and qty:
# # # #             try:
# # # #                 qty_value = float(qty)

# # # #                 # Classify inward / outward
# # # #                 inward = qty_value if vtype in ["Purchase", "Receipt Note"] else 0
# # # #                 outward = abs(qty_value) if vtype in ["Sales", "Delivery Note"] else 0

# # # #                 rows.append({
# # # #                     "Date": date,
# # # #                     "Month": date[:6],  # YYYYMM
# # # #                     "Item": item,
# # # #                     "Inward Qty": inward,
# # # #                     "Outward Qty": outward
# # # #                 })

# # # #             except:
# # # #                 continue

# # # # # ---------------- DATAFRAME ----------------
# # # # df = pd.DataFrame(rows)

# # # # if df.empty:
# # # #     print("⚠️ No stock data found. Check Tally date/company.")
# # # #     exit()

# # # # # Convert date
# # # # df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")
# # # # df["Month"] = df["Date"].dt.to_period("M")

# # # # # ---------------- GROUPING ----------------
# # # # summary = df.groupby(["Month", "Item"]).agg({
# # # #     "Inward Qty": "sum",
# # # #     "Outward Qty": "sum"
# # # # }).reset_index()

# # # # # Net movement
# # # # summary["Net Qty"] = summary["Inward Qty"] - summary["Outward Qty"]

# # # # # ---------------- EXPORT ----------------
# # # # with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
# # # #     df.to_excel(writer, sheet_name="Raw Data", index=False)
# # # #     summary.to_excel(writer, sheet_name="Monthly Summary", index=False)

# # # # print(f"✅ Report generated: {OUTPUT_FILE}")

# # # import requests
# # # import pandas as pd
# # # import xml.etree.ElementTree as ET

# # # URL = "http://localhost:900"
# # # HEADERS = {"Content-Type": "text/xml"}

# # # # ---------- XML REQUEST (STOCK SUMMARY REPORT) ----------
# # # xml_request = """
# # # <ENVELOPE>
# # #  <HEADER>
# # #   <TALLYREQUEST>Export</TALLYREQUEST>
# # #   <TYPE>Data</TYPE>
# # #   <ID>Stock Summary</ID>
# # #  </HEADER>
# # #  <BODY>
# # #   <DESC>
# # #    <STATICVARIABLES>
# # #     <SVEXPORTFORMAT>XML</SVEXPORTFORMAT>
# # #     <SVFROMDATE>20240401</SVFROMDATE>
# # #     <SVTODATE>20240531</SVTODATE>
# # #    </STATICVARIABLES>
# # #   </DESC>
# # #  </BODY>
# # # </ENVELOPE>
# # # """

# # # # ---------- FETCH DATA ----------
# # # response = requests.post(URL, data=xml_request, headers=HEADERS)

# # # # DEBUG (very important)
# # # if "LINEERROR" in response.text or response.text.strip() == "":
# # #     print("❌ Error or empty response from Tally")
# # #     print(response.text)
# # #     exit()

# # # # ---------- PARSE XML ----------
# # # root = ET.fromstring(response.text)

# # # data = []

# # # # Tally stock summary structure may vary slightly
# # # for item in root.findall(".//STOCKITEM"):
    
# # #     name = item.findtext("NAME", "")
    
# # #     opening_qty = item.findtext("OPENINGBALANCE", "")
# # #     inwards_qty = item.findtext("INWARDS", "")
# # #     outwards_qty = item.findtext("OUTWARDS", "")
# # #     closing_qty = item.findtext("CLOSINGBALANCE", "")

# # #     data.append({
# # #         "Item Name": name,
# # #         "Opening": opening_qty,
# # #         "Inwards": inwards_qty,
# # #         "Outwards": outwards_qty,
# # #         "Closing": closing_qty
# # #     })

# # # # ---------- CHECK DATA ----------
# # # if not data:
# # #     print("⚠️ No stock data found. Try changing date in Tally (Alt + F2 → 1st)")
# # #     exit()

# # # # ---------- CREATE DATAFRAME ----------
# # # df = pd.DataFrame(data)

# # # # ---------- EXPORT TO EXCEL ----------
# # # file_name = "stock_summary.xlsx"

# # # with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
# # #     df.to_excel(writer, sheet_name="Stock Summary", index=False)

# # # print(f"✅ Stock Summary Exported: {file_name}")

# # import requests
# # import pandas as pd
# # import xml.etree.ElementTree as ET

# # URL = "http://localhost:900"
# # HEADERS = {"Content-Type": "text/xml"}

# # # ---------- XML REQUEST (STOCK SUMMARY REPORT) ----------
# # xml_request = """
# # <ENVELOPE>
# #  <HEADER>
# #   <TALLYREQUEST>Export</TALLYREQUEST>
# #   <TYPE>Data</TYPE>
# #   <ID>Stock Summary</ID>
# #  </HEADER>
# #  <BODY>
# #   <DESC>
# #    <STATICVARIABLES>
# #     <SVEXPORTFORMAT>XML</SVEXPORTFORMAT>
# #     <SVFROMDATE>20240401</SVFROMDATE>
# #     <SVTODATE>20240531</SVTODATE>
# #    </STATICVARIABLES>
# #   </DESC>
# #  </BODY>
# # </ENVELOPE>
# # """

# # # ---------- FETCH ----------
# # response = requests.post(URL, data=xml_request, headers=HEADERS)

# # if response.status_code != 200:
# #     print("❌ Failed to connect Tally")
# #     exit()

# # if response.text.strip() == "":
# #     print("❌ Empty response (Check Tally running / date)")
# #     exit()

# # # ---------- PARSE XML ----------
# # root = ET.fromstring(response.text)

# # data = []

# # # 🔥 TRY MULTIPLE STRUCTURES (IMPORTANT)
# # # Case 1: STOCKITEM (rare in report)
# # for item in root.findall(".//STOCKITEM"):
# #     data.append({
# #         "Item": item.findtext("NAME", ""),
# #         "Closing Qty": item.findtext("CLOSINGBALANCE", ""),
# #     })

# # # Case 2: DSPSTKINFO (most common for Stock Summary)
# # if not data:
# #     for item in root.findall(".//DSPSTKINFO"):
# #         data.append({
# #             "Item": item.findtext("DSPSTKNAME", ""),
# #             "Closing Qty": item.findtext("DSPCLQTY", ""),
# #             "Closing Value": item.findtext("DSPCLVAL", ""),
# #         })

# # # Case 3: fallback debug parsing
# # if not data:
# #     print("⚠️ Structure not matched — printing available tags:")
# #     tags = set()
# #     for elem in root.iter():
# #         tags.add(elem.tag)
# #     for t in sorted(tags):
# #         print(t)
# #     exit()

# # # ---------- CREATE DATAFRAME ----------
# # df = pd.DataFrame(data)

# # # ---------- EXPORT ----------
# # file_name = "tally_stock_output.xlsx"
# # df.to_excel(file_name, index=False)

# # print(f"✅ Data exported successfully → {file_name}")

# # # # import requests
# # # # import pandas as pd
# # # # import xml.etree.ElementTree as ET

# # # # url = "http://localhost:900"

# # # # xml_request = """
# # # # <ENVELOPE>
# # # #  <HEADER>
# # # #   <TALLYREQUEST>Export</TALLYREQUEST>
# # # #   <TYPE>Collection</TYPE>
# # # #   <ID>Ledger Collection</ID>
# # # #  </HEADER>
# # # #  <BODY>
# # # #   <DESC>
# # # #    <STATICVARIABLES>
# # # #     <SVEXPORTFORMAT>XML</SVEXPORTFORMAT>
# # # #    </STATICVARIABLES>
# # # #    <TDL>
# # # #     <TDLMESSAGE>
# # # #      <COLLECTION NAME="Ledger Collection">
# # # #       <TYPE>Ledger</TYPE>
# # # #       <FETCH>Name, Parent, OpeningBalance</FETCH>
# # # #      </COLLECTION>
# # # #     </TDLMESSAGE>
# # # #    </TDL>
# # # #   </DESC>
# # # #  </BODY>
# # # # </ENVELOPE>
# # # # """

# # # # headers = {"Content-Type": "text/xml"}

# # # # response = requests.post(url, data=xml_request, headers=headers)

# # # # root = ET.fromstring(response.text)

# # # # rows = []

# # # # for ledger in root.findall(".//LEDGER"):
# # # #     rows.append({
# # # #         "Ledger": ledger.findtext("NAME"),
# # # #         "Group": ledger.findtext("PARENT"),
# # # #         "Opening Balance": ledger.findtext("OPENINGBALANCE")
# # # #     })

# # # # df = pd.DataFrame(rows)

# # # # df.to_excel("tally_output.xlsx", index=False)

# # # # print("✅ Exported to tally_output.xlsx")

# # # #Stock monthly summary export
# # # import requests
# # # import pandas as pd
# # # import xml.etree.ElementTree as ET

# # # # ---------------- CONFIG ----------------
# # # URL = "http://localhost:900"
# # # HEADERS = {"Content-Type": "text/xml"}
# # # OUTPUT_FILE = "stock_monthly_summary.xlsx"

# # # # ---------------- XML REQUEST ----------------
# # # xml_request = """
# # # <ENVELOPE>
# # #  <HEADER>
# # #   <TALLYREQUEST>Export</TALLYREQUEST>
# # #   <TYPE>Collection</TYPE>
# # #   <ID>StockVoucherCollection</ID>
# # #  </HEADER>
# # #  <BODY>
# # #   <DESC>
# # #    <STATICVARIABLES>
# # #     <SVEXPORTFORMAT>XML</SVEXPORTFORMAT>
# # #    </STATICVARIABLES>
# # #    <TDL>
# # #     <TDLMESSAGE>
# # #      <COLLECTION NAME="StockVoucherCollection">
# # #       <TYPE>Voucher</TYPE>
# # #       <FETCH>Date, VoucherTypeName, StockItemName, BilledQty</FETCH>
# # #      </COLLECTION>
# # #     </TDLMESSAGE>
# # #    </TDL>
# # #   </DESC>
# # #  </BODY>
# # # </ENVELOPE>
# # # """

# # # # ---------------- FETCH DATA ----------------
# # # response = requests.post(URL, data=xml_request, headers=HEADERS)

# # # if response.status_code != 200:
# # #     print("❌ Failed to connect to Tally")
# # #     exit()

# # # root = ET.fromstring(response.text)

# # # rows = []

# # # # ---------------- PARSE XML ----------------
# # # for voucher in root.findall(".//VOUCHER"):

# # #     date = voucher.findtext("DATE")
# # #     vtype = voucher.findtext("VOUCHERTYPENAME")

# # #     for inv in voucher.findall(".//ALLINVENTORYENTRIES.LIST"):

# # #         item = inv.findtext("STOCKITEMNAME")
# # #         qty = inv.findtext("BILLEDQTY")

# # #         if date and item and qty:
# # #             try:
# # #                 qty_value = float(qty)

# # #                 # Classify inward / outward
# # #                 inward = qty_value if vtype in ["Purchase", "Receipt Note"] else 0
# # #                 outward = abs(qty_value) if vtype in ["Sales", "Delivery Note"] else 0

# # #                 rows.append({
# # #                     "Date": date,
# # #                     "Month": date[:6],  # YYYYMM
# # #                     "Item": item,
# # #                     "Inward Qty": inward,
# # #                     "Outward Qty": outward
# # #                 })

# # #             except:
# # #                 continue

# # # # ---------------- DATAFRAME ----------------
# # # df = pd.DataFrame(rows)

# # # if df.empty:
# # #     print("⚠️ No stock data found. Check Tally date/company.")
# # #     exit()

# # # # Convert date
# # # df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d")
# # # df["Month"] = df["Date"].dt.to_period("M")

# # # # ---------------- GROUPING ----------------
# # # summary = df.groupby(["Month", "Item"]).agg({
# # #     "Inward Qty": "sum",
# # #     "Outward Qty": "sum"
# # # }).reset_index()

# # # # Net movement
# # # summary["Net Qty"] = summary["Inward Qty"] - summary["Outward Qty"]

# # # # ---------------- EXPORT ----------------
# # # with pd.ExcelWriter(OUTPUT_FILE, engine="openpyxl") as writer:
# # #     df.to_excel(writer, sheet_name="Raw Data", index=False)
# # #     summary.to_excel(writer, sheet_name="Monthly Summary", index=False)

# # # print(f"✅ Report generated: {OUTPUT_FILE}")

# # import requests
# # import pandas as pd
# # import xml.etree.ElementTree as ET

# # URL = "http://localhost:900"
# # HEADERS = {"Content-Type": "text/xml"}

# # # ---------- XML REQUEST (STOCK SUMMARY REPORT) ----------
# # xml_request = """
# # <ENVELOPE>
# #  <HEADER>
# #   <TALLYREQUEST>Export</TALLYREQUEST>
# #   <TYPE>Data</TYPE>
# #   <ID>Stock Summary</ID>
# #  </HEADER>
# #  <BODY>
# #   <DESC>
# #    <STATICVARIABLES>
# #     <SVEXPORTFORMAT>XML</SVEXPORTFORMAT>
# #     <SVFROMDATE>20240401</SVFROMDATE>
# #     <SVTODATE>20240531</SVTODATE>
# #    </STATICVARIABLES>
# #   </DESC>
# #  </BODY>
# # </ENVELOPE>
# # """

# # # ---------- FETCH DATA ----------
# # response = requests.post(URL, data=xml_request, headers=HEADERS)

# # # DEBUG (very important)
# # if "LINEERROR" in response.text or response.text.strip() == "":
# #     print("❌ Error or empty response from Tally")
# #     print(response.text)
# #     exit()

# # # ---------- PARSE XML ----------
# # root = ET.fromstring(response.text)

# # data = []

# # # Tally stock summary structure may vary slightly
# # for item in root.findall(".//STOCKITEM"):
    
# #     name = item.findtext("NAME", "")
    
# #     opening_qty = item.findtext("OPENINGBALANCE", "")
# #     inwards_qty = item.findtext("INWARDS", "")
# #     outwards_qty = item.findtext("OUTWARDS", "")
# #     closing_qty = item.findtext("CLOSINGBALANCE", "")

# #     data.append({
# #         "Item Name": name,
# #         "Opening": opening_qty,
# #         "Inwards": inwards_qty,
# #         "Outwards": outwards_qty,
# #         "Closing": closing_qty
# #     })

# # # ---------- CHECK DATA ----------
# # if not data:
# #     print("⚠️ No stock data found. Try changing date in Tally (Alt + F2 → 1st)")
# #     exit()

# # # ---------- CREATE DATAFRAME ----------
# # df = pd.DataFrame(data)

# # # ---------- EXPORT TO EXCEL ----------
# # file_name = "stock_summary.xlsx"

# # with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
# #     df.to_excel(writer, sheet_name="Stock Summary", index=False)

# # print(f"✅ Stock Summary Exported: {file_name}")

# import requests
# import pandas as pd
# import xml.etree.ElementTree as ET

# URL = "http://localhost:900"
# HEADERS = {"Content-Type": "text/xml"}

# # ---------- XML REQUEST (STOCK SUMMARY REPORT) ----------
# xml_request = """
# <ENVELOPE>
#  <HEADER>
#   <TALLYREQUEST>Export</TALLYREQUEST>
#   <TYPE>Data</TYPE>
#   <ID>Stock Summary</ID>
#  </HEADER>
#  <BODY>
#   <DESC>
#    <STATICVARIABLES>
#     <SVEXPORTFORMAT>XML</SVEXPORTFORMAT>
#     <SVFROMDATE>20240401</SVFROMDATE>
#     <SVTODATE>20240531</SVTODATE>
#    </STATICVARIABLES>
#   </DESC>
#  </BODY>
# </ENVELOPE>
# """

# # ---------- FETCH ----------
# response = requests.post(URL, data=xml_request, headers=HEADERS)

# if response.status_code != 200:
#     print("❌ Failed to connect Tally")
#     exit()

# if response.text.strip() == "":
#     print("❌ Empty response (Check Tally running / date)")
#     exit()

# # ---------- PARSE XML ----------
# root = ET.fromstring(response.text)

# data = []

# # 🔥 TRY MULTIPLE STRUCTURES (IMPORTANT)
# # Case 1: STOCKITEM (rare in report)
# for item in root.findall(".//STOCKITEM"):
#     data.append({
#         "Item": item.findtext("NAME", ""),
#         "Closing Qty": item.findtext("CLOSINGBALANCE", ""),
#     })

# # Case 2: DSPSTKINFO (most common for Stock Summary)
# if not data:
#     for item in root.findall(".//DSPSTKINFO"):
#         data.append({
#             "Item": item.findtext("DSPSTKNAME", ""),
#             "Closing Qty": item.findtext("DSPCLQTY", ""),
#             "Closing Value": item.findtext("DSPCLVAL", ""),
#         })

# # Case 3: fallback debug parsing
# if not data:
#     print("⚠️ Structure not matched — printing available tags:")
#     tags = set()
#     for elem in root.iter():
#         tags.add(elem.tag)
#     for t in sorted(tags):
#         print(t)
#     exit()

# # ---------- CREATE DATAFRAME ----------
# df = pd.DataFrame(data)

# # ---------- EXPORT ----------
# file_name = "tally_stock_output.xlsx"
# df.to_excel(file_name, index=False)

# print(f"✅ Data exported successfully → {file_name}")
 
import requests
import pandas as pd
import re
from xml.etree import ElementTree as ET

url = "http://localhost:9000"

# -----------------------------
# CLEAN XML
# -----------------------------
def clean_xml(text):
    text = re.sub(r'&#\d+;', '', text)
    text = re.sub(r'&#x[0-9A-Fa-f]+;', '', text)
    text = re.sub(r'[^\x09\x0A\x0D\x20-\x7F]', '', text)
    return text

def to_float(val):
    try:
        return float(val)
    except:
        return 0.0

def fetch(xml):
    res = requests.post(url, data=xml)
    return ET.fromstring(clean_xml(res.text))

# -----------------------------
# DATE RANGE
# -----------------------------
DATE_XML = """
<SVFROMDATE>20240401</SVFROMDATE>
<SVTODATE>20250331</SVTODATE>
"""

# =============================
# 1️⃣ FETCH GROUP HIERARCHY
# =============================
group_xml = """<ENVELOPE>
<HEADER><TALLYREQUEST>Export</TALLYREQUEST></HEADER>
<BODY>
<DESC>
<STATICVARIABLES>
<SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
</STATICVARIABLES>
<TDL>
<TDLMESSAGE>
<COLLECTION NAME="Groups">
<TYPE>Group</TYPE>
<FETCH>Name, Parent</FETCH>
</COLLECTION>
</TDLMESSAGE>
</TDL>
</DESC>
</BODY>
</ENVELOPE>"""

group_root = fetch(group_xml)

group_map = {}
for grp in group_root.findall(".//GROUP"):
    name = grp.findtext("NAME")
    parent = grp.findtext("PARENT")
    if name:
        group_map[name.strip()] = parent.strip() if parent else ""

# 🔥 Resolve top-level group
def get_main_group(group):
    while group in group_map:
        parent = group_map.get(group)
        if not parent or parent == group:
            break
        group = parent
    return group

# =============================
# 2️⃣ FETCH LEDGERS
# =============================
ledger_xml = f"""<ENVELOPE>
<HEADER><TALLYREQUEST>Export</TALLYREQUEST></HEADER>
<BODY>
<DESC>
<STATICVARIABLES>
{DATE_XML}
<SVEXPORTFORMAT>$$SysName:XML</SVEXPORTFORMAT>
</STATICVARIABLES>
<TDL>
<TDLMESSAGE>
<COLLECTION NAME="LedgerData">
<TYPE>Ledger</TYPE>
<FETCH>Name, Parent, ClosingBalance</FETCH>
</COLLECTION>
</TDLMESSAGE>
</TDL>
</DESC>
</BODY>
</ENVELOPE>"""

root = fetch(ledger_xml)

assets = []
liabilities = []

for led in root.findall(".//LEDGER"):
    name = led.findtext("NAME")
    parent = led.findtext("PARENT")
    bal = to_float(led.findtext("CLOSINGBALANCE"))

    main_group = get_main_group(parent)

    # -----------------------------
    # BALANCE SHEET CLASSIFICATION
    # -----------------------------
    if main_group in ["Capital Account", "Loans (Liability)", "Current Liabilities"]:
        liabilities.append([name, bal])

    elif main_group in ["Current Assets", "Fixed Assets", "Investments"]:
        assets.append([name, abs(bal)])

# =============================
# 3️⃣ OPTIONAL: ADD PROFIT
# =============================
# (Manually adjust if needed)
net_profit = 0  # Replace with your calculated P&L if available
liabilities.append(["Net Profit", net_profit])

# =============================
# 4️⃣ CREATE DATAFRAME
# =============================
bs_df = pd.DataFrame({
    "Assets": pd.Series([x[0] for x in assets]),
    "Amount": pd.Series([x[1] for x in assets]),
    "Liabilities": pd.Series([x[0] for x in liabilities]),
    "Amount_2": pd.Series([x[1] for x in liabilities])
})

# =============================
# 5️⃣ EXPORT
# =============================
bs_df.to_excel("Tally_Balance_Sheet.xlsx", index=False)

print("✅ BALANCE SHEET GENERATED: Tally_Balance_Sheet.xlsx")