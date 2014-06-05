import sys

import scrape_utils

trans = scrape_utils.translator


def scrape_verbs(filename):
    """Inflected verbs"""
    labels = ['name', 'root', 'class', 'person', 'number', 'mode', 'voice',
              'modification']
    output = []

    output.append(','.join(labels))
    num_written = 0
    for xml in scrape_utils.iter_xml(filename):
        v = xml.find('v')
        cj = v.find('cj')
        _sys = v.find('sys')
        tense = _sys[0]
        np = v.find('np')
        s = xml.find('s')

        # Present system (present, imperfect, imperative, optative)
        if tense.tag == 'prs':
            vclass = tense.attrib.get('k', None)
            mode = trans[tense.find('md')[0].tag]
            voice = trans[tense[1].tag]

        # "Tense paradigm" (future, aorist, conditional, perfect,
        #                   injunctive, benedictive)
        elif tense.tag == 'tp':
            vclass = None
            mode = trans[tense[0].tag]
            voice = trans[tense[1].tag]

        # Passive
        elif tense.tag == 'pas':
            vclass = None
            mode = trans[tense.find('md')[0].tag]
            voice = trans[tense.tag]

        # Periphrastic future
        elif tense.tag == 'pef':
            vclass = None
            mode = trans[tense.tag]
            voice = trans[tense[0].tag]
        else:
            print ET.tostring(xml)

        name = xml.attrib['form']
        root = s.attrib['stem']
        person = trans[np[1].tag]
        number = trans[np[0].tag]
        modification = trans[cj[0].tag]

        # Denominative
        if vclass == '11':
            vclass = 'denom'

        # Print as CSV
        format_str = ','.join('{%s}' % x for x in labels)
        output.append(format_str.format(**{
            'name': name,
            'root': root,
            'class': vclass,
            'person': person,
            'number': number,
            'mode': mode,
            'voice': voice or '',
            'modification': modification or '',
        }))
        num_written += 1

    return '\n'.join(output)


def main():
    if len(sys.argv) < 2:
        print 'Usage: scrape_roots.py <filename>'
        sys.exit()
    print scrape_verbs(sys.argv[1])

if __name__ == '__main__':
    main()