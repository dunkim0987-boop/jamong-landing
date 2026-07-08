"""dream-interpretation/docs/policies 의 약관·개인정보 마크다운을 랜딩용 HTML로 변환.

사용법: python build_policies.py
결과: terms.html, privacy.html 생성 (약관 개정 시 다시 돌리면 갱신됨)
"""
import html
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
POLICY_DIR = HERE.parent / "dream-interpretation" / "docs" / "policies"

PAGE_TMPL = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — 자몽</title>
<meta name="description" content="{title} - AI 꿈해몽 서비스 자몽">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
    background:#f7f6fb; color:#2a2540; line-height:1.7; }}
  header {{ background:linear-gradient(135deg,#34215a,#1d1440); color:#fff; padding:28px 20px; text-align:center; }}
  header a {{ color:#ffbfa8; text-decoration:none; font-size:14px; }}
  header h1 {{ font-size:22px; margin-top:8px; letter-spacing:-.3px; }}
  main {{ max-width:760px; margin:0 auto; padding:32px 22px 80px; }}
  h2 {{ font-size:17px; margin:30px 0 10px; color:#34215a; border-bottom:2px solid #eee; padding-bottom:6px; }}
  h3 {{ font-size:15px; margin:20px 0 8px; }}
  p {{ margin:10px 0; font-size:14.5px; }}
  ul {{ margin:10px 0 10px 20px; }}
  li {{ margin:5px 0; font-size:14.5px; }}
  table {{ border-collapse:collapse; width:100%; margin:16px 0; font-size:13px; overflow-x:auto; display:block; }}
  th,td {{ border:1px solid #ddd; padding:8px 10px; text-align:left; vertical-align:top; }}
  th {{ background:#f0edf7; font-weight:600; }}
  hr {{ border:none; border-top:1px solid #e5e2ef; margin:26px 0; }}
  .meta {{ color:#8a83a3; font-size:13px; margin-bottom:8px; }}
  footer {{ text-align:center; color:#a49dbb; font-size:12px; padding:24px; }}
</style>
</head>
<body>
<header>
  <a href="./">← 자몽 홈으로</a>
  <h1>{title}</h1>
</header>
<main>
{body}
</main>
<footer>© 2026 자몽 (JAMONG) · 문의 dunkim0987@gmail.com</footer>
</body>
</html>
"""


def _inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text


def md_to_html(md: str) -> tuple[str, str]:
    lines = md.splitlines()
    title = "자몽"
    out: list[str] = []
    ul: list[str] = []
    table: list[list[str]] = []

    def flush_ul():
        nonlocal ul
        if ul:
            out.append("<ul>" + "".join(f"<li>{_inline(x)}</li>" for x in ul) + "</ul>")
            ul = []

    def flush_table():
        nonlocal table
        if table:
            rows = [r for r in table if not all(re.fullmatch(r"\s*:?-+:?\s*", c) for c in r)]
            if rows:
                head, *body = rows
                thead = "<tr>" + "".join(f"<th>{_inline(c.strip())}</th>" for c in head) + "</tr>"
                tbody = "".join(
                    "<tr>" + "".join(f"<td>{_inline(c.strip())}</td>" for c in r) + "</tr>"
                    for r in body
                )
                out.append(f"<table><thead>{thead}</thead><tbody>{tbody}</tbody></table>")
            table = []

    for ln in lines:
        s = ln.rstrip()
        if s.startswith("|"):
            flush_ul()
            cells = s.strip().strip("|").split("|")
            table.append(cells)
            continue
        flush_table()
        if s.startswith("# "):
            title = s[2:].strip()
        elif s.startswith("## "):
            flush_ul()
            out.append(f"<h2>{_inline(s[3:].strip())}</h2>")
        elif s.startswith("### "):
            flush_ul()
            out.append(f"<h3>{_inline(s[4:].strip())}</h3>")
        elif s.startswith("- "):
            ul.append(s[2:].strip())
        elif re.match(r"^\d+\.\s", s):
            ul.append(re.sub(r"^\d+\.\s", "", s).strip())
        elif s.strip() == "---":
            flush_ul()
            out.append("<hr>")
        elif s.strip() == "":
            flush_ul()
        else:
            flush_ul()
            out.append(f"<p>{_inline(s.strip())}</p>")
    flush_ul()
    flush_table()
    return title, "\n".join(out)


for src, dest in [("terms.md", "terms.html"), ("privacy.md", "privacy.html")]:
    md = (POLICY_DIR / src).read_text(encoding="utf-8")
    title, body = md_to_html(md)
    (HERE / dest).write_text(PAGE_TMPL.format(title=title, body=body), encoding="utf-8")
    print(f"생성: {dest} (제목: {title})")
