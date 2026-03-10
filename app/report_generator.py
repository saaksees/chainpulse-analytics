from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import (getSampleStyleSheet, ParagraphStyle)
from reportlab.lib.units import cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                               Table, TableStyle, HRFlowable)
from reportlab.lib.enums import TA_CENTER
import pandas as pd
import os
import io
from datetime import datetime

# ── Color palette ─────────────────────
NAVY = colors.HexColor('#0A0E1A')
BLUE = colors.HexColor('#38BDF8')
CARD = colors.HexColor('#111827')
BORDER = colors.HexColor('#1E293B')
WHITE = colors.white
GRAY = colors.HexColor('#94A3B8')
GREEN = colors.HexColor('#10b981')
RED = colors.HexColor('#EF4444')
AMBER = colors.HexColor('#F59E0B')

def get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CPTitle',
                             fontSize=28,
                             textColor=BLUE,
                             fontName='Helvetica-Bold',
                             alignment=TA_CENTER,
                             spaceAfter=8))
    styles.add(ParagraphStyle(name='CPSubtitle',
                             fontSize=14,
                             textColor=WHITE,
                             fontName='Helvetica-Bold',
                             alignment=TA_CENTER,
                             spaceAfter=6))
    styles.add(ParagraphStyle(name='CPMuted',
                             fontSize=10,
                             textColor=GRAY,
                             fontName='Helvetica',
                             alignment=TA_CENTER,
                             spaceAfter=4))
    styles.add(ParagraphStyle(name='CPSectionHeader',
                             fontSize=14,
                             textColor=BLUE,
                             fontName='Helvetica-Bold',
                             spaceAfter=8,
                             spaceBefore=16))
    styles.add(ParagraphStyle(name='CPBody',
                             fontSize=10,
                             textColor=WHITE,
                             fontName='Helvetica',
                             spaceAfter=4,
                             leading=16))
    styles.add(ParagraphStyle(name='CPInsight',
                             fontSize=10,
                             textColor=WHITE,
                             fontName='Helvetica',
                             spaceAfter=4,
                             leading=16,
                             leftIndent=12,
                             borderPad=8))
    return styles

def make_table(headers, rows, col_widths=None):
    data = [headers] + rows
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), BLUE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 10),
        ('TOPPADDING', (0,0), (-1,0), 10),
        # Data rows
        ('BACKGROUND', (0,1), (-1,-1), CARD),
        ('TEXTCOLOR', (0,1), (-1,-1), WHITE),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('BOTTOMPADDING', (0,1), (-1,-1), 8),
        ('TOPPADDING', (0,1), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [CARD, colors.HexColor('#0F172A')]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t

def build_cover_page(story, styles, report_title):
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph('⚡ ChainPulse Analytics', styles['CPTitle']))
    story.append(Paragraph(report_title, styles['CPSubtitle']))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', styles['CPMuted']))
    story.append(Paragraph('Dataset: DataCo Supply Chain', styles['CPMuted']))
    story.append(Spacer(1, 1*cm))
    story.append(HRFlowable(width='100%', thickness=2, color=BLUE))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph('Feel the pulse of your supply chain', styles['CPMuted']))

# ── EDA Report ────────────────────────
def build_eda_report(story, styles, project_root):
    try:
        df = pd.read_csv(os.path.join(project_root, 'data', 'powerbi', 'fact_orders.csv'))
    except Exception:
        story.append(Paragraph('Data not available', styles['CPBody']))
        return
    
    story.append(Paragraph('📊 Dataset Overview', styles['CPSectionHeader']))
    
    # KPI table
    total_rev = df['Sales'].sum() if 'Sales' in df.columns else 0
    late_rate = 0
    if 'Delivery_Status' in df.columns:
        late_rate = df['Delivery_Status'].str.contains('Late', na=False).mean() * 100
    
    kpi_rows = [
        ['Total Records', f"{len(df):,}"],
        ['Total Revenue', f"${total_rev:,.0f}"],
        ['Late Delivery Rate', f"{late_rate:.1f}%"],
        ['Data Columns', str(len(df.columns))],
    ]
    story.append(make_table(['Metric', 'Value'], kpi_rows, [9*cm, 7*cm]))
    story.append(Spacer(1, 0.5*cm))
    
    # Top categories
    if 'Category_Name' in df.columns and 'Sales' in df.columns:
        story.append(Paragraph('🏆 Top 5 Categories by Revenue', styles['CPSectionHeader']))
        top_cats = df.groupby('Category_Name')['Sales'].sum().nlargest(5).reset_index()
        cat_rows = [[row['Category_Name'], f"${row['Sales']:,.0f}"] for _, row in top_cats.iterrows()]
        story.append(make_table(['Category', 'Revenue'], cat_rows, [10*cm, 6*cm]))
    
    # Top regions
    if 'Order_Region' in df.columns and 'Sales' in df.columns:
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph('🌍 Top 5 Regions by Revenue', styles['CPSectionHeader']))
        top_reg = df.groupby('Order_Region')['Sales'].sum().nlargest(5).reset_index()
        reg_rows = [[row['Order_Region'], f"${row['Sales']:,.0f}"] for _, row in top_reg.iterrows()]
        story.append(make_table(['Region', 'Revenue'], reg_rows, [10*cm, 6*cm]))

