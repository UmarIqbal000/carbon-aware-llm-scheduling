"""Assemble Umar_Iqbal_CarbonAware_LLM_Full_Package.pdf without altering source PDFs."""

from pathlib import Path
from pypdf import PdfReader, PdfWriter

COMBINED_DIR = Path(__file__).resolve().parent
PAPER_DIR = COMBINED_DIR.parent

COVER_PDF = COMBINED_DIR / "cover.pdf"
MAIN_PDF = PAPER_DIR / "main.pdf"
SUPP_PDF = PAPER_DIR / "supplement.pdf"
BANNER_PDF = COMBINED_DIR / "supp_banner_overlay.pdf"
ELSEVIER_FM_PDF = COMBINED_DIR / "elsevier_frontmatter.pdf"
OUT_PDF = COMBINED_DIR / "Umar_Iqbal_CarbonAware_LLM_Full_Package.pdf"


def main() -> None:
    writer = PdfWriter()

    cover_reader = PdfReader(str(COVER_PDF))
    writer.append(cover_reader, outline_item="Cover and Package Contents")

    main_reader = PdfReader(str(MAIN_PDF))
    main_start = len(writer.pages)
    writer.append(main_reader)
    writer.add_outline_item("Main Manuscript (IEEEtran, 12 pages)", main_start)

    supp_reader = PdfReader(str(SUPP_PDF))
    banner_reader = PdfReader(str(BANNER_PDF))
    banner_page = banner_reader.pages[0]

    supp_start = len(writer.pages)
    first_supp = writer.add_page(supp_reader.pages[0])
    first_supp.merge_page(banner_page)
    for page in supp_reader.pages[1:]:
        writer.add_page(page)
    writer.add_outline_item("Online Supplementary Material (Tables S1 to S7)", supp_start)

    fm_reader = PdfReader(str(ELSEVIER_FM_PDF))
    fm_start = len(writer.pages)
    writer.add_page(fm_reader.pages[0])
    writer.add_outline_item("Graphical Abstract and Research Highlights (Elsevier Material)", fm_start)

    writer.add_metadata({
        "/Title": "Carbon-Aware Scheduling for Phase-Disaggregated LLM Inference in Cloud and Serverless Platforms: Full Package",
        "/Author": "Umar Iqbal",
        "/Subject": "Review, Discrete-Event Simulation, Online Supplement (Tables S1-S7), and Graphical Abstract",
    })

    with open(OUT_PDF, "wb") as f:
        writer.write(f)
    print(f"Wrote {OUT_PDF} ({len(writer.pages)} pages, {OUT_PDF.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
