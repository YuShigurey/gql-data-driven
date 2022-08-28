import pandas

def to_rst(df: pandas.DataFrame):
    """
===== ======================================================= =====
name  Description                                             Type 
===== ======================================================= =====
a     This is just a good example of don't do any thing silly str 
.     .                                                       .
===== ======================================================= =====
    """
    equal_signs = list()
    for column in df.columns:
        equal_signs.append("=" * max(len(str(column)), 5))

    for line in df.values:
        for idx, string in enumerate(line):
            if len(equal_signs[idx]) < len(string):
                equal_signs[idx] = len(string) * "="
            
    def align_columns(strings: list[str]):
        
        strings = [string + ' ' * (len(equal_signs[idx]) - len(string)) for idx, string in enumerate(strings)]
        return strings

    heading1 = " ".join(align_columns(equal_signs))
    heading2 = " ".join(align_columns(df.columns))
    heading3 = heading1
    body = "\n".join([" ".join(align_columns(strings)) for strings in df.values] )
    ending = heading1

    return "\n".join([heading1,heading2,heading3,body,ending])


if __name__ == "__main__":
    from init_data_from_md import read_md_table
    df = read_md_table("""| name | Description | Type |
|:----|:-----------|:---- |
| a   | This is just a good example of don't do any thing silly   | str  |""".split("\n")
    )
    print(df.iloc[0])

    