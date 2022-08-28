from os import cpu_count
import sqlite3
import typing
import pandas

T = typing.TypeVar("T")
TITLE_LEVEL = 4

def main():
    con = sqlite3.connect("foo.db")
    cur = con.cursor()
    tables:dict[str, pandas.DataFrame] = {}

    with open("./sqlitehelper/default.md", 'r') as f:
        md_lines = f.readlines()
        next_start = 0
        while True:
            title, start, end = find_md_table(md_lines[next_start:])
            if start is None:
                break
            else:
                next_start = end
                tables[title] = read_md_table(md_lines[start:end])

    del next_start, start, end, md_lines

    for hasa, attr_table in tables.items():
        res = cur.execute('INSERT INTO has_attribute (name) VALUES (?)', [hasa])
        # res = cur.execute('SELECT last_insert_rowid() AS last_insert_rowid FROM has_attribute')
        hasa_id = res.lastrowid

        cols = attr_table.columns
        fields = ",".join(cols)
        for idx in range(len(attr_table.index)):
            row = attr_table.iloc[idx].values
            fields_value = '"' + '","'.join(row) + '"'
            res = cur.execute(f"INSERT INTO attribute ({fields}) VALUES ({fields_value})")
            attr_id = res.lastrowid

            res = cur.execute(f"INSERT INTO has_attribute_attribute_link (has_attribute_id, attribute_id) VALUES (?, ?)", [hasa_id, attr_id])

    con.commit()


def find_md_table(lines: list[str]) -> tuple[str, int | None, int]:
    import re
    title: str = ""
    start: int | None = None
    end: int = 0
    for idx, line in enumerate(lines):
        if (r := re.match("^" + "#"*TITLE_LEVEL + " " + "(.+)", line)) is not None and r.group(0) != '':
            title = r.group(1)
        if (r:=re.search(r"\|[-|: ]+\|", line)) is not None and r.group(0) != '':
            start = idx - 1
        if start is not None and line.strip(' ') == "\n":
            end = idx
            return title, start, end
    
    return title, None, 0
    


def read_md_table(lines: list[str]) -> pandas.DataFrame:
    """Read md table.

    Args:
        lines (list[str]): lines only contains the md table.

    Returns:
        pandas.DataFrame: DataFrame for further processing.


    """

    def clean(raw: list[str]) -> list[str]:
        ret = raw
        ret = [s.replace('-', ' ') for s in ret]
        ret = [s.strip() for s in ret]
        ret = [s for s in ret if s != '']
        return ret

    header, *lines = lines
    column_names = clean(header.split("|"))

    _, *lines = lines

    data = []
    for _, line in enumerate(lines):
        data.append(clean(line.split("|")))

    return pandas.DataFrame(data, columns = column_names)

if __name__ == '__main__':
    main()