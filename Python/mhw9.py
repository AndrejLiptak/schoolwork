def huffman_decode(text: str) -> str:
    s = ""
    res = ""
    for ch in text:
        s = s + ch
        if s == "00":
            res += 'U'
            s = ""
        elif s == "01":
            res += 'G'
            s = ""
        elif s == "10":
            res += "IÁ"
            s = ""
        elif s == "1100":
            res += 'Q'
            s = ""
        elif s == "1101":
            res += 'T'
            s = ""
        elif s == "1110":
            res += 'F'
            s = ""
        elif s == "1111":
            res += 'E'
            s = ""
    return res
