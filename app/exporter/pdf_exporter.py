from io import BytesIO

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate


class PDFExporter:

    def export(
        self,
        report: str,
    ) -> bytes:
        """
        Convert report text into PDF bytes.

        The PDF is generated in memory instead of
        being permanently written to disk.
        """

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        # Styles
        styles = getSampleStyleSheet()

        title_style = styles["Heading1"]

        title_style.alignment = TA_CENTER

        heading_style = styles["Heading2"]

        body_style = styles["BodyText"]

        story = []

        lines = report.split("\n")

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # Main title
            if line.startswith("# "):

                story.append(
                    Paragraph(
                        line[2:],
                        title_style,
                    )
                )

            # Section heading
            elif line.startswith("## "):

                story.append(
                    Paragraph(
                        line[3:],
                        heading_style,
                    )
                )

            # Sub heading
            elif line.startswith("###"):

                story.append(
                    Paragraph(
                        line[4:],
                        heading_style,
                    )
                )

            # Bullet point
            elif line.startswith("* "):

                story.append(
                    Paragraph(
                        "• " + line[2:],
                        body_style,
                    )
                )

            elif line.startswith("- "):

                story.append(
                    Paragraph(
                        "• " + line[2:],
                        body_style,
                    )
                )

            # Normal paragraph
            else:

                story.append(
                    Paragraph(
                        line,
                        body_style,
                    )
                )

        # Build PDF
        doc.build(story)

        # Move pointer to beginning
        buffer.seek(0)

        # Return PDF bytes
        return buffer.read()