#!/usr/bin/env python3
"""Write reviewed leads to the lead-sheet format.

Usage: python3 build_xlsx.py review.json leads.xlsx
Uses each lead's "email"/"email_source" (pick from "emails_found"; leave empty if none is the creator's own)
and "notes". Columns match the original lead sheet plus dates, email source and notes.
Also appends every lead to exclude_handles.txt, so later searches never return them again.
"""
import datetime, json, os, sys
import openpyxl
from openpyxl.styles import Font, PatternFill

leads = sorted(json.load(open(sys.argv[1])), key=lambda x: x['followers'])
wb = openpyxl.Workbook(); ws = wb.active; ws.title = 'Leads'
ws.append(['Name', 'User Handle', 'Profile link', 'Follower', 'Email', 'Youtube link', 'Location',
           'Last IG post', 'Last YT upload', 'Email source', 'Notes'])
for c in ws[1]:
    c.font = Font(bold=True, color='FFFFFF'); c.fill = PatternFill('solid', fgColor='1F4E78')
link = Font(color='0563C1', underline='single')
for l in leads:
    ws.append([l['name'], '@' + l['handle'], f"https://www.instagram.com/{l['handle']}/", l['followers'],
               l.get('email', ''), l.get('youtube'), l.get('location'), l.get('last_ig_post'),
               l.get('last_yt_upload'), l.get('email_source', ''), l.get('notes', '')])
    row = ws[ws.max_row]
    row[3].number_format = '#,##0'
    for cell, target in ((row[2], row[2].value), (row[5], row[5].value), (row[4], row[4].value and 'mailto:' + row[4].value)):
        if target:
            cell.hyperlink = target; cell.font = link
    if not row[4].value:
        row[4].fill = PatternFill('solid', fgColor='FFF2CC')
for col, w in zip('ABCDEFGHIJK', [28, 18, 42, 10, 30, 44, 16, 13, 14, 40, 55]):
    ws.column_dimensions[col].width = w
ws.freeze_panes = 'A2'
wb.save(sys.argv[2])
ex_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'exclude_handles.txt')
known = {l.split('\t')[0].strip().lower() for l in open(ex_path) if l.strip() and not l.startswith('#')}
new = [l['handle'] for l in leads if l['handle'].lower() not in known]
if new:
    with open(ex_path, 'a') as f:
        f.write(f"\n# {os.path.basename(sys.argv[2])}, {datetime.date.today().isoformat()}\n" + '\n'.join(new) + '\n')
print(f'{len(leads)} leads -> {sys.argv[2]}; {len(new)} added to exclude_handles.txt')
