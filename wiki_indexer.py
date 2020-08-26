import xml.sax

if __name__ == "__main__":
    

    xmlPath = sys.argv[1]
    outputPath = sys.argv[2]

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    wikiHandler = WikiXMLHandler(outputPath)
    parser.setContentHandler(wikiHandler)
    parser.parse(xmlPath)
    