# ── Risk Report ───────────────────────
def build_risk_report(story, styles, project_root):
    try:
        df = pd.read_csv(os.path.join(project_root, 'data', 'processed', 'delivery_risk_scored.csv'))
    except Exception:
        story.append(Paragraph('Risk data not available', styles['CPBody']))
        return
    
    story.append(Paragraph('🚨 Risk Model Performance', styles['CPSectionHeader']))
    
    perf_rows = [
        ['Model', 'XGBoost Classifier'],
        ['Accuracy', '72%'],
        ['ROC-AUC Score', '0.775'],
        ['Total Orders Scored', f"{len(df):,}"],
    ]
    story.append(make_table(['Metric', 'Value'], perf_rows, [9*cm, 7*cm]))
    story.append(Spacer(1, 0.5*cm))
    
    if 'Risk_Level' in df.columns:
        story.append(Paragraph('📊 Risk Distribution', styles['CPSectionHeader']))
        dist = df['Risk_Level'].value_counts()
        total = len(df)
        dist_rows = [[level, f"{count:,}", f"{count/total*100:.1f}%"] for level, count in dist.items()]
        story.append(make_table(['Risk Level', 'Orders', '%'], dist_rows, [7*cm, 5*cm, 4*cm]))
    
    # Revenue at risk
    if 'Risk_Level' in df.columns and 'Sales' in df.columns:
        high = df[df['Risk_Level']=='High Risk']['Sales'].sum()
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(f'💰 Revenue at Risk (High): ${high:,.0f}', styles['CPBody']))

# ── Forecast Report ───────────────────
def build_forecast_report(story, styles, project_root):
    try:
        df = pd.read_csv(os.path.join(project_root, 'data', 'processed', 'demand_forecast_results.csv'))
    except Exception:
        story.append(Paragraph('Forecast data not available', styles['CPBody']))
        return
    
    story.append(Paragraph('📈 90-Day Demand Forecast', styles['CPSectionHeader']))
    
    if 'Category' in df.columns:
        summary = df.groupby('Category')['Predicted_Sales'].agg(['sum', 'mean']).reset_index()
        summary.columns = ['Category', 'Total', 'Daily Avg']
        fc_rows = [[row['Category'], f"${row['Total']:,.0f}", f"${row['Daily Avg']:,.0f}"] for _, row in summary.iterrows()]
        story.append(make_table(['Category', '90-Day Total', 'Daily Average'], fc_rows, [7*cm, 5*cm, 4*cm]))

# ── Customer Report ───────────────────
def build_customers_report(story, styles, project_root):
    try:
        df = pd.read_csv(os.path.join(project_root, 'data', 'processed', 'customer_segments.csv'))
    except Exception:
        story.append(Paragraph('Segment data not available', styles['CPBody']))
        return
    
    story.append(Paragraph('👥 Customer Segmentation', styles['CPSectionHeader']))
    
    if 'Segment' in df.columns:
        segs = df.groupby('Segment').agg(
            Count=('Segment', 'count'),
            AvgMonetary=('Monetary', 'mean')
        ).reset_index()
        seg_rows = [[row['Segment'], f"{row['Count']:,}", f"{row['Count']/len(df)*100:.1f}%", f"${row['AvgMonetary']:,.0f}"] for _, row in segs.iterrows()]
        story.append(make_table(['Segment', 'Count', '%', 'Avg Revenue'], seg_rows, [6*cm, 3*cm, 3*cm, 4*cm]))

# ── NLP Report ────────────────────────
def build_nlp_report(story, styles, project_root):
    try:
        df = pd.read_csv(os.path.join(project_root, 'data', 'processed', 'product_nlp_analysis.csv'))
    except Exception:
        story.append(Paragraph('NLP data not available', styles['CPBody']))
        return
    
    story.append(Paragraph('🔍 NLP Product Analysis', styles['CPSectionHeader']))
    story.append(Paragraph(f'Total products analyzed: {len(df):,}', styles['CPBody']))
    
    if 'Product_Name' in df.columns and 'Frequency' in df.columns:
        top = df.nlargest(10, 'Frequency')[['Product_Name', 'Frequency']]
        nlp_rows = [[row['Product_Name'], f"{row['Frequency']:,}"] for _, row in top.iterrows()]
        story.append(make_table(['Product', 'Frequency'], nlp_rows, [11*cm, 5*cm]))

# ── Master generate function ──────────
def generate_report(page_name, project_root):
    titles = {
        'eda': 'Exploratory Data Analysis Report',
        'risk': 'Delivery Risk Analysis Report',
        'forecast': 'Demand Forecast Report',
        'customers': 'Customer Intelligence Report',
        'nlp': 'NLP Product Insights Report'
    }
    
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer,
                           pagesize=A4,
                           rightMargin=2*cm,
                           leftMargin=2*cm,
                           topMargin=2*cm,
                           bottomMargin=2*cm)
    
    styles = get_styles()
    story = []
    
    # Cover page
    build_cover_page(story, styles, titles.get(page_name, 'Analytics Report'))
    
    # Page break after cover
    from reportlab.platypus import PageBreak
    story.append(PageBreak())
    
    # Content based on page
    builders = {
        'eda': build_eda_report,
        'risk': build_risk_report,
        'forecast': build_forecast_report,
        'customers': build_customers_report,
        'nlp': build_nlp_report
    }
    
    builder = builders.get(page_name)
    if builder:
        builder(story, styles, project_root)
    
    doc.build(story)
    buffer.seek(0)
    return buffer