import panflute as pf


class MathReplace():
    def action(self, elem, doc):
        pf.debug('s:', elem)
        if isinstance(elem, pf.Para) and len(elem.content) == 1:
            elem1 = elem.content[0]
            if isinstance(elem1, pf.Math) and elem1.format == 'DisplayMath':
                elem = pf.Table(
                    head=pf.TableHead(
                        pf.TableRow(pf.TableCell(pf.Plain(pf.Str(''))),
                                    pf.TableCell(pf.Plain(elem1)),
                                    pf.TableCell(pf.Plain(pf.Str('a'))))),
                    colspec=[('AlignLeft', 0.1), ('AlignCenter', 0.8),
                             ('AlignRight', 0.1)],
                    caption=pf.Caption()
                    #attributes={
                    #   "alignment":
                    #   ['AlignLeft', 'AlignCenter', 'AlignRight'],
                    #   "width": [0.1, 0.8, 0.1]
                    #                }
                )
                pf.debug(elem.caption)

        if isinstance(elem, pf.Table):
            pf.debug(elem.caption)
        pf.debug('o:', elem)
        return elem

    def __init__(self):
        pass


def main(doc=None):
    replacer = MathReplace()
    return pf.run_filter(replacer.action, doc=doc)


if __name__ == "__main__":
    main()
